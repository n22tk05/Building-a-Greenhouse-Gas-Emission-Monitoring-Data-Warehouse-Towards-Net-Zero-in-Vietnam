-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 1 (Week 4) - Semantic Layer & SQL BI Views (DirectQuery / Import Mode)
-- File: sql/05_create_bi_views.sql
-- Description: Định nghĩa các Views ngữ nghĩa chuẩn hóa cho Power BI, bảo vệ kép
--              chống tính trùng lặp GDP (Overcounting Guard), hỗ trợ DirectQuery.
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. VIEW CHIỀU THỜI GIAN: dwh.vw_Dim_Date_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Dim_Date_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Dim_Date_BI]
AS
SELECT 
    d.[Date_Key],
    d.[Year],
    d.[Decade],
    d.[Five_Year_Plan_Phase],
    d.[Is_Target_Milestone],
    -- Trường ngày giả lập phục vụ các hàm Time Intelligence trong DAX (DATE format)
    DATEFROMPARTS(d.[Year], 12, 31) AS [Year_Date],
    -- Phân loại thời kỳ lịch sử & mốc chính sách
    CASE 
        WHEN d.[Year] < 1986 THEN N'Trước Đổi Mới (Trước 1986)'
        WHEN d.[Year] BETWEEN 1986 AND 2020 THEN N'Thời kỳ Đổi Mới & Công nghiệp hóa'
        WHEN d.[Year] BETWEEN 2021 AND 2030 THEN N'Thập kỷ Hành động NDC 2030'
        ELSE N'Lộ trình Chuyển dịch Net-Zero 2050'
    END AS [Policy_Period],
    CASE WHEN d.[Year] < 1986 THEN 1 ELSE 0 END AS [Is_Pre_DoiMoi],
    CASE WHEN d.[Year] >= 1986 THEN 1 ELSE 0 END AS [Is_DoiMoi_Era],
    CASE WHEN d.[Year] IN (2030, 2050) THEN 1 ELSE 0 END AS [Is_NetZero_Milestone]
FROM [dwh].[Dim_Date] d;
GO

-- ==============================================================================
-- 2. VIEW CHIỀU ĐỊA LÝ: dwh.vw_Dim_Province_Geo_BI (63 Tỉnh thành)
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Dim_Province_Geo_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Dim_Province_Geo_BI]
AS
SELECT 
    p.[Province_Key],
    p.[Province_Code], -- Giữ nguyên kiểu VARCHAR(10) có số '0' ở đầu ('01' đến '96')
    p.[Province_Name],
    p.[Province_Name_Ascii], -- Trùng khớp với id/name trong file TopoJSON Vietnam Map
    p.[Region],
    p.[Economic_Zone],
    p.[Area_Km2],
    p.[Is_Industrial_Hub],
    CASE WHEN p.[Is_Industrial_Hub] = 1 THEN N'Cực tăng trưởng công nghiệp' ELSE N'Khu vực thông thường' END AS [Industrial_Hub_Label],
    -- Tọa độ trung tâm phục vụ Map visuals trong trường hợp không dùng TopoJSON
    CASE p.[Region]
        WHEN N'Đồng bằng sông Hồng' THEN N'Miền Bắc'
        WHEN N'Trung du và miền núi phía Bắc' THEN N'Miền Bắc'
        WHEN N'Bắc Trung Bộ và Duyên hải miền Trung' THEN N'Miền Trung'
        WHEN N'Tây Nguyên' THEN N'Miền Trung'
        WHEN N'Đông Nam Bộ' THEN N'Miền Nam'
        WHEN N'Đồng bằng sông Cửu Long' THEN N'Miền Nam'
        ELSE N'Khác'
    END AS [Macro_Region]
FROM [dwh].[Dim_Province] p;
GO

-- ==============================================================================
-- 3. VIEW CHIỀU LĨNH VỰC PHÁT THẢI: dwh.vw_Dim_Sector_Hierarchy_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Dim_Sector_Hierarchy_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Dim_Sector_Hierarchy_BI]
AS
SELECT 
    s.[Sector_Key],
    s.[Sector_Code],
    s.[Sector_Name_EN],
    s.[Sector_Name_VI],
    s.[Sector_Category],
    COALESPECS.[Scope_Type],
    -- Cấu trúc phân cấp phục vụ visual Matrix và Sunburst
    COALESPECS.[Scope_Type] + N' > ' + s.[Sector_Category] + N' > ' + s.[Sector_Name_VI] AS [Sector_Hierarchy_Path],
    CASE WHEN s.[Sector_Code] = 'TOT' THEN 1 ELSE 0 END AS [Is_Total_Sector]
FROM [dwh].[Dim_Sector] s
CROSS APPLY (
    SELECT ISNULL(s.[Scope_Type], 'Scope 1 & 2') AS [Scope_Type]
) COALESPECS;
GO

-- ==============================================================================
-- 4. VIEW SỰ KIỆN PHÁT THẢI QUỐC GIA: dwh.vw_Fact_National_Emissions_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Fact_National_Emissions_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Fact_National_Emissions_BI]
AS
SELECT 
    f.[Emission_ID],
    f.[Date_Key],
    d.[Year],
    d.[Decade],
    d.[Five_Year_Plan_Phase],
    f.[Sector_Key],
    s.[Sector_Code],
    s.[Sector_Name_VI],
    s.[Sector_Category],
    ISNULL(s.[Scope_Type], 'Scope 1 & 2') AS [Scope_Type],
    f.[Gas],
    f.[Emissions_MtCO2e],
    f.[CO2_MtCO2e],
    f.[Methane_MtCO2e],
    f.[Renewable_Energy_Pct],
    
    -- ==========================================================================
    -- GDP OVERCOUNTING GUARD:
    -- Khẳng định GDP chỉ xuất hiện khi Sector_Code = 'TOT' (Tổng quốc gia).
    -- Khi người dùng lọc từng phân ngành hoặc nhóm ngành, SUM(GDP_USD) trên View
    -- KHÔNG BAO GIỜ bị cộng dồn nhân lên 9 lần.
    -- ==========================================================================
    CASE 
        WHEN s.[Sector_Code] = 'TOT' THEN f.[GDP_USD]
        ELSE NULL 
    END AS [GDP_USD],
    f.[GDP_USD] AS [Raw_GDP_USD_Unsafe] -- Giữ lại trường gốc để đối soát kỹ thuật
FROM [dwh].[Fact_National_Emissions] f
INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Sector] s ON f.[Sector_Key] = s.[Sector_Key];
GO

-- ==============================================================================
-- 5. VIEW SỰ KIỆN KINH TẾ & PHÁT THẢI TỈNH: dwh.vw_Fact_Provincial_Economy_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Fact_Provincial_Economy_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Fact_Provincial_Economy_BI]
AS
SELECT 
    f.[Economy_ID],
    f.[Date_Key],
    d.[Year],
    d.[Decade],
    f.[Province_Key],
    p.[Province_Code],
    p.[Province_Name],
    p.[Province_Name_Ascii],
    p.[Region],
    p.[Economic_Zone],
    p.[Area_Km2],
    p.[Is_Industrial_Hub],
    f.[GRDP_Billion_VND],
    f.[Population],
    f.[Industrial_Output_Billion_VND],
    f.[Forest_Coverage_Pct],
    f.[Estimated_Carbon_Tonnes],
    f.[Decoupling_Index],
    
    -- Phân loại trạng thái tách rời kinh tế - carbon (Tapio Decoupling Model)
    CASE 
        WHEN f.[Decoupling_Index] < 0 THEN N'Tách rời mạnh (Strong Decoupling)'
        WHEN f.[Decoupling_Index] BETWEEN 0 AND 0.8 THEN N'Tách rời yếu (Weak Decoupling)'
        WHEN f.[Decoupling_Index] BETWEEN 0.8 AND 1.2 THEN N'Mở rộng đồng tốc (Expansive Coupling)'
        ELSE N'Tăng trưởng thâm dụng carbon (Negative Decoupling)'
    END AS [Decoupling_Status],

    -- Chỉ số cường độ carbon tính sẵn tại tầng View
    CAST(
        CASE 
            WHEN f.[GRDP_Billion_VND] > 0 
            THEN f.[Estimated_Carbon_Tonnes] / f.[GRDP_Billion_VND]
            ELSE 0 
        END AS DECIMAL(18, 4)
    ) AS [Carbon_Intensity_Tonnes_Per_Billion_VND],

    CAST(
        CASE 
            WHEN f.[Population] > 0 
            THEN f.[Estimated_Carbon_Tonnes] / f.[Population]
            ELSE 0 
        END AS DECIMAL(18, 4)
    ) AS [Carbon_Per_Capita_Tonnes],

    CAST(
        CASE 
            WHEN p.[Area_Km2] > 0 
            THEN f.[Estimated_Carbon_Tonnes] / p.[Area_Km2]
            ELSE 0 
        END AS DECIMAL(18, 4)
    ) AS [Carbon_Density_Tonnes_Per_Km2]
FROM [dwh].[Fact_Provincial_Economy] f
INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Province] p ON f.[Province_Key] = p.[Province_Key];
GO

-- ==============================================================================
-- 6. VIEW CHIỀU TRẠM QUAN TRẮC: dwh.vw_Dim_Station_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Dim_Station_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Dim_Station_BI]
AS
SELECT 
    s.[Station_Key],
    s.[Station_Code],
    s.[Station_Name],
    s.[Province_Key],
    p.[Province_Code],
    p.[Province_Name],
    p.[Region],
    p.[Economic_Zone],
    s.[Station_Type],
    s.[Latitude],
    s.[Longitude],
    s.[Is_Active]
FROM [dwh].[Dim_Station] s
INNER JOIN [dwh].[Dim_Province] p ON s.[Province_Key] = p.[Province_Key];
GO

-- ==============================================================================
-- 7. VIEW CHIỀU THỜI GIAN TRONG NGÀY: dwh.vw_Dim_Time_Of_Day_BI
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Dim_Time_Of_Day_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Dim_Time_Of_Day_BI]
AS
SELECT 
    t.[Time_Key],
    t.[Hour_24],
    t.[Hour_Label],
    t.[Time_Bucket],
    t.[Is_Rush_Hour],
    CASE WHEN t.[Is_Rush_Hour] = 1 THEN N'Giờ Cao Điểm' ELSE N'Giờ Bình Thường' END AS [Rush_Hour_Label]
FROM [dwh].[Dim_Time_Of_Day] t;
GO

-- ==============================================================================
-- 8. VIEW SỰ KIỆN QUAN TRẮC KHÔNG KHÍ BIG DATA: dwh.vw_Fact_Hourly_Air_Monitoring_BI
-- Phục vụ Dashboard 3 - Giám sát 1.66 Triệu dòng thời gian thực 2024
-- ==============================================================================
PRINT N'[INFO] Đang tạo View dwh.vw_Fact_Hourly_Air_Monitoring_BI...';
GO
CREATE OR ALTER VIEW [dwh].[vw_Fact_Hourly_Air_Monitoring_BI]
AS
SELECT 
    f.[Monitoring_ID],
    f.[Date_Key],
    d.[Year],
    f.[Time_Key],
    t.[Hour_24],
    t.[Hour_Label],
    t.[Time_Bucket],
    t.[Is_Rush_Hour],
    f.[Province_Key],
    p.[Province_Code],
    p.[Province_Name],
    p.[Region],
    f.[Station_Key],
    s.[Station_Code],
    s.[Station_Name],
    s.[Station_Type],
    s.[Latitude],
    s.[Longitude],
    f.[CO2_ppm],
    f.[CO_mg_m3],
    f.[NO2_ug_m3],
    f.[SO2_ug_m3],
    f.[PM25_ug_m3],
    f.[PM10_ug_m3],
    f.[AQI_Index],
    f.[AQI_Category],
    f.[Is_Exceeding_QCVN],
    CASE WHEN f.[Is_Exceeding_QCVN] = 1 THEN N'Vượt chuẩn QCVN 05:2023' ELSE N'Đạt chuẩn an toàn' END AS [QCVN_Compliance_Label]
FROM [dwh].[Fact_Hourly_Air_Monitoring] f
INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Time_Of_Day] t ON f.[Time_Key] = t.[Time_Key]
INNER JOIN [dwh].[Dim_Province] p ON f.[Province_Key] = p.[Province_Key]
INNER JOIN [dwh].[Dim_Station] s ON f.[Station_Key] = s.[Station_Key];
GO

PRINT N'[COMPLETE] Đã tạo thành công 8 BI Semantic Views trong schema [dwh].';
GO
