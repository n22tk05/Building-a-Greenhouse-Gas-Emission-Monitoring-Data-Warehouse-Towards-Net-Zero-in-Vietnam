-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 4 - Dimension Seeding
-- File: sql/03_seed_dimensions.sql
-- Description: Nạp dữ liệu nền cho Dim_Date (1970–2050), Dim_Province (63 tỉnh), Dim_Sector
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. NẠP DỮ LIỆU BẢNG THỜI GIAN (dwh.Dim_Date: 1970 – 2050 = 81 Năm)
-- ==============================================================================
PRINT N'[INFO] Bắt đầu nạp dữ liệu nền cho dwh.Dim_Date (1970 - 2050)...';

;WITH YearSequence AS (
    SELECT 1970 AS [Year]
    UNION ALL
    SELECT [Year] + 1 FROM YearSequence WHERE [Year] < 2050
)
MERGE INTO [dwh].[Dim_Date] AS target
USING (
    SELECT 
        [Year] AS [Date_Key],
        [Year],
        CAST(([Year] / 10) * 10 AS VARCHAR(10)) + 's' AS [Decade],
        CASE 
            WHEN [Year] < 1976 THEN N'Giai đoạn trước 1976'
            WHEN [Year] BETWEEN 1976 AND 1980 THEN N'Kế hoạch 5 năm lần II (1976-1980)'
            WHEN [Year] BETWEEN 1981 AND 1985 THEN N'Kế hoạch 5 năm lần III (1981-1985)'
            WHEN [Year] BETWEEN 1986 AND 1990 THEN N'Kế hoạch 5 năm lần IV - Đổi mới (1986-1990)'
            WHEN [Year] BETWEEN 1991 AND 1995 THEN N'Kế hoạch 5 năm 1991-1995'
            WHEN [Year] BETWEEN 1996 AND 2000 THEN N'Kế hoạch 5 năm 1996-2000'
            WHEN [Year] BETWEEN 2001 AND 2005 THEN N'Kế hoạch 5 năm 2001-2005'
            WHEN [Year] BETWEEN 2006 AND 2010 THEN N'Kế hoạch 5 năm 2006-2010'
            WHEN [Year] BETWEEN 2011 AND 2015 THEN N'Kế hoạch 5 năm 2011-2015'
            WHEN [Year] BETWEEN 2016 AND 2020 THEN N'Kế hoạch 5 năm 2016-2020'
            WHEN [Year] BETWEEN 2021 AND 2025 THEN N'Kế hoạch 5 năm 2021-2025'
            WHEN [Year] BETWEEN 2026 AND 2030 THEN N'Kế hoạch 5 năm 2026-2030 (NDC Milestone)'
            WHEN [Year] BETWEEN 2031 AND 2035 THEN N'Kế hoạch 5 năm 2031-2035'
            WHEN [Year] BETWEEN 2036 AND 2040 THEN N'Kế hoạch 5 năm 2036-2040'
            WHEN [Year] BETWEEN 2041 AND 2045 THEN N'Kế hoạch 5 năm 2041-2045'
            ELSE N'Kế hoạch 5 năm 2046-2050 (Net-Zero Target)'
        END AS [Five_Year_Plan_Phase],
        CASE 
            WHEN [Year] IN (2030, 2050) THEN 1 
            ELSE 0 
        END AS [Is_Target_Milestone]
    FROM YearSequence
) AS source
ON (target.[Date_Key] = source.[Date_Key])
WHEN MATCHED THEN
    UPDATE SET 
        target.[Decade] = source.[Decade],
        target.[Five_Year_Plan_Phase] = source.[Five_Year_Plan_Phase],
        target.[Is_Target_Milestone] = source.[Is_Target_Milestone]
WHEN NOT MATCHED THEN
    INSERT ([Date_Key], [Year], [Decade], [Five_Year_Plan_Phase], [Is_Target_Milestone])
    VALUES (source.[Date_Key], source.[Year], source.[Decade], source.[Five_Year_Plan_Phase], source.[Is_Target_Milestone])
OPTION (MAXRECURSION 100);

PRINT N'[SUCCESS] Nạp thành công dữ liệu dwh.Dim_Date.';
GO

-- ==============================================================================
-- 2. NẠP DỮ LIỆU DANH MỤC PHÂN NGÀNH PHÁT THẢI IPCC (dwh.Dim_Sector)
-- ==============================================================================
PRINT N'[INFO] Bắt đầu nạp danh mục ngành chuẩn vào dwh.Dim_Sector...';

MERGE INTO [dwh].[Dim_Sector] AS target
USING (
    VALUES
        ('AGR', 'Agriculture', N'Nông nghiệp & Trồng lúa nước', N'Agriculture', 'Scope 1'),
        ('BLD', 'Building', N'Tòa nhà & Dân dụng', N'Building', 'Scope 1/2'),
        ('ELE', 'Electricity/Heat', N'Sản xuất Điện & Nhiệt', N'Energy', 'Scope 1'),
        ('ENG', 'Energy', N'Năng lượng & Khai khoáng', N'Energy', 'Scope 1'),
        ('IND', 'Manufacturing/Construction', N'Công nghiệp Chế biến & Xây dựng', N'Industry', 'Scope 1/2'),
        ('TRA', 'Transportation', N'Giao thông Vận tải', N'Transportation', 'Scope 1'),
        ('WAS', 'Waste', N'Chất thải & Xử lý nước thải', N'Waste', 'Scope 1'),
        ('OTH', 'Other Fuel Combustion', N'Sử dụng Nhiên liệu khác', N'Other', 'Scope 1'),
        ('TOT', 'Total National Emissions', N'Tổng phát thải toàn quốc', N'National Total', 'Scope 1/2/3')
) AS source ([Sector_Code], [Sector_Name_EN], [Sector_Name_VI], [Sector_Category], [Scope_Type])
ON (target.[Sector_Code] = source.[Sector_Code])
WHEN MATCHED THEN
    UPDATE SET 
        target.[Sector_Name_EN] = source.[Sector_Name_EN],
        target.[Sector_Name_VI] = source.[Sector_Name_VI],
        target.[Sector_Category] = source.[Sector_Category],
        target.[Scope_Type] = source.[Scope_Type]
WHEN NOT MATCHED THEN
    INSERT ([Sector_Code], [Sector_Name_EN], [Sector_Name_VI], [Sector_Category], [Scope_Type])
    VALUES (source.[Sector_Code], source.[Sector_Name_EN], source.[Sector_Name_VI], source.[Sector_Category], source.[Scope_Type]);

PRINT N'[SUCCESS] Nạp thành công danh mục phân ngành dwh.Dim_Sector.';
GO

-- ==============================================================================
-- 3. NẠP DỮ LIỆU 63 TỈNH THÀNH (dwh.Dim_Province) TỪ STAGING HOẶC CATALOG
-- ==============================================================================
PRINT N'[INFO] Đồng bộ danh mục 63 tỉnh thành vào dwh.Dim_Province...';

IF EXISTS (SELECT 1 FROM [staging].[stg_dim_provinces])
BEGIN
    MERGE INTO [dwh].[Dim_Province] AS target
    USING [staging].[stg_dim_provinces] AS source
    ON (target.[Province_Code] = source.[Province_Code])
    WHEN MATCHED THEN
        UPDATE SET 
            target.[Province_Name] = source.[Province_Name],
            target.[Province_Name_Ascii] = source.[Province_Name_Ascii],
            target.[Region] = source.[Region],
            target.[Economic_Zone] = source.[Economic_Zone],
            target.[Area_Km2] = ISNULL(source.[Area_Km2], target.[Area_Km2]),
            target.[Is_Industrial_Hub] = ISNULL(source.[Is_Industrial_Hub], target.[Is_Industrial_Hub])
    WHEN NOT MATCHED THEN
        INSERT ([Province_Code], [Province_Name], [Province_Name_Ascii], [Region], [Economic_Zone], [Area_Km2], [Is_Industrial_Hub])
        VALUES (source.[Province_Code], source.[Province_Name], source.[Province_Name_Ascii], source.[Region], source.[Economic_Zone], ISNULL(source.[Area_Km2], 0), ISNULL(source.[Is_Industrial_Hub], 0));

    PRINT N'[SUCCESS] Đã nạp ' + CAST(@@ROWCOUNT AS NVARCHAR(10)) + N' tỉnh thành từ staging.stg_dim_provinces vào dwh.Dim_Province.';
END
ELSE
BEGIN
    PRINT N'[WARNING] Bảng staging.stg_dim_provinces hiện chưa có dữ liệu. Bảng dwh.Dim_Province sẽ được nạp trong chu trình ETL SSIS.';
END
GO

PRINT N'[COMPLETE] Hoàn thành nạp dữ liệu nền cho các Dimension.';
GO
