-- ==============================================================================
-- Project: Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
-- Phase: 2 - Database Initialization
-- File: sql/00_init_database.sql
-- Description: Khởi tạo Cơ sở Dữ liệu NetZero_VN_DWH và thiết lập Schema phân tầng
-- ==============================================================================

USE [master];
GO

-- 1. Khởi tạo Database với Collation chuẩn tiếng Việt (Vietnamese_CI_AS)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'NetZero_VN_DWH')
BEGIN
    PRINT N'[INFO] Đang khởi tạo Cơ sở Dữ liệu NetZero_VN_DWH...';
    CREATE DATABASE [NetZero_VN_DWH]
    COLLATE Vietnamese_CI_AS;
    PRINT N'[SUCCESS] Khởi tạo Database NetZero_VN_DWH thành công với Collation Vietnamese_CI_AS.';
END
ELSE
BEGIN
    PRINT N'[INFO] Database NetZero_VN_DWH đã tồn tại sẵn.';
END
GO

-- 2. Tối ưu hóa cấu hình cho Data Warehouse (Recovery Model = SIMPLE để tối ưu ETL log)
ALTER DATABASE [NetZero_VN_DWH] SET RECOVERY SIMPLE;
ALTER DATABASE [NetZero_VN_DWH] SET AUTO_CREATE_STATISTICS ON;
ALTER DATABASE [NetZero_VN_DWH] SET AUTO_UPDATE_STATISTICS ON;
GO

-- 3. Chuyển sang ngữ cảnh Database NetZero_VN_DWH
USE [NetZero_VN_DWH];
GO

-- 4. Tạo Schema phân tầng: staging (Tầng trung gian ETL) và dwh (Tầng kho dữ liệu chuẩn)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'staging')
BEGIN
    PRINT N'[INFO] Đang tạo Schema [staging]...';
    EXEC('CREATE SCHEMA [staging] AUTHORIZATION [dbo];');
    PRINT N'[SUCCESS] Tạo Schema [staging] thành công.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'dwh')
BEGIN
    PRINT N'[INFO] Đang tạo Schema [dwh]...';
    EXEC('CREATE SCHEMA [dwh] AUTHORIZATION [dbo];');
    PRINT N'[SUCCESS] Tạo Schema [dwh] thành công.';
END
GO

PRINT N'[COMPLETE] Hoàn thành cấu hình khởi tạo Database và Schemas cho NetZero_VN_DWH.';
GO
