<#
.SYNOPSIS
Progressive Git Push Script for Assignment 4 (PowerShell)
Student: V. Karthik Harish (Reg No: 192511328)
Repository: CSA08-192511328-Assignment4
Remote: https://github.com/KarthikHarish170260/CSA08-192511328-Assignment4.git
#>

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "CSA08 ASSIGNMENT 4 - PROGRESSIVE GIT PUSH SCRIPT" -ForegroundColor Cyan
Write-Host "Student: V. Karthik Harish | Reg: 192511328" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$remoteUrl = "https://github.com/KarthikHarish170260/CSA08-192511328-Assignment4.git"

# Verify current git status
Write-Host "`n[1] Checking local git status and commit history..." -ForegroundColor Yellow
git status
git log --oneline

Write-Host "`n[2] Verifying remote origin configuration..." -ForegroundColor Yellow
$remotes = git remote -v
if (-not ($remotes -match "origin")) {
    Write-Host "Setting remote origin to $remoteUrl..." -ForegroundColor Green
    git remote add origin $remoteUrl
} else {
    Write-Host "Remote origin already configured." -ForegroundColor Green
}

Write-Host "`n[3] Pushing progressive commit history to GitHub (branch: main)..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] All progressive commits pushed successfully to:" -ForegroundColor Green
    Write-Host "$remoteUrl" -ForegroundColor Green
} else {
    Write-Host "`n[NOTICE] Git push returned exit code $LASTEXITCODE." -ForegroundColor Magenta
    Write-Host "If authentication is required, complete it in the Git Credential Manager." -ForegroundColor Yellow
}
