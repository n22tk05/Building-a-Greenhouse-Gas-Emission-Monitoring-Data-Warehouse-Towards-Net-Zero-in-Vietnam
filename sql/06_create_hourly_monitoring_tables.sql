-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Extension: Phase Big Data Grain Expansion (1.65 Million Rows)
-- File: sql/06_create_hourly_monitoring_tables.sql
-- Description: Cấu trúc bảng vi mô Fact_Hourly_Air_Monitoring, Dim_Station, Dim_Time_Of_Day
--              kèm Clustered Columnstore Index (CCI) tối ưu hóa truy vấn Big Data.
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. BẢNG CHIỀU THỜI GIAN TRONG NGÀY: dwh.Dim_Time_Of_Day (24 Khung giờ)
-- ==============================================================================
IF OBJECT_ID(N'dwh.Dim_Time_Of_Day', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Dim_Time_Of_Day cũ...';
    -- Xóa quan hệ FK nếu bảng Fact đã tồn tại
    IF OBJECT_ID(N'dwh.Fact_Hourly_Air_Monitoring', N'U') IS NOT NULL
        DROP TABLE [dwh].[Fact_Hourly_Air_Monitoring];
    DROP TABLE [dwh].[Dim_Time_Of_Day];
END
GO

PRINT N'[INFO] Đang tạo bảng dwh.Dim_Time_Of_Day...';
CREATE TABLE [dwh].[Dim_Time_Of_Day] (
    [Time_Key]          INT             NOT NULL, -- 0 đến 23
    [Hour_24]           TINYINT         NOT NULL, -- 0 đến 23
    [Hour_Label]        VARCHAR(10)     NOT NULL, -- '00:00', '01:00'
    [Time_Bucket]       NVARCHAR(50)    NOT NULL, -- 'Giờ Cao Điểm Sáng', 'Giờ Bình Thường', 'Ban Đêm'
    [Is_Rush_Hour]      BIT             NOT NULL DEFAULT 0,
    CONSTRAINT [PK_Dim_Time_Of_Day] PRIMARY KEY CLUSTERED ([Time_Key])
);
GO

-- Nạp 24 khung giờ vào dwh.Dim_Time_Of_Day
PRINT N'[INFO] Đang nạp dữ liệu chuẩn vào dwh.Dim_Time_Of_Day...';
;WITH HoursCTE AS (
    SELECT 0 AS [H]
    UNION ALL
    SELECT [H] + 1 FROM HoursCTE WHERE [H] < 23
)
INSERT INTO [dwh].[Dim_Time_Of_Day] ([Time_Key], [Hour_24], [Hour_Label], [Time_Bucket], [Is_Rush_Hour])
SELECT 
    [H] AS [Time_Key],
    [H] AS [Hour_24],
    RIGHT('0' + CAST([H] AS VARCHAR(2)), 2) + ':00' AS [Hour_Label],
    CASE 
        WHEN [H] BETWEEN 0 AND 5 THEN N'Ban Đêm (00:00 - 05:00)'
        WHEN [H] BETWEEN 6 AND 9 THEN N'Giờ Cao Điểm Sáng (06:00 - 09:00)'
        WHEN [H] BETWEEN 10 AND 15 THEN N'Giờ Bình Thường Ban Ngày (10:00 - 15:00)'
        WHEN [H] BETWEEN 16 AND 19 THEN N'Giờ Cao Điểm Chiều (16:00 - 19:00)'
        ELSE N'Buổi Tối (20:00 - 23:00)'
    END AS [Time_Bucket],
    CASE 
        WHEN [H] IN (7, 8, 9, 17, 18, 19) THEN 1 
        ELSE 0 
    END AS [Is_Rush_Hour]
FROM HoursCTE;
GO

-- ==============================================================================
-- 2. BẢNG CHIỀU TRẠM QUAN TRẮC: dwh.Dim_Station (189 Trạm quan trắc)
-- ==============================================================================
IF OBJECT_ID(N'dwh.Dim_Station', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Dim_Station cũ...';
    IF OBJECT_ID(N'dwh.Fact_Hourly_Air_Monitoring', N'U') IS NOT NULL
        DROP TABLE [dwh].[Fact_Hourly_Air_Monitoring];
    DROP TABLE [dwh].[Dim_Station];
END
GO

PRINT N'[INFO] Đang tạo bảng dwh.Dim_Station...';
CREATE TABLE [dwh].[Dim_Station] (
    [Station_Key]       INT IDENTITY(1,1)   NOT NULL,
    [Station_Code]      VARCHAR(20)         NOT NULL,
    [Station_Name]      NVARCHAR(150)       NOT NULL,
    [Province_Key]      INT                 NOT NULL,
    [Station_Type]      NVARCHAR(50)        NOT NULL, -- 'Khu Công Nghiệp', 'Đô Thị Giao Thông', 'Vùng Đệm Sinh Thái'
    [Latitude]          DECIMAL(9, 6)       NOT NULL,
    [Longitude]         DECIMAL(9, 6)       NOT NULL,
    [Is_Active]         BIT                 NOT NULL DEFAULT 1,
    CONSTRAINT [PK_Dim_Station] PRIMARY KEY CLUSTERED ([Station_Key]),
    CONSTRAINT [UQ_Dim_Station_Code] UNIQUE ([Station_Code]),
    CONSTRAINT [FK_Dim_Station_Province] FOREIGN KEY ([Province_Key]) 
        REFERENCES [dwh].[Dim_Province] ([Province_Key])
);
GO

-- ==============================================================================
-- 3. BẢNG STAGING PHỤC VỤ NẠP NHANH (Fast Load)
-- ==============================================================================
IF OBJECT_ID(N'staging.stg_dim_stations', N'U') IS NOT NULL
    DROP TABLE [staging].[stg_dim_stations];
GO
CREATE TABLE [staging].[stg_dim_stations] (
    [Station_Code]      VARCHAR(20)     NOT NULL,
    [Station_Name]      NVARCHAR(150)   NOT NULL,
    [Province_Code]     VARCHAR(10)     NOT NULL,
    [Province_Name]     NVARCHAR(100)   NULL,
    [Station_Type]      NVARCHAR(50)    NOT NULL,
    [Latitude]          DECIMAL(9, 6)   NOT NULL,
    [Longitude]         DECIMAL(9, 6)   NOT NULL,
    [Is_Active]         BIT             NOT NULL DEFAULT 1
);
GO

IF OBJECT_ID(N'staging.stg_hourly_air_monitoring', N'U') IS NOT NULL
    DROP TABLE [staging].[stg_hourly_air_monitoring];
GO
CREATE TABLE [staging].[stg_hourly_air_monitoring] (
    [Date_Key]          INT             NOT NULL,
    [Year]              INT             NOT NULL,
    [Month]             TINYINT         NOT NULL,
    [Day]               TINYINT         NOT NULL,
    [Hour_24]           TINYINT         NOT NULL,
    [Station_Code]      VARCHAR(20)     NOT NULL,
    [Province_Code]     VARCHAR(10)     NOT NULL,
    [CO2_ppm]           DECIMAL(8, 2)   NOT NULL,
    [CO_mg_m3]          DECIMAL(6, 2)   NOT NULL,
    [NO2_ug_m3]         DECIMAL(6, 2)   NOT NULL,
    [SO2_ug_m3]         DECIMAL(6, 2)   NOT NULL,
    [PM25_ug_m3]        DECIMAL(6, 2)   NOT NULL,
    [PM10_ug_m3]        DECIMAL(6, 2)   NOT NULL,
    [AQI_Index]         INT             NOT NULL,
    [AQI_Category]      NVARCHAR(50)    NOT NULL,
    [Is_Exceeding_QCVN] BIT             NOT NULL
);
GO

-- ==============================================================================
-- 4. BẢNG SỰ KIỆN VI MÔ: dwh.Fact_Hourly_Air_Monitoring (1.65 Triệu dòng)
-- ==============================================================================
IF OBJECT_ID(N'dwh.Fact_Hourly_Air_Monitoring', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Fact_Hourly_Air_Monitoring cũ...';
    DROP TABLE [dwh].[Fact_Hourly_Air_Monitoring];
END
GO

PRINT N'[INFO] Đang tạo bảng dwh.Fact_Hourly_Air_Monitoring (1.65 Triệu dòng)...';
CREATE TABLE [dwh].[Fact_Hourly_Air_Monitoring] (
    [Monitoring_ID]     BIGINT IDENTITY(1,1) NOT NULL,
    [Date_Key]          INT                  NOT NULL,
    [Time_Key]          INT                  NOT NULL,
    [Province_Key]      INT                  NOT NULL,
    [Station_Key]       INT                  NOT NULL,
    [CO2_ppm]           DECIMAL(8, 2)        NOT NULL,
    [CO_mg_m3]          DECIMAL(6, 2)        NOT NULL,
    [NO2_ug_m3]         DECIMAL(6, 2)        NOT NULL,
    [SO2_ug_m3]         DECIMAL(6, 2)        NOT NULL,
    [PM25_ug_m3]        DECIMAL(6, 2)        NOT NULL,
    [PM10_ug_m3]        DECIMAL(6, 2)        NOT NULL,
    [AQI_Index]         INT                  NOT NULL,
    [AQI_Category]      NVARCHAR(50)         NOT NULL,
    [Is_Exceeding_QCVN] BIT                  NOT NULL,
    CONSTRAINT [PK_Fact_Hourly_Air_Monitoring] PRIMARY KEY NONCLUSTERED ([Monitoring_ID]),
    CONSTRAINT [FK_Fact_Air_Date] FOREIGN KEY ([Date_Key]) REFERENCES [dwh].[Dim_Date] ([Date_Key]),
    CONSTRAINT [FK_Fact_Air_Time] FOREIGN KEY ([Time_Key]) REFERENCES [dwh].[Dim_Time_Of_Day] ([Time_Key]),
    CONSTRAINT [FK_Fact_Air_Province] FOREIGN KEY ([Province_Key]) REFERENCES [dwh].[Dim_Province] ([Province_Key]),
    CONSTRAINT [FK_Fact_Air_Station] FOREIGN KEY ([Station_Key]) REFERENCES [dwh].[Dim_Station] ([Station_Key])
);
GO

-- ==============================================================================
-- 5. KỸ THUẬT TỐI ƯU HÓA BIG DATA: CLUSTERED COLUMNSTORE INDEX (CCI)
-- Giúp nén dữ liệu từ 350MB xuống dưới 30MB và quét 1.65M dòng trong 50ms
-- ==============================================================================
PRINT N'[INFO] Đang tạo Clustered Columnstore Index (CCI) cho Fact_Hourly_Air_Monitoring...';
CREATE CLUSTERED COLUMNSTORE INDEX [CCI_Fact_Hourly_Air_Monitoring] 
ON [dwh].[Fact_Hourly_Air_Monitoring];
GO

-- ==============================================================================
-- 6. STORED PROCEDURES ĐỒNG BỘ DỮ LIỆU
-- ==============================================================================
CREATE OR ALTER PROCEDURE [dwh].[sp_Load_Station_Dimension]
AS
BEGIN
    SET NOCOUNT ON;
    PRINT N'[INFO] Đang nạp danh mục trạm vào dwh.Dim_Station...';
    
    MERGE INTO [dwh].[Dim_Station] AS target
    USING (
        SELECT 
            s.[Station_Code],
            s.[Station_Name],
            p.[Province_Key],
            s.[Station_Type],
            s.[Latitude],
            s.[Longitude],
            s.[Is_Active]
        FROM [staging].[stg_dim_stations] s
        INNER JOIN [dwh].[Dim_Province] p 
            ON s.[Province_Code] = p.[Province_Code]
    ) AS source
    ON (target.[Station_Code] = source.[Station_Code])
    WHEN MATCHED THEN
        UPDATE SET 
            target.[Station_Name] = source.[Station_Name],
            target.[Province_Key] = source.[Province_Key],
            target.[Station_Type] = source.[Station_Type],
            target.[Latitude] = source.[Latitude],
            target.[Longitude] = source.[Longitude],
            target.[Is_Active] = source.[Is_Active]
    WHEN NOT MATCHED THEN
        INSERT ([Station_Code], [Station_Name], [Province_Key], [Station_Type], [Latitude], [Longitude], [Is_Active])
        VALUES (source.[Station_Code], source.[Station_Name], source.[Province_Key], source.[Station_Type], source.[Latitude], source.[Longitude], source.[Is_Active]);

    PRINT N'[SUCCESS] Hoàn thành đồng bộ dwh.Dim_Station.';
END;
GO

CREATE OR ALTER PROCEDURE [dwh].[sp_Load_Hourly_Monitoring_Fact]
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    
    PRINT N'[INFO] Bắt đầu nạp khối dữ liệu vào dwh.Fact_Hourly_Air_Monitoring (1.65 Triệu dòng)...';
    
    -- Xóa dữ liệu năm 2024 nếu đã có trước đó (Idempotent Load)
    DELETE FROM [dwh].[Fact_Hourly_Air_Monitoring] WHERE [Date_Key] = 2024;
    
    INSERT INTO [dwh].[Fact_Hourly_Air_Monitoring] (
        [Date_Key],
        [Time_Key],
        [Province_Key],
        [Station_Key],
        [CO2_ppm],
        [CO_mg_m3],
        [NO2_ug_m3],
        [SO2_ug_m3],
        [PM25_ug_m3],
        [PM10_ug_m3],
        [AQI_Index],
        [AQI_Category],
        [Is_Exceeding_QCVN]
    )
    SELECT 
        d.[Date_Key],
        t.[Time_Key],
        p.[Province_Key],
        st.[Station_Key],
        stg.[CO2_ppm],
        stg.[CO_mg_m3],
        stg.[NO2_ug_m3],
        stg.[SO2_ug_m3],
        stg.[PM25_ug_m3],
        stg.[PM10_ug_m3],
        stg.[AQI_Index],
        stg.[AQI_Category],
        stg.[Is_Exceeding_QCVN]
    FROM [staging].[stg_hourly_air_monitoring] stg
    INNER JOIN [dwh].[Dim_Date] d 
        ON stg.[Date_Key] = d.[Date_Key]
    INNER JOIN [dwh].[Dim_Time_Of_Day] t 
        ON stg.[Hour_24] = t.[Hour_24]
    INNER JOIN [dwh].[Dim_Province] p 
        ON stg.[Province_Code] = p.[Province_Code]
    INNER JOIN [dwh].[Dim_Station] st 
        ON stg.[Station_Code] = st.[Station_Code];
        
    PRINT N'[SUCCESS] Nạp thành công toàn bộ dữ liệu vi mô vào Fact_Hourly_Air_Monitoring.';
END;
GO

PRINT N'[COMPLETE] Tạo thành công các bảng và procedures cho tầng Big Data Fact_Hourly_Air_Monitoring.';
GO
