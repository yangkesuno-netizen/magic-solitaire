@echo off
echo ========================================
echo   Pre-Commit Check - Magic Solitaire
echo ========================================
echo.

:: 1. TypeScript Build
echo [1/5] TypeScript 编译检查...
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo ❌ 编译失败！禁止提交！
    exit /b 1
)
echo ✅ 编译通过
echo.

:: 2. Check dist directory
echo [2/5] 检查构建输出...
if not exist "dist\assets" (
    echo.
    echo ❌ dist/assets 目录不存在！
    exit /b 1
)
if not exist "dist\assets\cards" (
    echo.
    echo ⚠️  dist/assets/cards 不存在（确认是否需要卡牌资源）
    echo    按任意键继续，或 Ctrl+C 取消...
    pause
)
echo ✅ dist 目录检查通过
echo.

:: 3. Run Tests
echo [3/5] 运行单元测试...
call npm test
if %errorlevel% neq 0 (
    echo.
    echo ❌ 测试失败！禁止提交！
    exit /b 1
)
echo ✅ 测试通过
echo.

:: 4. Check for sensitive files
echo [4/5] 检查敏感文件...
git status --porcelain | findstr ".env" >nul
if %errorlevel% equ 0 (
    echo.
    echo ⚠️  发现 .env 文件，确认不要提交！
    echo    按任意键继续，或 Ctrl+C 取消...
    pause
)
echo ✅ 敏感文件检查通过
echo.

:: 5. Show git status
echo [5/5] Git 状态...
git status --short
echo.

:: Summary
echo ========================================
echo   ✅ 所有检查通过！
echo   可以安全提交
echo ========================================
echo.
echo 提示：请确保提交信息规范
echo 格式：type: description
echo 例如：feat: add new feature
echo       fix: resolve issue #123
echo.
