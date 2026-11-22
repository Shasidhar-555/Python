@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0push_task_by_task.ps1" %*
pause
