# ==============================================================================
# Automated Step-by-Step Task Committer and Pusher for GitHub
# Course: CSA08 / CSA0807 Python Programming - Assignment 3 (CO3)
# Student: V. Karthik Harish (192511328)
# ==============================================================================

param (
    [string]$RepoUrl = "https://github.com/KarthikHarish170260/CSA08-192511328-Assignment3.git"
)

$ErrorActionPreference = "Stop"

# Ensure we are in the script's directory
Set-Location -Path $PSScriptRoot

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "CSA0807 Assignment 3 (CO3): Progressive Commit & Push Utility" -ForegroundColor Cyan
Write-Host "Student: V. Karthik Harish | Register Number: 192511328" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Prompt for repository URL if needed
if (-not $RepoUrl) {
    Write-Host "`nBefore proceeding, create an empty repository on GitHub named:" -ForegroundColor Yellow
    Write-Host "  CSA08-192511328-Assignment3" -ForegroundColor White
    Write-Host "(Do NOT check 'Add a README file', 'Add .gitignore', or 'Choose a license'.)`n" -ForegroundColor DarkGray
    $RepoUrl = Read-Host "Paste your GitHub Repository URL (e.g. https://github.com/KarthikHarish170260/CSA08-192511328-Assignment3.git)"
}

if (-not $RepoUrl) {
    Write-Error "Repository URL cannot be empty. Aborted."
    exit 1
}

# Configure remote origin
git remote remove origin 2>$null
git remote add origin $RepoUrl
Write-Host "`n[✓] Configured remote origin: $RepoUrl" -ForegroundColor Green

# Ensure branch is main
git branch -M main

# Helper function to commit and push with feedback
function Commit-And-Push {
    param (
        [string]$PathToAdd,
        [string]$CommitMessage,
        [string]$TaskLabel,
        [int]$DelaySeconds = 1
    )

    Write-Host "`n----------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ">> Processing: $TaskLabel" -ForegroundColor Yellow
    Write-Host "   Files  : $PathToAdd" -ForegroundColor White
    Write-Host "   Message: $CommitMessage" -ForegroundColor White

    git add $PathToAdd
    # Check if there are changes to commit
    $status = git status --porcelain $PathToAdd
    if ($status) {
        git commit -m "$CommitMessage"
    } else {
        Write-Host "   (Already committed or no unstaged changes in this step)" -ForegroundColor DarkGray
    }
    
    Write-Host "   Pushing to GitHub main branch..." -ForegroundColor Cyan
    try {
        git push -u origin main
        Write-Host "   [✓] Successfully pushed $TaskLabel" -ForegroundColor Green
    } catch {
        Write-Host "   [!] Push paused: Check internet connection or authenticate GitHub credentials." -ForegroundColor Red
    }

    if ($DelaySeconds -gt 0) {
        Start-Sleep -Seconds $DelaySeconds
    }
}

# Push all progressive commits to GitHub
Write-Host "`nPushing all progressive commits to GitHub..." -ForegroundColor Cyan
try {
    git push -u origin main
    Write-Host "[✓] Progressive Git commit history pushed successfully to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "[!] Note: To push to GitHub, ensure the remote repository is created and git credentials are authenticated." -ForegroundColor Yellow
}
