# ==============================================================================
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
Write-Host "[OK 成功] 前后端服务已全部安全停止，端口 8000 与 3000 已释放！" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Start-Sleep -Seconds 2
