@echo off
chcp 65001 >nul 2>&1
set KMP_DUPLICATE_LIB_OK=TRUE
set OMP_NUM_THREADS=4
cd /d "%~dp0"
title 东盟域外法查明助手 - 正在启动...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
