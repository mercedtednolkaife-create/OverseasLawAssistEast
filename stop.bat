@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title 东盟域外法查明助手 - 一键停止服务
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop.ps1"
