param(
    [string]$Server = "localhost",
    [string]$Database = "NetZero_VN_DWH"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$DataDir = Join-Path $RootDir "data"

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " [NETZERO DWH] LOAD DATA INTO SQL SERVER ($Database)" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan

$connString = "Server=$Server;Database=$Database;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connString)
$conn.Open()

function Exec-Sql([string]$sql) {
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $sql
    $cmd.ExecuteNonQuery() | Out-Null
}

try {
    # 1. Truncate Staging
    Write-Host "[BUOC 1] Lam sach 4 bang Staging..." -ForegroundColor Yellow
    Exec-Sql "EXEC staging.sp_Truncate_Staging;"
    Write-Host "  -> Done." -ForegroundColor Green

    # 2. Load wb_national_emissions.csv
    Write-Host "[BUOC 2] Nap wb_national_emissions.csv vao stg_wb_national_emissions..." -ForegroundColor Yellow
    $wbPath = Join-Path $DataDir "staging\wb_national_emissions.csv"
    $wbRows = Import-Csv $wbPath -Encoding UTF8
    foreach ($row in $wbRows) {
        $year = $row.Year
        $co2 = if ([string]::IsNullOrWhiteSpace($row.CO2_MtCO2e)) { "NULL" } else { $row.CO2_MtCO2e }
        $co2Cap = if ([string]::IsNullOrWhiteSpace($row.CO2_Per_Capita_Tonnes)) { "NULL" } else { $row.CO2_Per_Capita_Tonnes }
        $gdp = if ([string]::IsNullOrWhiteSpace($row.GDP_USD)) { "NULL" } else { $row.GDP_USD }
        $ch4 = if ([string]::IsNullOrWhiteSpace($row.Methane_MtCO2e)) { "NULL" } else { $row.Methane_MtCO2e }
        $ren = if ([string]::IsNullOrWhiteSpace($row.Renewable_Energy_Pct)) { "NULL" } else { $row.Renewable_Energy_Pct }
        $tot = if ([string]::IsNullOrWhiteSpace($row.Total_GHG_MtCO2e)) { "NULL" } else { $row.Total_GHG_MtCO2e }
        
        $sql = "INSERT INTO staging.stg_wb_national_emissions ([Year], [CO2_MtCO2e], [CO2_Per_Capita_Tonnes], [GDP_USD], [Methane_MtCO2e], [Renewable_Energy_Pct], [Total_GHG_MtCO2e]) VALUES ($year, $co2, $co2Cap, $gdp, $ch4, $ren, $tot);"
        Exec-Sql $sql
    }
    Write-Host "  -> Nap thanh cong $($wbRows.Count) dong." -ForegroundColor Green

    # 3. Load cw_sector_emissions.csv
    Write-Host "[BUOC 3] Nap cw_sector_emissions.csv vao stg_cw_sector_emissions..." -ForegroundColor Yellow
    $cwPath = Join-Path $DataDir "staging\cw_sector_emissions.csv"
    $cwRows = Import-Csv $cwPath -Encoding UTF8
    foreach ($row in $cwRows) {
        $year = $row.Year
        $secCode = $row.Sector_Code.Replace("'", "''")
        $secEN = $row.Sector_Name_EN.Replace("'", "''")
        $secVI = $row.Sector_Name_VI.Replace("'", "''")
        $secCat = $row.Sector_Category.Replace("'", "''")
        $gas = $row.Gas.Replace("'", "''")
        $src = $row.Source.Replace("'", "''")
        $emi = if ([string]::IsNullOrWhiteSpace($row.Emissions_MtCO2e)) { "NULL" } else { $row.Emissions_MtCO2e }

        $sql = "INSERT INTO staging.stg_cw_sector_emissions ([Year], [Sector_Code], [Sector_Name_EN], [Sector_Name_VI], [Sector_Category], [Gas], [Source], [Emissions_MtCO2e]) VALUES ($year, '$secCode', '$secEN', N'$secVI', '$secCat', '$gas', '$src', $emi);"
        Exec-Sql $sql
    }
    Write-Host "  -> Nap thanh cong $($cwRows.Count) dong." -ForegroundColor Green

    # 4. Load gso_provincial_economy.csv
    Write-Host "[BUOC 4] Nap gso_provincial_economy.csv vao stg_gso_provincial_economy..." -ForegroundColor Yellow
    $gsoPath = Join-Path $DataDir "staging\gso_provincial_economy.csv"
    $gsoRows = Import-Csv $gsoPath -Encoding UTF8
    foreach ($row in $gsoRows) {
        $year = $row.Year
        $pCode = $row.Province_Code.Replace("'", "''")
        $pName = $row.Province_Name.Replace("'", "''")
        $grdp = if ([string]::IsNullOrWhiteSpace($row.GRDP_Billion_VND)) { "0" } else { $row.GRDP_Billion_VND }
        $pop = if ([string]::IsNullOrWhiteSpace($row.Population)) { "0" } else { $row.Population }
        $ind = if ([string]::IsNullOrWhiteSpace($row.Industrial_Output_Billion_VND)) { "0" } else { $row.Industrial_Output_Billion_VND }
        $for = if ([string]::IsNullOrWhiteSpace($row.Forest_Coverage_Pct)) { "0" } else { $row.Forest_Coverage_Pct }
        $carb = if ([string]::IsNullOrWhiteSpace($row.Estimated_Carbon_Tonnes)) { "0" } else { $row.Estimated_Carbon_Tonnes }
        $dec = if ([string]::IsNullOrWhiteSpace($row.Decoupling_Index)) { "0" } else { $row.Decoupling_Index }

        $sql = "INSERT INTO staging.stg_gso_provincial_economy ([Year], [Province_Code], [Province_Name], [GRDP_Billion_VND], [Population], [Industrial_Output_Billion_VND], [Forest_Coverage_Pct], [Estimated_Carbon_Tonnes], [Decoupling_Index]) VALUES ($year, '$pCode', N'$pName', $grdp, $pop, $ind, $for, $carb, $dec);"
        Exec-Sql $sql
    }
    Write-Host "  -> Nap thanh cong $($gsoRows.Count) dong." -ForegroundColor Green

    # 5. Load dim_provinces_master.csv
    Write-Host "[BUOC 5] Nap dim_provinces_master.csv vao stg_dim_provinces..." -ForegroundColor Yellow
    $provPath = Join-Path $DataDir "reference\dim_provinces_master.csv"
    $provRows = Import-Csv $provPath -Encoding UTF8
    foreach ($row in $provRows) {
        $pCode = $row.Province_Code.Replace("'", "''")
        $pName = $row.Province_Name.Replace("'", "''")
        $pAscii = $row.Province_Name_Ascii.Replace("'", "''")
        $region = $row.Region.Replace("'", "''")
        $zone = $row.Economic_Zone.Replace("'", "''")
        $area = if ([string]::IsNullOrWhiteSpace($row.Area_Km2)) { "0" } else { $row.Area_Km2 }
        $hub = if ($row.Is_Industrial_Hub -eq "1") { "1" } else { "0" }

        $sql = "INSERT INTO staging.stg_dim_provinces ([Province_Code], [Province_Name], [Province_Name_Ascii], [Region], [Economic_Zone], [Area_Km2], [Is_Industrial_Hub]) VALUES ('$pCode', N'$pName', '$pAscii', N'$region', N'$zone', $area, $hub);"
        Exec-Sql $sql
    }
    Write-Host "  -> Nap thanh cong $($provRows.Count) dong." -ForegroundColor Green

    # 6. Dong bo sang Dimensions
    Write-Host "[BUOC 6] Dong bo Staging vao Dim_Province va Dim_Sector..." -ForegroundColor Yellow
    Exec-Sql "EXEC dwh.sp_Load_Staging_To_Dimensions;"
    Write-Host "  -> Hoan thanh nap Dimensions (63 tinh thanh va 9 nganh IPCC)." -ForegroundColor Green

    # 7. Nap sang Facts
    Write-Host "[BUOC 7] Nap Staging vao Fact_National_Emissions va Fact_Provincial_Economy..." -ForegroundColor Yellow
    Exec-Sql "EXEC dwh.sp_Load_Staging_To_Facts;"
    Write-Host "  -> Hoan thanh nap 2 bang Fact." -ForegroundColor Green

    Write-Host "==========================================================================" -ForegroundColor Green
    Write-Host " >>> NAP DU LIEU HOAN THANH 100%! CSDL DA CO DU LIEU SAN SANG <<<        " -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Green
}
finally {
    $conn.Close()
}
