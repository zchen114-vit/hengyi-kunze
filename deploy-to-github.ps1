# deploy-to-github.ps1
# Helper script to prepare push to GitHub

$GITHUB_USER = "zchen114-vit"
$REPO_NAME = "hengyi-kunze"

Write-Host "=== Hengyi Kunze Deployment Prep ===" -ForegroundColor Cyan

if (-not (Test-Path .git)) {
    git init
}

git add .
git commit -m "Ready for Streamlit Cloud deployment" --allow-empty

git branch -M main

$originUrl = "https://github.com/$GITHUB_USER/$REPO_NAME.git"

if ((git remote) -contains "origin") {
    git remote set-url origin $originUrl
} else {
    git remote add origin $originUrl
}

Write-Host ""
Write-Host "Local prep done!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure the repo exists on GitHub: https://github.com/zchen114-vit/hengyi-kunze"
Write-Host "2. To push, run:"
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "If permission error, use PAT:"
Write-Host "   git remote set-url origin https://zchen114-vit:YOUR_PAT@github.com/zchen114-vit/hengyi-kunze.git"
Write-Host "   git push -u origin main"
Write-Host "   Then reset: git remote set-url origin https://github.com/zchen114-vit/hengyi-kunze.git"
Write-Host ""
Write-Host "After push, go to https://share.streamlit.io to deploy." -ForegroundColor Green
