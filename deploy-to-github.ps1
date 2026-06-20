# deploy-to-github.ps1
# 恆易 · 坤澤 部署輔助腳本
#
# 使用步驟：
# 1. 先去 GitHub 建立 Public Repository，名稱建議 hengyi-kunze
# 2. 確認下面的 $GITHUB_USER 是正確的
# 3. 在 PowerShell 執行: .\deploy-to-github.ps1
# 4. 最後手動執行 git push

$GITHUB_USER = "zchen114-vit"
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
Write-Host "1. 確認已在 GitHub 建立 https://github.com/$GITHUB_USER/$REPO_NAME （Public）"
Write-Host "2. 執行推送指令："
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "推送成功後，前往 https://share.streamlit.io 點擊 New app 選擇 repo 部署。" -ForegroundColor Green
