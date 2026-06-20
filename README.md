# 洞察易生的經歷

**簡易易經卜卦 App**  
完全免費、無限次使用。純粹輸入問題，由「易經顧問」給予智慧解讀。

## 特色

- 6 大生活分區獨立聊天室
- 連續對話，記錄永久保存（同裝置）
- 無需起卦：直接輸入你的問題
- 個人檔案（姓名 + 解讀偏好）
- 溫暖大地色系，儀式感設計
- 完全使用 Streamlit 實作，跨平台網頁版（可當手機 App 使用）

## 安裝與執行

```bash
cd D:\Grok\hengyi-kunze
pip install -r requirements.txt
streamlit run app.py
```

打開後會自動在瀏覽器啟動。  
建議手機用 Safari / Chrome 的「新增到主畫面」功能，安裝成像 App 一樣使用（詳見 DEPLOY.md）。

## 使用方式

1. 側邊欄填寫姓名與偏好（傳統 / 現代）
2. 在首頁點擊想咨詢的分區卡片
3. 直接輸入你的問題
4. **選擇解讀方式**：
   - ⚡ **內建快速解讀**：立即給出回答（離線）
   - ✨ **SuperGrok 專業解讀（推薦）**：產生優化提示詞 → 複製 → 去 grok.x.ai 詢問 → 把回答貼回來
5. 可以一直追問，維持在同一個分區聊天室
6. 隨時點「回到首頁」切換其他分區

### 關於 SuperGrok 訂閱

因為你有 SuperGrok 訂閱，強烈建議使用「SuperGrok 專業解讀」：

- 不會產生額外的 API 費用
- 品質遠高於內建模板
- 每次問問題都等於用你的訂閱額度

這種方式比直接呼叫付費 API 省錢非常多。

## 技術說明

- 所有聊天記錄使用 `st.session_state` 獨立保存
- 沒有任何隨機數起卦，完全由問題內容與分區脈絡驅動
- 如想接真實 LLM（Grok / GPT），可在 `get_yijing_response()` 函式中替換 API 呼叫

## 部署與讓別人使用

詳細步驟請看 **[DEPLOY.md](DEPLOY.md)**

### 快速開始（讓別人也能用）

1. 把這個資料夾上傳到 GitHub
2. 去 [share.streamlit.io](https://share.streamlit.io) 點 New app 部署
3. 拿到網址後，告訴大家：
   - 電腦直接開網址
   - 手機用瀏覽器開 → 「加到主畫面」

這樣就算是「發佈」了，不需要上架。

## 版權與使用

純粹個人使用與學習之用。
「洞察易生的經歷」—— 洞察易經智慧，體悟人生經歷。

Built directly in D:\Grok following zero-confirmation protocol.
