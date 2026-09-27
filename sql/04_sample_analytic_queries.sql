-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 5 - Sample Analytical KPI Queries
-- File: sql/04_sample_analytic_queries.sql
-- Description: 3+ câu truy vấn SQL phân tích nghiệp vụ thực chiến phục vụ Power BI
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- TRUY VẤN 1: Top 10 Tỉnh Phát Thải Cao Nhất Kèm Chỉ Số Decoupling (Provincial Decoupling)
-- Mục đích: Phục vụ Bảng xếp hạng và Thẻ cảnh báo sớm trên Trang 2 của Power BI
-- Logic nghiệp vụ: Lấy năm mới nhất có số liệu GSO (2024), sắp xếp theo lượng carbon
-- ==============================================================================
PRINT N'--- [TRUY VẤN 1] TOP 10 TỈNH PHÁT THẢI CARBON CAO NHẤT VÀ CHỈ SỐ DECOUPLING ---';
GO

WITH LatestYear AS (
    SELECT MAX(d.[Year]) AS [Max_Year]
    FROM [dwh].[Fact_Provincial_Economy] f
    INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
)
SELECT TOP 10
    d.[Year],
    p.[Province_Code],
    p.[Province_Name],
    p.[Region],
    p.[Economic_Zone],
    p.[Is_Industrial_Hub],
    f.[Estimated_Carbon_Tonnes] AS [Carbon_Tonnes],
    f.[GRDP_Billion_VND] AS [GRDP_Billion_VND],
    f.[Decoupling_Index],
    CASE 
        WHEN f.[Decoupling_Index] >= 100 THEN N'Kinh tế Tăng trưởng Xanh (Decoupled)'
        WHEN f.[Decoupling_Index] >= 70 THEN N'Tăng trưởng trung gian'
        ELSE N'Thâm dụng Carbon cao (Risk Area)'
    END AS [Decoupling_Status],
    DENSE_RANK() OVER (ORDER BY f.[Estimated_Carbon_Tonnes] DESC) AS [Emission_Rank]
FROM [dwh].[Fact_Provincial_Economy] f
INNER JOIN [dwh].[Dim_Date] d 
    ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Province] p 
    ON f.[Province_Key] = p.[Province_Key]
CROSS JOIN LatestYear ly
WHERE d.[Year] = ly.[Max_Year]
ORDER BY f.[Estimated_Carbon_Tonnes] DESC;
GO

-- ==============================================================================
-- TRUY VẤN 2: Xu Hướng Chuyển Dịch Năng Lượng & Cường Độ Carbon Quốc Gia Qua Các Thập Kỷ
-- Mục đích: Phục vụ biểu đồ đường đôi (Dual-axis Line Chart) tương quan trên Trang 1 Power BI
-- Logic nghiệp vụ: Gom nhóm theo Thập kỷ, tính tỷ lệ NLTT bình quân và cường độ phát thải
-- ==============================================================================
PRINT N'--- [TRUY VẤN 2] XU HƯỚNG TƯƠNG QUAN NĂNG LƯỢNG TÁI TẠO & CƯỜNG ĐỘ PHÁT THẢI CO2 ---';
GO

SELECT 
    d.[Decade],
    COUNT(DISTINCT d.[Year]) AS [Years_Count],
    ROUND(AVG(f.[Renewable_Energy_Pct]), 2) AS [Avg_Renewable_Pct],
    ROUND(SUM(f.[CO2_MtCO2e]), 2) AS [Total_CO2_MtCO2e],
    ROUND(AVG(f.[GDP_USD]) / 1000000000.0, 2) AS [Avg_GDP_Billion_USD],
    -- Cường độ Carbon trên GDP: Tấn CO2 trên 1.000 USD GDP
    ROUND(
        CASE 
            WHEN AVG(f.[GDP_USD]) > 0 
            THEN (SUM(f.[CO2_MtCO2e]) * 1000000.0) / (AVG(f.[GDP_USD]) / 1000.0) 
            ELSE 0 
        END, 4
    ) AS [Carbon_Intensity_Tonnes_Per_1k_USD]
FROM [dwh].[Fact_National_Emissions] f
INNER JOIN [dwh].[Dim_Date] d 
    ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Sector] s 
    ON f.[Sector_Key] = s.[Sector_Key]
WHERE s.[Sector_Code] = 'TOT'
GROUP BY d.[Decade]
ORDER BY d.[Decade];
GO

-- ==============================================================================
-- TRUY VẤN 3: Cơ Cấu & Tăng Trưởng Phát Thải Theo Ngành Qua Các Kế Hoạch 5 Năm
-- Mục đích: Phục vụ biểu đồ Donut / Tree-Map trên Trang 1 của Power BI
-- Logic nghiệp vụ: Tính tổng phát thải của từng phân ngành kinh tế theo từng giai đoạn 5 năm
-- ==============================================================================
PRINT N'--- [TRUY VẤN 3] PHÁT THẢI PHÂN BỔ THEO NGÀNH VÀ KẾ HOẠCH 5 NĂM QUỐC GIA ---';
GO

SELECT 
    d.[Five_Year_Plan_Phase],
    s.[Sector_Category],
    s.[Sector_Name_VI],
    ROUND(SUM(f.[Emissions_MtCO2e]), 2) AS [Period_Total_Emissions_MtCO2e],
    ROUND(AVG(f.[Emissions_MtCO2e]), 2) AS [Annual_Avg_Emissions_MtCO2e],
    ROUND(
        100.0 * SUM(f.[Emissions_MtCO2e]) / 
        NULLIF(SUM(SUM(f.[Emissions_MtCO2e])) OVER (PARTITION BY d.[Five_Year_Plan_Phase]), 0), 
        2
    ) AS [Sector_Contribution_Pct]
FROM [dwh].[Fact_National_Emissions] f
INNER JOIN [dwh].[Dim_Date] d 
    ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Sector] s 
    ON f.[Sector_Key] = s.[Sector_Key]
WHERE s.[Sector_Code] <> 'TOT' -- Loại trừ dòng tổng để tính tỷ trọng chính xác
  AND f.[Gas] = 'All GHG'     -- Tránh cộng gộp các loại khí đơn lẻ (CO2, CH4, N2O)
  AND d.[Year] >= 1990        -- Dữ liệu phân ngành ClimateWatch khả dụng từ 1990
GROUP BY 
    d.[Five_Year_Plan_Phase], 
    s.[Sector_Category], 
    s.[Sector_Name_VI]
ORDER BY 
    d.[Five_Year_Plan_Phase], 
    [Period_Total_Emissions_MtCO2e] DESC;
GO

-- ==============================================================================
-- TRUY VẤN 4 (BONUS): Ma Trận Phân Nhóm 4 Góc Phần Tư Tỉnh Thành (Growth vs Carbon)
-- Mục đích: Cung cấp tập dữ liệu trực tiếp cho Biểu đồ Scatter Plot trên Trang 2 Power BI
-- ==============================================================================
PRINT N'--- [TRUY VẤN 4] PHÂN NHÓM 4 GÓC PHẦN TƯ (GROWTH VS CARBON INTENSITY) ---';
GO

WITH Benchmark AS (
    SELECT 
        AVG(f.[GRDP_Billion_VND]) AS [National_Avg_GRDP],
        AVG(f.[Estimated_Carbon_Tonnes]) AS [National_Avg_Carbon]
    FROM [dwh].[Fact_Provincial_Economy] f
    INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
    WHERE d.[Year] = 2024
)
SELECT 
    p.[Province_Code],
    p.[Province_Name],
    p.[Region],
    f.[GRDP_Billion_VND],
    f.[Estimated_Carbon_Tonnes],
    f.[Decoupling_Index],
    CASE 
        WHEN f.[GRDP_Billion_VND] >= b.[National_Avg_GRDP] AND f.[Estimated_Carbon_Tonnes] < b.[National_Avg_Carbon]
            THEN N'Góc I: Tiên phong Xanh (Kinh tế cao, Phát thải thấp)'
        WHEN f.[GRDP_Billion_VND] >= b.[National_Avg_GRDP] AND f.[Estimated_Carbon_Tonnes] >= b.[National_Avg_Carbon]
            THEN N'Góc II: Cần Chuyển dịch (Kinh tế cao, Phát thải cao)'
        WHEN f.[GRDP_Billion_VND] < b.[National_Avg_GRDP] AND f.[Estimated_Carbon_Tonnes] >= b.[National_Avg_Carbon]
            THEN N'Góc III: Rủi ro cao (Kinh tế thấp, Phát thải cao)'
        ELSE N'Góc IV: Đang phát triển (Kinh tế thấp, Phát thải thấp)'
    END AS [Quadrant_Classification]
FROM [dwh].[Fact_Provincial_Economy] f
INNER JOIN [dwh].[Dim_Date] d ON f.[Date_Key] = d.[Date_Key]
INNER JOIN [dwh].[Dim_Province] p ON f.[Province_Key] = p.[Province_Key]
CROSS JOIN Benchmark b
WHERE d.[Year] = 2024
ORDER BY f.[GRDP_Billion_VND] DESC;
GO
