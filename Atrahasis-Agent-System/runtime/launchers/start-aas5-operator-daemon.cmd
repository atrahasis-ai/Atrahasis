@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0..\..\scripts\start_aas5_operator_stack.ps1" -Daemon -Open %*
