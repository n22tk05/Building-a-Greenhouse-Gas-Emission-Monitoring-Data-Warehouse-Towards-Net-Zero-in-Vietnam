-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 4 - ETL Stored Procedures
-- File: sql/03b_etl_stored_procedures.sql
-- Description: Stored Procedures nạp dữ liệu từ Staging vào Fact & Dimension
-- ==============================================================================

USE [NetZero_VN_DWH];
GO

-- ==============================================================================
-- 1. SP: Nạp và đồng bộ từ Staging vào các bảng Dimension (Surrogate Key generation)
-- ==============================================================================
IF OBJECT_ID(N'dwh.sp_Load_Staging_To_Dimensions', N'P') IS NOT NULL
BEGIN
    DROP PROCEDURE [dwh].[sp_Load_Staging_To_Dimensions];
END
GO

PRINT N'[INFO] Đang tạo Stored Procedure dwh.sp_Load_Staging_To_Dimensions...';
GO
CREATE PROCEDURE [dwh].[sp_Load_Staging_To_Dimensions]
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        PRINT N'[INFO] [1/2] Đồng bộ dữ liệu vào dwh.Dim_Province...';
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

        PRINT N'[INFO] [2/2] Đồng bộ dữ liệu vào dwh.Dim_Sector...';
        MERGE INTO [dwh].[Dim_Sector] AS target
        USING (
            SELECT DISTINCT 
                [Sector_Code], 
                [Sector_Name_EN], 
                [Sector_Name_VI], 
                [Sector_Category]
            FROM [staging].[stg_cw_sector_emissions]
            WHERE [Sector_Code] IS NOT NULL
        ) AS source
        ON (target.[Sector_Code] = source.[Sector_Code])
        WHEN MATCHED THEN
            UPDATE SET 
                target.[Sector_Name_EN] = source.[Sector_Name_EN],
                target.[Sector_Name_VI] = source.[Sector_Name_VI],
                target.[Sector_Category] = source.[Sector_Category]
        WHEN NOT MATCHED THEN
            INSERT ([Sector_Code], [Sector_Name_EN], [Sector_Name_VI], [Sector_Category])
            VALUES (source.[Sector_Code], source.[Sector_Name_EN], source.[Sector_Name_VI], source.[Sector_Category]);

        PRINT N'[SUCCESS] Hoàn thành đồng bộ Dimensions từ Staging.';
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO

-- ==============================================================================
-- 2. SP: Tra cứu Surrogate Keys và nạp dữ liệu từ Staging vào Fact Tables
-- ==============================================================================
IF OBJECT_ID(N'dwh.sp_Load_Staging_To_Facts', N'P') IS NOT NULL
BEGIN
    DROP PROCEDURE [dwh].[sp_Load_Staging_To_Facts];
END
GO

PRINT N'[INFO] Đang tạo Stored Procedure dwh.sp_Load_Staging_To_Facts...';
GO
CREATE PROCEDURE [dwh].[sp_Load_Staging_To_Facts]
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        PRINT N'[INFO] [1/2] Nạp dữ liệu vào dwh.Fact_National_Emissions...';
        
        BEGIN TRANSACTION;
            -- Dọn dẹp dữ liệu cũ của các năm có trong staging để tránh trùng lặp (Idempotent Load)
            DELETE FROM [dwh].[Fact_National_Emissions]
            WHERE [Date_Key] IN (SELECT DISTINCT [Year] FROM [staging].[stg_cw_sector_emissions]);

            INSERT INTO [dwh].[Fact_National_Emissions] (
                [Date_Key],
                [Sector_Key],
                [Gas],
                [Emissions_MtCO2e],
                [CO2_MtCO2e],
                [Methane_MtCO2e],
                [Renewable_Energy_Pct],
                [GDP_USD]
            )
            SELECT 
                d.[Date_Key],
                s.[Sector_Key],
                cw.[Gas],
                ISNULL(cw.[Emissions_MtCO2e], 0),
                wb.[CO2_MtCO2e],
                wb.[Methane_MtCO2e],
                -- Overcounting protection: Chỉ gán GDP và Renewable cho Sector_Code = 'TOT'
                CASE WHEN s.[Sector_Code] = 'TOT' THEN wb.[Renewable_Energy_Pct] ELSE NULL END,
                CASE WHEN s.[Sector_Code] = 'TOT' THEN wb.[GDP_USD] ELSE NULL END
            FROM [staging].[stg_cw_sector_emissions] cw
            INNER JOIN [dwh].[Dim_Date] d 
                ON cw.[Year] = d.[Year]
            INNER JOIN [dwh].[Dim_Sector] s 
                ON cw.[Sector_Code] = s.[Sector_Code]
            LEFT JOIN [staging].[stg_wb_national_emissions] wb 
                ON cw.[Year] = wb.[Year];
        COMMIT TRANSACTION;

        PRINT N'[INFO] [2/2] Nạp dữ liệu vào dwh.Fact_Provincial_Economy...';
        
        BEGIN TRANSACTION;
            DELETE FROM [dwh].[Fact_Provincial_Economy]
            WHERE [Date_Key] IN (SELECT DISTINCT [Year] FROM [staging].[stg_gso_provincial_economy]);

            INSERT INTO [dwh].[Fact_Provincial_Economy] (
                [Date_Key],
                [Province_Key],
                [GRDP_Billion_VND],
                [Population],
                [Industrial_Output_Billion_VND],
                [Forest_Coverage_Pct],
                [Estimated_Carbon_Tonnes],
                [Decoupling_Index]
            )
            SELECT 
                d.[Date_Key],
                p.[Province_Key],
                ISNULL(gso.[GRDP_Billion_VND], 0),
                ISNULL(gso.[Population], 0),
                ISNULL(gso.[Industrial_Output_Billion_VND], 0),
                ISNULL(gso.[Forest_Coverage_Pct], 0),
                ISNULL(gso.[Estimated_Carbon_Tonnes], 0),
                ISNULL(gso.[Decoupling_Index], 0)
            FROM [staging].[stg_gso_provincial_economy] gso
            INNER JOIN [dwh].[Dim_Date] d 
                ON gso.[Year] = d.[Year]
            INNER JOIN [dwh].[Dim_Province] p 
                ON gso.[Province_Code] = p.[Province_Code];
        COMMIT TRANSACTION;

        PRINT N'[SUCCESS] Hoàn thành nạp dữ liệu vào các bảng Fact với Transaction an toàn.';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

PRINT N'[COMPLETE] Tạo thành công các ETL Stored Procedures trong schema [dwh].';
GO
