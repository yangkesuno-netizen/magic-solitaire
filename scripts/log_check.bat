@echo off
REM 记录提交检查日志
REM 用法：log_check.bat [passed|failed] [message]

setlocal enabledelayedexpansion

set TIMESTAMP=%date% %time%
set CHECK_STATUS=%1
set MESSAGE=%2

if "%CHECK_STATUS%"=="" set CHECK_STATUS=unknown
if "%MESSAGE%"=="" set MESSAGE=No message

REM 获取当前 commit hash
for /f "delims=" %%i in ('git rev-parse --short HEAD 2^>nul') do set COMMIT_HASH=%%i
if "%COMMIT_HASH%"=="" set COMMIT_HASH=uncommitted

REM 读取现有日志
set LOG_FILE=CHECK_LOG.json

REM 创建日志条目
set LOG_ENTRY={"timestamp":"%TIMESTAMP%","commit":"%COMMIT_HASH%","status":"%CHECK_STATUS%","message":"%MESSAGE%"}

REM 简单追加（实际应该用 JSON 库，这里简化处理）
echo Log entry: %LOG_ENTRY% >> check_log.txt

echo ✅ 检查日志已记录：%COMMIT_HASH% - %CHECK_STATUS%

endlocal
