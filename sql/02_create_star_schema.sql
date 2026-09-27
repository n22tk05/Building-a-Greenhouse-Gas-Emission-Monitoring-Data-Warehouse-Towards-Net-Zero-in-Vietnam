-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 3 - Star Schema DDL (Dimensions & Fact Tables)
-- File: sql/02_create_star_schema.sql
-- Description: Tạo 3 bảng Dimension chuẩn tắc và 2 bảng Fact theo chuẩn Kimball
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. XÓA CÁC BẢNG THEO THỨ TỰ PHỤ THUỘC KHÓA NGOẠI (Fact trước, Dim sau)
-- ==============================================================================
IF OBJECT_ID(N'dwh.Fact_National_Emissions', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Fact_National_Emissions cũ...';
    DROP TABLE [dwh].[Fact_National_Emissions];
END
GO

IF OBJECT_ID(N'dwh.Fact_Provincial_Economy', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Fact_Provincial_Economy cũ...';
    DROP TABLE [dwh].[Fact_Provincial_Economy];
END
GO

IF OBJECT_ID(N'dwh.Dim_Date', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Dim_Date cũ...';
    DROP TABLE [dwh].[Dim_Date];
END
GO

IF OBJECT_ID(N'dwh.Dim_Province', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Dim_Province cũ...';
    DROP TABLE [dwh].[Dim_Province];
END
GO

IF OBJECT_ID(N'dwh.Dim_Sector', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng dwh.Dim_Sector cũ...';
    DROP TABLE [dwh].[Dim_Sector];
END
GO

-- ==============================================================================
-- 2. TẠO CÁC BẢNG DIMENSION CHUẨN TẮC (Conformed & Specialized Dimensions)
-- ==============================================================================

-- 2.1. Dim_Date: Chiều thời gian dùng chung (Conformed Dimension)
PRINT N'[INFO] Đang tạo bảng dwh.Dim_Date...';
CREATE TABLE [dwh].[Dim_Date] (
    [Date_Key]              INT             NOT NULL, -- Smart Surrogate Key (YYYY)
    [Year]                  INT             NOT NULL,
    [Decade]                VARCHAR(20)     NOT NULL, -- VD: '2020s'
    [Five_Year_Plan_Phase]  NVARCHAR(50)    NOT NULL, -- VD: N'Kế hoạch 2021-2025'
    [Is_Target_Milestone]   BIT             NOT NULL DEFAULT 0, -- 1 cho năm 2030 (NDC) và 2050 (Net-Zero)
    CONSTRAINT [PK_Dim_Date] PRIMARY KEY CLUSTERED ([Date_Key]),
    CONSTRAINT [UQ_Dim_Date_Year] UNIQUE ([Year])
);
GO

-- 2.2. Dim_Province: Chiều địa lý hành chính 63 tỉnh thành Việt Nam
PRINT N'[INFO] Đang tạo bảng dwh.Dim_Province...';
CREATE TABLE [dwh].[Dim_Province] (
    [Province_Key]          INT IDENTITY(1,1) NOT NULL, -- Surrogate Key tự tăng
    [Province_Code]         VARCHAR(10)       NOT NULL, -- Mã chuẩn GSO (giữ số 0 ở đầu)
    [Province_Name]         NVARCHAR(100)     NOT NULL, -- Tên tỉnh có dấu tiếng Việt
    [Province_Name_Ascii]   VARCHAR(100)      NOT NULL, -- Tên không dấu khớp TopoJSON map
    [Region]                NVARCHAR(50)      NOT NULL, -- Vùng địa lý sinh thái
    [Economic_Zone]         NVARCHAR(100)     NOT NULL, -- Vùng kinh tế trọng điểm
    [Area_Km2]              DECIMAL(10, 2)    NOT NULL, -- Diện tích tự nhiên
    [Is_Industrial_Hub]     BIT               NOT NULL DEFAULT 0, -- Cờ cực tăng trưởng công nghiệp
    CONSTRAINT [PK_Dim_Province] PRIMARY KEY CLUSTERED ([Province_Key]),
    CONSTRAINT [UQ_Dim_Province_Code] UNIQUE ([Province_Code])
);
GO

-- 2.3. Dim_Sector: Chiều lĩnh vực phát thải theo phân loại IPCC / ClimateWatch
PRINT N'[INFO] Đang tạo bảng dwh.Dim_Sector...';
CREATE TABLE [dwh].[Dim_Sector] (
    [Sector_Key]            INT IDENTITY(1,1) NOT NULL, -- Surrogate Key tự tăng
    [Sector_Code]           VARCHAR(20)       NOT NULL, -- Mã ngành chuẩn IPCC/CW (VD: 'ELE', 'AGR')
    [Sector_Name_EN]        VARCHAR(100)      NOT NULL, -- Tên tiếng Anh
    [Sector_Name_VI]        NVARCHAR(150)     NOT NULL, -- Tên tiếng Việt
    [Sector_Category]       NVARCHAR(50)      NOT NULL, -- Nhóm ngành lớn (Energy, Agriculture...)
    [Scope_Type]            VARCHAR(20)       NULL,     -- Phân loại Scope 1 / Scope 2
    CONSTRAINT [PK_Dim_Sector] PRIMARY KEY CLUSTERED ([Sector_Key]),
    CONSTRAINT [UQ_Dim_Sector_Code] UNIQUE ([Sector_Code])
);
GO

-- ==============================================================================
-- 3. TẠO CÁC BẢNG SỰ KIỆN (Fact Tables)
-- ==============================================================================

-- 3.1. Fact_National_Emissions: Phát thải khí nhà kính và năng lượng cấp quốc gia
-- Grain: 1 dòng cho 1 lĩnh vực, 1 loại khí trong 1 năm tại Việt Nam
PRINT N'[INFO] Đang tạo bảng dwh.Fact_National_Emissions...';
CREATE TABLE [dwh].[Fact_National_Emissions] (
    [Emission_ID]           BIGINT IDENTITY(1,1) NOT NULL,
    [Date_Key]              INT                  NOT NULL,
    [Sector_Key]            INT                  NOT NULL,
    [Gas]                   VARCHAR(20)          NOT NULL, -- 'All GHG', 'CO2', 'CH4'
    [Emissions_MtCO2e]      DECIMAL(18, 4)       NOT NULL, -- Triệu tấn CO2e
    [CO2_MtCO2e]            DECIMAL(18, 4)       NULL,     -- Triệu tấn CO2
    [Methane_MtCO2e]        DECIMAL(18, 4)       NULL,     -- Triệu tấn CO2e quy đổi
    [Renewable_Energy_Pct]  DECIMAL(5, 2)        NULL,     -- % Năng lượng tái tạo
    [GDP_USD]               DECIMAL(18, 2)       NULL,     -- Tổng sản phẩm quốc nội hiện hành
    [Created_At]            DATETIME             NOT NULL DEFAULT GETDATE(),

    -- Ràng buộc Khóa chính & Khóa ngoại
    CONSTRAINT [PK_Fact_National_Emissions] PRIMARY KEY CLUSTERED ([Emission_ID]),
    CONSTRAINT [FK_Fact_National_Date] FOREIGN KEY ([Date_Key]) 
        REFERENCES [dwh].[Dim_Date] ([Date_Key]) ON DELETE NO ACTION,
    CONSTRAINT [FK_Fact_National_Sector] FOREIGN KEY ([Sector_Key]) 
        REFERENCES [dwh].[Dim_Sector] ([Sector_Key]) ON DELETE NO ACTION,

    -- Ràng buộc kiểm tra tính hợp lệ logic (Check Constraints)
    CONSTRAINT [CK_National_Emissions_NonNegative] CHECK ([Emissions_MtCO2e] >= 0),
    CONSTRAINT [CK_National_CO2_NonNegative] CHECK ([CO2_MtCO2e] IS NULL OR [CO2_MtCO2e] >= 0),
    CONSTRAINT [CK_National_CH4_NonNegative] CHECK ([Methane_MtCO2e] IS NULL OR [Methane_MtCO2e] >= 0),
    CONSTRAINT [CK_National_Renewable_Range] CHECK ([Renewable_Energy_Pct] IS NULL OR ([Renewable_Energy_Pct] >= 0 AND [Renewable_Energy_Pct] <= 100)),
    CONSTRAINT [CK_National_GDP_NonNegative] CHECK ([GDP_USD] IS NULL OR [GDP_USD] >= 0)
);
GO

-- 3.2. Fact_Provincial_Economy: Kinh tế xã hội và phát thải ước tính 63 tỉnh thành
-- Grain: 1 dòng cho 1 tỉnh thành trong 1 năm
PRINT N'[INFO] Đang tạo bảng dwh.Fact_Provincial_Economy...';
CREATE TABLE [dwh].[Fact_Provincial_Economy] (
    [Economy_ID]                    BIGINT IDENTITY(1,1) NOT NULL,
    [Date_Key]                      INT                  NOT NULL,
    [Province_Key]                  INT                  NOT NULL,
    [GRDP_Billion_VND]              DECIMAL(18, 2)       NOT NULL, -- Tỷ VNĐ
    [Population]                    BIGINT               NOT NULL, -- Người
    [Industrial_Output_Billion_VND] DECIMAL(18, 2)       NOT NULL, -- Tỷ VNĐ
    [Forest_Coverage_Pct]           DECIMAL(5, 2)        NOT NULL, -- % Che phủ rừng
    [Estimated_Carbon_Tonnes]       DECIMAL(18, 4)       NOT NULL, -- Tấn CO2e ước lượng
    [Decoupling_Index]              DECIMAL(18, 4)       NOT NULL, -- Chỉ số tách rời kinh tế - carbon Tapio
    [Created_At]                    DATETIME             NOT NULL DEFAULT GETDATE(),

    -- Ràng buộc Khóa chính & Khóa ngoại
    CONSTRAINT [PK_Fact_Provincial_Economy] PRIMARY KEY CLUSTERED ([Economy_ID]),
    CONSTRAINT [FK_Fact_Provincial_Date] FOREIGN KEY ([Date_Key]) 
        REFERENCES [dwh].[Dim_Date] ([Date_Key]) ON DELETE NO ACTION,
    CONSTRAINT [FK_Fact_Provincial_Province] FOREIGN KEY ([Province_Key]) 
        REFERENCES [dwh].[Dim_Province] ([Province_Key]) ON DELETE NO ACTION,

    -- Ràng buộc kiểm tra tính hợp lệ logic (Check Constraints)
    CONSTRAINT [CK_Provincial_GRDP_Positive] CHECK ([GRDP_Billion_VND] >= 0),
    CONSTRAINT [CK_Provincial_Population_Positive] CHECK ([Population] >= 0),
    CONSTRAINT [CK_Provincial_IndOutput_NonNegative] CHECK ([Industrial_Output_Billion_VND] >= 0),
    CONSTRAINT [CK_Provincial_Forest_Range] CHECK ([Forest_Coverage_Pct] >= 0 AND [Forest_Coverage_Pct] <= 100),
    CONSTRAINT [CK_Provincial_Carbon_Positive] CHECK ([Estimated_Carbon_Tonnes] >= 0),
    CONSTRAINT [CK_Provincial_Decoupling_Valid] CHECK ([Decoupling_Index] IS NOT NULL)
);
GO

-- ==============================================================================
-- 4. TỐI ƯU HÓA CHỈ MỤC (INDEXING STRATEGY CHO POWER BI & OLAP STAR JOIN)
-- ==============================================================================

-- 4.1. Non-Clustered Indexes trên các Khóa ngoại (Gia tốc Star Join)
PRINT N'[INFO] Đang tạo các Non-Clustered Indexes trên Khóa ngoại...';
CREATE NONCLUSTERED INDEX [IX_Fact_National_Date] 
    ON [dwh].[Fact_National_Emissions] ([Date_Key]);
CREATE NONCLUSTERED INDEX [IX_Fact_National_Sector] 
    ON [dwh].[Fact_National_Emissions] ([Sector_Key]);

CREATE NONCLUSTERED INDEX [IX_Fact_Provincial_Date] 
    ON [dwh].[Fact_Provincial_Economy] ([Date_Key]);
CREATE NONCLUSTERED INDEX [IX_Fact_Provincial_Province] 
    ON [dwh].[Fact_Provincial_Economy] ([Province_Key]);
GO

-- 4.2. Composite Covering Index: Tối ưu hóa truy vấn Dashboard Power BI theo Năm & Tỉnh
PRINT N'[INFO] Đang tạo Composite Covering Index cho Fact_Provincial_Economy...';
CREATE NONCLUSTERED INDEX [IX_Fact_Provincial_Date_Province]
    ON [dwh].[Fact_Provincial_Economy] ([Date_Key], [Province_Key])
    INCLUDE ([GRDP_Billion_VND], [Estimated_Carbon_Tonnes], [Decoupling_Index]);
GO

PRINT N'[COMPLETE] Tạo thành công toàn bộ mô hình Star Schema (3 Dim, 2 Fact, PK/FK, Indexes) trong schema [dwh].';
GO
