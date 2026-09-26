-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 2 - Staging Tables DDL
-- File: sql/01_create_staging_tables.sql
-- Description: Tạo 4 bảng Staging ánh xạ 1:1 với dữ liệu CSV nguồn và SP Truncate
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. Bảng Staging: Phát thải quốc gia World Bank (stg_wb_national_emissions)
-- Nguồn dữ liệu: data/staging/wb_national_emissions.csv
-- ==============================================================================
IF OBJECT_ID(N'staging.stg_wb_national_emissions', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng staging.stg_wb_national_emissions cũ...';
    DROP TABLE [staging].[stg_wb_national_emissions];
END
GO

PRINT N'[INFO] Đang tạo bảng staging.stg_wb_national_emissions...';
CREATE TABLE [staging].[stg_wb_national_emissions] (
    [Year]                  INT             NOT NULL,
    [CO2_MtCO2e]            DECIMAL(18, 4)  NULL,
    [CO2_Per_Capita_Tonnes] DECIMAL(18, 6)  NULL,
    [GDP_USD]               DECIMAL(18, 2)  NULL,
    [Methane_MtCO2e]        DECIMAL(18, 4)  NULL,
    [Renewable_Energy_Pct]  DECIMAL(5, 2)   NULL,
    [Total_GHG_MtCO2e]      DECIMAL(18, 4)  NULL,
    -- Metadata phục vụ kiểm soát chất lượng & truy xuất nguồn gốc (Data Lineage)
    [Loaded_At]             DATETIME        NOT NULL DEFAULT GETDATE(),
    [Source_File]           NVARCHAR(255)   NOT NULL DEFAULT N'wb_national_emissions.csv'
);
GO

-- ==============================================================================
-- 2. Bảng Staging: Phát thải theo ngành ClimateWatch (stg_cw_sector_emissions)
-- Nguồn dữ liệu: data/staging/cw_sector_emissions.csv
-- ==============================================================================
IF OBJECT_ID(N'staging.stg_cw_sector_emissions', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng staging.stg_cw_sector_emissions cũ...';
    DROP TABLE [staging].[stg_cw_sector_emissions];
END
GO

PRINT N'[INFO] Đang tạo bảng staging.stg_cw_sector_emissions...';
CREATE TABLE [staging].[stg_cw_sector_emissions] (
    [Year]                  INT             NOT NULL,
    [Sector_Code]           VARCHAR(20)     NOT NULL,
    [Sector_Name_EN]        VARCHAR(100)    NOT NULL,
    [Sector_Name_VI]        NVARCHAR(150)   NOT NULL,
    [Sector_Category]       NVARCHAR(50)    NOT NULL,
    [Gas]                   VARCHAR(20)     NOT NULL,
    [Source]                VARCHAR(50)     NULL,
    [Emissions_MtCO2e]      DECIMAL(18, 4)  NULL,
    -- Metadata phục vụ kiểm soát chất lượng & truy xuất nguồn gốc (Data Lineage)
    [Loaded_At]             DATETIME        NOT NULL DEFAULT GETDATE(),
    [Source_File]           NVARCHAR(255)   NOT NULL DEFAULT N'cw_sector_emissions.csv'
);
GO

-- ==============================================================================
-- 3. Bảng Staging: Kinh tế & Phát thải cấp tỉnh GSO (stg_gso_provincial_economy)
-- Nguồn dữ liệu: data/staging/gso_provincial_economy.csv
-- ==============================================================================
IF OBJECT_ID(N'staging.stg_gso_provincial_economy', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng staging.stg_gso_provincial_economy cũ...';
    DROP TABLE [staging].[stg_gso_provincial_economy];
END
GO

PRINT N'[INFO] Đang tạo bảng staging.stg_gso_provincial_economy...';
CREATE TABLE [staging].[stg_gso_provincial_economy] (
    [Year]                          INT             NOT NULL,
    [Province_Code]                 VARCHAR(10)     NOT NULL,
    [Province_Name]                 NVARCHAR(100)   NOT NULL,
    [GRDP_Billion_VND]              DECIMAL(18, 2)  NULL,
    [Population]                    BIGINT          NULL,
    [Industrial_Output_Billion_VND] DECIMAL(18, 2)  NULL,
    [Forest_Coverage_Pct]           DECIMAL(5, 2)   NULL,
    [Estimated_Carbon_Tonnes]       DECIMAL(18, 4)  NULL,
    [Decoupling_Index]              DECIMAL(18, 4)  NULL,
    -- Metadata phục vụ kiểm soát chất lượng & truy xuất nguồn gốc (Data Lineage)
    [Loaded_At]                     DATETIME        NOT NULL DEFAULT GETDATE(),
    [Source_File]                   NVARCHAR(255)   NOT NULL DEFAULT N'gso_provincial_economy.csv'
);
GO

-- ==============================================================================
-- 4. Bảng Staging: Danh mục chuẩn 63 tỉnh thành (stg_dim_provinces)
-- Nguồn dữ liệu: data/reference/dim_provinces_master.csv
-- ==============================================================================
IF OBJECT_ID(N'staging.stg_dim_provinces', N'U') IS NOT NULL
BEGIN
    PRINT N'[INFO] Đang xóa bảng staging.stg_dim_provinces cũ...';
    DROP TABLE [staging].[stg_dim_provinces];
END
GO

PRINT N'[INFO] Đang tạo bảng staging.stg_dim_provinces...';
CREATE TABLE [staging].[stg_dim_provinces] (
    [Province_Code]         VARCHAR(10)     NOT NULL,
    [Province_Name]         NVARCHAR(100)   NOT NULL,
    [Province_Name_Ascii]   VARCHAR(100)    NOT NULL,
    [Region]                NVARCHAR(50)    NOT NULL,
    [Economic_Zone]         NVARCHAR(100)   NOT NULL,
    [Area_Km2]              DECIMAL(10, 2)  NULL,
    [Is_Industrial_Hub]     BIT             NULL,
    -- Metadata phục vụ kiểm soát chất lượng & truy xuất nguồn gốc (Data Lineage)
    [Loaded_At]             DATETIME        NOT NULL DEFAULT GETDATE(),
    [Source_File]           NVARCHAR(255)   NOT NULL DEFAULT N'dim_provinces_master.csv'
);
GO

-- ==============================================================================
-- 5. Stored Procedure: Truncate toàn bộ Staging trước mỗi chu trình nạp SSIS
-- ==============================================================================
IF OBJECT_ID(N'staging.sp_Truncate_Staging', N'P') IS NOT NULL
BEGIN
    DROP PROCEDURE [staging].[sp_Truncate_Staging];
END
GO

PRINT N'[INFO] Đang tạo Stored Procedure staging.sp_Truncate_Staging...';
GO
CREATE PROCEDURE [staging].[sp_Truncate_Staging]
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        PRINT N'[INFO] Bắt đầu dọn dẹp các bảng Staging...';
        TRUNCATE TABLE [staging].[stg_wb_national_emissions];
        TRUNCATE TABLE [staging].[stg_cw_sector_emissions];
        TRUNCATE TABLE [staging].[stg_gso_provincial_economy];
        TRUNCATE TABLE [staging].[stg_dim_provinces];
        PRINT N'[SUCCESS] Dọn dẹp thành công 4 bảng Staging, sẵn sàng cho chu trình ETL mới.';
    END TRY
    BEGIN CATCH
        -- Sử dụng THROW để giữ nguyên mã lỗi gốc và số dòng lỗi cho SSIS logging
        THROW;
    END CATCH
END;
GO

PRINT N'[COMPLETE] Tạo thành công 4 bảng Staging và Stored Procedure Truncate trong schema [staging].';
GO
