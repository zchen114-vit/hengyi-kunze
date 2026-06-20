# deploy-to-github.ps1
# 使用方式：
# 1. 先去 GitHub 建立一個 Public repo，名字建議 hengyi-kunze
# 2. 把下面 $GITHUB_USER 改成你的 GitHub 使用者名稱
# 3. 在 PowerShell 裡執行 .\deploy-to-github.ps1

$GITHUB_USER = "zchen114-vit"   # <--- 改這裡！！！
$REPO_NAME = "hengyi-kunze"

Write-Host "=== 恆易 · 坤澤 部署準備 ===" -ForegroundColor Cyan

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
Write-Host "✅ 本地準備完成！" -ForegroundColor Green
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 去 https://github.com/new 建立一個 Public Repository，名稱 $REPO_NAME"
Write-Host "2. 執行以下指令推送："
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "推送成功後，去 https://share.streamlit.io 點 New app 選擇你的 repo 部署。" -ForegroundColor Green
