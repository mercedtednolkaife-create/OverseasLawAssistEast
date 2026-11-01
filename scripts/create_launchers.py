# -*- coding: utf-8 -*-
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. start.ps1 完整源码
START_PS1 = r'''# ==============================================================================
# 东盟域外法查明助手 (OverseasLawAssistEast) - 一键服务启动管理器
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "       东盟域外法查明助手 (OverseasLawAssistEast) - 一键启动器" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 Python 环境
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[错误] 未检测到 Python 运行环境！" -ForegroundColor Red
    Write-Host "请先安装 Python 3.10 或更高版本，并在安装时勾选 'Add python.exe to PATH'。" -ForegroundColor Yellow
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Gray
    Write-Host ""
    Read-Host "按回车键退出..."
    exit 1
}
$pyVer = python --version 2>&1
Write-Host "[✓] Python 环境检测正常: $pyVer" -ForegroundColor Green

# 2. 检查 Node.js / npm 环境
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $nodeCmd -or -not $npmCmd) {
    Write-Host "[错误] 未检测到 Node.js / npm 运行环境！" -ForegroundColor Red
    Write-Host "请先安装 Node.js (推荐 v18+ 或 v20+ LTS 版)。" -ForegroundColor Yellow
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Gray
    Write-Host ""
    Read-Host "按回车键退出..."
    exit 1
}
$nodeVer = node --version 2>&1
Write-Host "[✓] Node.js 环境检测正常: $nodeVer" -ForegroundColor Green

# 3. 检查前端依赖 node_modules 是否就绪
$frontendDir = Join-Path $rootDir "FrontEnd"
$nodeModulesDir = Join-Path $frontendDir "node_modules"
if (-not (Test-Path $nodeModulesDir)) {
    Write-Host "[提示] 检测到前端依赖尚未安装，正在为您自动执行 npm install，请稍候..." -ForegroundColor Yellow
    Push-Location $frontendDir
    npm install
    Pop-Location
    if (-not (Test-Path $nodeModulesDir)) {
        Write-Host "[错误] 前端依赖安装失败，请检查网络后重试。" -ForegroundColor Red
        Read-Host "按回车键退出..."
        exit 1
    }
    Write-Host "[✓] 前端依赖安装成功！" -ForegroundColor Green
}

# 4. 释放可能被占用的历史端口 (8000 与 3000)
function Stop-PortProcess([int]$port) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        foreach ($c in $conns) {
            $pidToKill = $c.OwningProcess
            if ($pidToKill -gt 0) {
                Write-Host "[提示] 端口 $port 已被占用 (PID: $pidToKill)，正在为您自动释放..." -ForegroundColor Yellow
                Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
            }
        }
    }
}
Stop-PortProcess 8000
Stop-PortProcess 3000

# 5. 启动后端 FastAPI 服务
Write-Host "`n[1/3] 正在启动后端 FastAPI 服务 (端口 8000)..." -ForegroundColor Cyan
$backendTitle = "东盟法查明-后端API (8000)"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k chcp 65001>nul & title $backendTitle & cd /d `"$rootDir`" & python -m uvicorn lawagent.api.main:app --host 127.0.0.1 --port 8000 --reload"

# 6. 启动前端 Vite Web 服务
Write-Host "[2/3] 正在启动前端 Vite 服务 (端口 3000)..." -ForegroundColor Cyan
$frontendTitle = "东盟法查明-前端Web (3000)"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k chcp 65001>nul & title $frontendTitle & cd /d `"$frontendDir`" & npm run dev"

# 7. 轮询检测服务就绪
Write-Host "[3/3] 正在等待前后端服务初始化并完成就绪检查..." -ForegroundColor Cyan
$maxWaitSeconds = 30
$waited = 0
$isReady = $false

while ($waited -lt $maxWaitSeconds -and -not $isReady) {
    Start-Sleep -Milliseconds 1000
    $waited++
    Write-Host -NoNewline "." -ForegroundColor DarkGray
    
    $p8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    $p3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
    
    if ($p8000 -and $p3000) {
        $isReady = $true
    }
}

Write-Host ""
if ($isReady) {
    Write-Host "==============================================================================" -ForegroundColor Green
    Write-Host "[✓ 成功] 前后端服务均已正常启动并进入就绪状态！" -ForegroundColor Green
    Write-Host "==============================================================================" -ForegroundColor Green
} else {
    Write-Host "[提示] 服务启动初始化耗时较长，正在尝试为您直接打开浏览器..." -ForegroundColor Yellow
}

# 8. 唤起系统默认浏览器
Write-Host "[*] 正在调用系统默认浏览器打开东盟域外法查明助手..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

# 9. 服务访问信息看板与退出指引
Write-Host ""
Write-Host "==============================================================================" -ForegroundColor White
Write-Host " 服务访问入口清单:" -ForegroundColor White
Write-Host "   - 前端 Web 交互控制台:  http://localhost:3000" -ForegroundColor Green
Write-Host "   - 后端 API 根地址:      http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "   - Swagger 交互文档:     http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor White
Write-Host ""
Write-Host "【提示】前后端服务正在后台窗口持续运行。" -ForegroundColor Yellow
Write-Host "如果需要停止并关闭所有前后端服务，请直接按【回车键 / Enter】或关闭此控制台。" -ForegroundColor Yellow
Write-Host "（您也可以随时双击运行 stop.bat 停止服务）" -ForegroundColor Gray
Write-Host "==============================================================================" -ForegroundColor White

Read-Host "按回车键停止所有服务并退出..."

# 10. 安全清理进程
Write-Host ""
Write-Host "[正在退出] 正在关闭前后端服务并释放端口..." -ForegroundColor Yellow
Stop-PortProcess 8000
Stop-PortProcess 3000
Write-Host "[✓] 全部服务已安全停止，感谢使用！" -ForegroundColor Green
Start-Sleep -Seconds 1
'''

# 2. start.bat 批处理文件 (带 ExecutionPolicy Bypass，双击即开)
START_BAT = '''@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title 东盟域外法查明助手 - 正在启动...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
'''

# 3. stop.ps1 完整源码
STOP_PS1 = r'''# ==============================================================================
# 东盟域外法查明助手 (OverseasLawAssistEast) - 一键停止服务
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Stop-PortProcess([int]$port) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($connections) {
        foreach ($conn in $connections) {
            $pId = $conn.OwningProcess
            if ($pId -gt 0) {
                Write-Host "[OK] 正在停止占用端口 $port 的进程 (PID: $pId)..." -ForegroundColor Yellow
                Stop-Process -Id $pId -Force -ErrorAction SilentlyContinue
            }
        }
    } else {
        Write-Host "[*] 端口 $port 当前未被占用" -ForegroundColor DarkGray
    }
}

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "       东盟域外法查明助手 (OverseasLawAssistEast) - 停止服务管理器            " -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "正在停止后端 FastAPI 服务 (端口 8000)..." -ForegroundColor Cyan
Stop-PortProcess 8000

Write-Host "正在停止前端 Vite 服务 (端口 3000)..." -ForegroundColor Cyan
Stop-PortProcess 3000

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "[✓ 成功] 前后端服务已全部安全停止，端口 8000 与 3000 已释放！" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Start-Sleep -Seconds 2
'''

# 4. stop.bat 批处理文件 (带 ExecutionPolicy Bypass，双击即开)
STOP_BAT = '''@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title 东盟域外法查明助手 - 一键停止服务
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop.ps1"
'''

with open(os.path.join(ROOT_DIR, "start.ps1"), "w", encoding="utf-8") as f:
    f.write(START_PS1)
print("[OK] start.ps1 written.")

with open(os.path.join(ROOT_DIR, "start.bat"), "w", encoding="utf-8") as f:
    f.write(START_BAT)
print("[OK] start.bat written.")

with open(os.path.join(ROOT_DIR, "stop.ps1"), "w", encoding="utf-8") as f:
    f.write(STOP_PS1)
print("[OK] stop.ps1 written.")

with open(os.path.join(ROOT_DIR, "stop.bat"), "w", encoding="utf-8") as f:
    f.write(STOP_BAT)
print("[OK] stop.bat written.")

print("All launcher scripts created successfully.")
