param(
    [string]$Server = "localhost",
    [string]$Database = "NetZero_VN_DWH"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$DataDir = Join-Path $RootDir "data"

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " [NETZERO DWH] FAST LOAD 1.66M HOURLY MONITORING RECORDS INTO SQL SERVER" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan

$connString = "Server=$Server;Database=$Database;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connString)
$conn.Open()

function Exec-Sql([string]$sql) {
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $sql
    $cmd.CommandTimeout = 600
    $cmd.ExecuteNonQuery() | Out-Null
}

try {
    # 1. Nạp danh mục trạm quan trắc
    Write-Host "[1/4] Nap 189 tram quan trac vao staging.stg_dim_stations..." -ForegroundColor Yellow
    Exec-Sql "TRUNCATE TABLE staging.stg_dim_stations;"
    
    $stationsPath = Join-Path $DataDir "reference\dim_stations_master.csv"
    $stations = Import-Csv $stationsPath -Encoding UTF8
    foreach ($st in $stations) {
        $code = $st.Station_Code.Replace("'", "''")
        $name = $st.Station_Name.Replace("'", "''")
        $pCode = $st.Province_Code.Replace("'", "''")
        $pName = $st.Province_Name.Replace("'", "''")
        $type = $st.Station_Type.Replace("'", "''")
        $lat = $st.Latitude
        $lon = $st.Longitude
        $active = $st.Is_Active
        
        $sql = "INSERT INTO staging.stg_dim_stations ([Station_Code], [Station_Name], [Province_Code], [Province_Name], [Station_Type], [Latitude], [Longitude], [Is_Active]) VALUES ('$code', N'$name', '$pCode', N'$pName', N'$type', $lat, $lon, $active);"
        Exec-Sql $sql
    }
    
    Write-Host "  -> Dong bo sang dwh.Dim_Station..." -ForegroundColor Yellow
    Exec-Sql "EXEC dwh.sp_Load_Station_Dimension;"
    Write-Host "  -> Done: 189 tram da nap vao dwh.Dim_Station." -ForegroundColor Green

    # 2. Xóa dữ liệu staging cũ
    Write-Host "[2/4] Lam sach staging.stg_hourly_air_monitoring..." -ForegroundColor Yellow
    Exec-Sql "TRUNCATE TABLE staging.stg_hourly_air_monitoring;"

    # 3. Stream Bulk Insert 1.66 triệu dòng sử dụng SqlBulkCopy
    $csvFile = Join-Path $DataDir "staging\hourly_air_monitoring_2024.csv"
    Write-Host "[3/4] Streaming SqlBulkCopy 1.66M dong tu $csvFile vao SQL Server..." -ForegroundColor Yellow
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    # Sử dụng Microsoft Visual Basic TextFieldParser hoặc DataTable streaming
    $bulkCopy = New-Object System.Data.SqlClient.SqlBulkCopy($conn)
    $bulkCopy.DestinationTableName = "staging.stg_hourly_air_monitoring"
    $bulkCopy.BatchSize = 50000
    $bulkCopy.BulkCopyTimeout = 600

    # Cấu hình ánh xạ cột
    $colMappings = @(
        "Date_Key", "Year", "Month", "Day", "Hour_24",
        "Station_Code", "Province_Code",
        "CO2_ppm", "CO_mg_m3", "NO2_ug_m3", "SO2_ug_m3",
        "PM25_ug_m3", "PM10_ug_m3", "AQI_Index", "AQI_Category", "Is_Exceeding_QCVN"
    )
    foreach ($col in $colMappings) {
        $bulkCopy.ColumnMappings.Add($col, $col) | Out-Null
    }

    # Đọc stream CSV qua StreamReader và nạp từng batch vào DataTable
    $reader = [System.IO.File]::OpenText($csvFile)
    $headerLine = $reader.ReadLine() # Bỏ qua header
    
    $dt = New-Object System.Data.DataTable
    $dt.Columns.Add("Date_Key", [int]) | Out-Null
    $dt.Columns.Add("Year", [int]) | Out-Null
    $dt.Columns.Add("Month", [byte]) | Out-Null
    $dt.Columns.Add("Day", [byte]) | Out-Null
    $dt.Columns.Add("Hour_24", [byte]) | Out-Null
    $dt.Columns.Add("Station_Code", [string]) | Out-Null
    $dt.Columns.Add("Province_Code", [string]) | Out-Null
    $dt.Columns.Add("CO2_ppm", [decimal]) | Out-Null
    $dt.Columns.Add("CO_mg_m3", [decimal]) | Out-Null
    $dt.Columns.Add("NO2_ug_m3", [decimal]) | Out-Null
    $dt.Columns.Add("SO2_ug_m3", [decimal]) | Out-Null
    $dt.Columns.Add("PM25_ug_m3", [decimal]) | Out-Null
    $dt.Columns.Add("PM10_ug_m3", [decimal]) | Out-Null
    $dt.Columns.Add("AQI_Index", [int]) | Out-Null
    $dt.Columns.Add("AQI_Category", [string]) | Out-Null
    $dt.Columns.Add("Is_Exceeding_QCVN", [byte]) | Out-Null

    $rowCount = 0
    $batchLimit = 50000
    while (($line = $reader.ReadLine()) -ne $null) {
        $parts = $line.Split(',')
        if ($parts.Length -ge 16) {
            $dt.Rows.Add(
                [int]$parts[0],
                [int]$parts[1],
                [byte]$parts[2],
                [byte]$parts[3],
                [byte]$parts[4],
                $parts[5],
                $parts[6],
                [decimal]$parts[7],
                [decimal]$parts[8],
                [decimal]$parts[9],
                [decimal]$parts[10],
                [decimal]$parts[11],
                [decimal]$parts[12],
                [int]$parts[13],
                $parts[14],
                [byte]$parts[15]
            ) | Out-Null
            $rowCount++

            if ($dt.Rows.Count -ge $batchLimit) {
                $bulkCopy.WriteToServer($dt)
                $dt.Clear()
                Write-Host "  -> Da nap $rowCount dong..." -ForegroundColor Gray
            }
        }
    }
    if ($dt.Rows.Count -gt 0) {
        $bulkCopy.WriteToServer($dt)
        $dt.Clear()
    }
    $reader.Close()
    $stopwatch.Stop()
    
    Write-Host "  -> SqlBulkCopy hoan thanh $rowCount dong trong $($stopwatch.Elapsed.TotalSeconds.ToString('F1')) giay!" -ForegroundColor Green

    # 4. Đổ từ staging sang Fact_Hourly_Air_Monitoring
    Write-Host "[4/4] Chuyen doi tu staging sang dwh.Fact_Hourly_Air_Monitoring (kem Columnstore Index)..." -ForegroundColor Yellow
    $factStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    Exec-Sql "EXEC dwh.sp_Load_Hourly_Monitoring_Fact;"
    $factStopwatch.Stop()
    Write-Host "  -> Nap Fact hoan thanh trong $($factStopwatch.Elapsed.TotalSeconds.ToString('F1')) giay." -ForegroundColor Green

    # 5. Kiểm tra tổng kết số dòng
    $cmdCount = $conn.CreateCommand()
    $cmdCount.CommandText = "SELECT COUNT(*) FROM dwh.Fact_Hourly_Air_Monitoring;"
    $finalCount = $cmdCount.ExecuteScalar()

    Write-Host "==========================================================================" -ForegroundColor Green
    Write-Host " >>> TONG KET: BANG dwh.Fact_Hourly_Air_Monitoring HIEN CO $($finalCount.ToString('N0')) DONG! <<<" -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Green
}
finally {
    $conn.Close()
}
