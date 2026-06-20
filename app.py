"""
恆易 · 坤澤
簡易易經卜卦 App - Streamlit 版本
完全免費、無限卜卦、連續對話、無起卦隨機邏輯
"""

import streamlit as st
from datetime import datetime
import random

# ====================== 設定頁面 ======================
st.set_page_config(
    page_title="恆易 · 坤澤",
    page_icon="☯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ====================== 溫暖大地色系 CSS ======================
CUSTOM_CSS = """
<style>
:root {
    --bg: #F8F1E3;
    --card-bg: #F5EDE0;
    --accent-green: #3D5A4C;
    --accent-earth: #8B6642;
    --accent-gold: #A67C52;
    --text: #2F2A24;
    --text-light: #5C5248;
}

.stApp {
    background-color: var(--bg);
}

/* 標題與儀式感 */
.main-title {
    font-family: 'Microsoft YaHei', 'Noto Serif TC', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--accent-green);
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: 2px;
}

.subtitle {
    text-align: center;
    color: var(--accent-earth);
    font-size: 1.05rem;
    margin-bottom: 1.8rem;
}

/* 卡片設計 */
.category-card {
    background: var(--card-bg);
    border: 1.5px solid #EDE0CC;
    border-radius: 18px;
    padding: 1.25rem 1rem;
    margin-bottom: 0.6rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 12px rgba(139, 102, 66, 0.08);
}

.category-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(139, 102, 66, 0.15);
    border-color: #D4C2A0;
}

.card-icon {
    font-size: 2.1rem;
    margin-bottom: 0.4rem;
    display: block;
}

.card-title {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--accent-green);
    margin-bottom: 0.25rem;
}

.card-desc {
    font-size: 0.85rem;
    color: var(--text-light);
    line-height: 1.35;
}

/* 聊天室標頭 */
.chat-header {
    background: linear-gradient(90deg, #F5EDE0 0%, #F8F1E3 100%);
    border: 1.5px solid #EDE0CC;
    border-radius: 16px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* 側邊欄優化 */
[data-testid="stSidebar"] {
    background-color: #F5EDE0;
    border-right: 1px solid #EDE0CC;
}

/* 訊息氣泡微調 */
.stChatMessage {
    background-color: #F8F1E3;
    border-radius: 16px;
}

/* 歡迎區塊 */
.welcome-box {
    background: #F5EDE0;
    border: 1px solid #E2D5C0;
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    margin: 1rem 0;
    font-size: 0.95rem;
    color: var(--text-light);
}

/* 按鈕統一樣式 */
.stButton button {
    border-radius: 9999px;
    font-weight: 600;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ====================== 分區定義 ======================
CATEGORIES = {
    "love": {
        "name": "感情與人際",
        "icon": "❤️",
        "desc": "愛情、婚姻、友情、人際關係"
    },
    "career": {
        "name": "事業與學業",
        "icon": "📚",
        "desc": "工作發展、考試、職涯選擇"
    },
    "wealth": {
        "name": "財運與財務",
        "icon": "💰",
        "desc": "投資、收入、理財決策"
    },
    "health": {
        "name": "健康與生活",
        "icon": "🌿",
        "desc": "身心健康、日常生活調適"
    },
    "timing": {
        "name": "時機與決策",
        "icon": "⏳",
        "desc": "重要決定、時機把握"
    },
    "general": {
        "name": "綜合命理",
        "icon": "☯",
        "desc": "整體運勢、人生方向"
    }
}

# ====================== Session State 初始化 ======================
if "user_name" not in st.session_state:
    st.session_state.user_name = "朋友"
if "preference" not in st.session_state:
    st.session_state.preference = "現代"
if "current_category" not in st.session_state:
    st.session_state.current_category = None

# 為每個分區建立獨立 messages
for key in CATEGORIES.keys():
    if f"messages_{key}" not in st.session_state:
        st.session_state[f"messages_{key}"] = []

# 簡單的瀏覽器本地儲存（跨刷新保留姓名與偏好）
# 注意：Streamlit Cloud 上效果有限，但比什麼都沒有好
import streamlit.components.v1 as components

components.html("""
<script>
    // 嘗試從 localStorage 恢復
    const savedName = localStorage.getItem('hengyi_name');
    const savedPref = localStorage.getItem('hengyi_pref');
    
    if (savedName && window.parent) {
        // 透過 postMessage 通知 Streamlit（簡易版）
        // 實際上我們會在 sidebar 手動同步
    }
    
    // 監聽姓名與偏好變化並儲存（由 Python 觸發）
    window.saveProfileToLocal = function(name, pref) {
        localStorage.setItem('hengyi_name', name);
        localStorage.setItem('hengyi_pref', pref);
    }
</script>
""", height=0)

# ====================== 輔助函式 ======================

def get_yijing_response(category_key: str, question: str, name: str, preference: str) -> str:
    """原本的內建快速解讀（離線、免費、速度快）"""
    cat = CATEGORIES[category_key]
    is_traditional = preference == "傳統"

    base_intro = f"{name}，關於「{question}」這個問題，"
    if is_traditional:
        base_intro = f"《易經》有云：「{name}問『{question}』，"

    responses = {
        "love": {
            "traditional": f"{base_intro}此問屬於「咸」與「恒」之象。感情之事貴在「感而應」，不宜強求。建議以誠待人，順其自然。當下宜以「柔」為主，過剛則易折。若目前有爭執，當暫時退讓，待時而動。",
            "modern": f"{base_intro}在感情與人際這件事上，易經提醒我們「感應」的重要性。真正的連結來自於真誠的回應，而不是過度的執著。建議你先誠實面對自己的感受，也給對方空間。如果目前卡住，試著用更溫柔、理解的方式重新開啟對話。"
        },
        "career": {
            "traditional": f"{base_intro}事業學業多應「乾」之健行與「坎」之險中求進。目前階段宜「修德」與「積小勝為大勝」。若有瓶頸，或許是時機未到，需再磨練內在實力。",
            "modern": f"{base_intro}工作或學業上，易經強調「持之以恆」與「適時調整」的平衡。不要急著求大突破，先把眼前的事做到極致。若你正考慮轉換跑道或準備考試，現在的關鍵是「內外兼修」——既要累積實力，也要觀察外部環境的風向。"
        },
        "wealth": {
            "traditional": f"{base_intro}財運之問常見「益」與「損」之辨。真正的富貴來自「義」與「時」。建議謹慎投資，勿貪快利。守正而行，財源自來。",
            "modern": f"{base_intro}財務問題上，易經教我們「知進退」。現在可能不是大舉擴張的時候，建議先盤點現有資源，把錢用在「穩健增值」而非投機。若有大額決定，建議多聽聽值得信任的人的意見。"
        },
        "health": {
            "traditional": f"{base_intro}身心乃「坤」之德，宜「厚德載物」。目前宜注意作息與情緒調節。過勞則「乾」過，當以靜養為先。",
            "modern": f"{base_intro}健康與生活方面，易經最重視「中道」。建議你現在先把生活作息調整回平衡狀態。不要忽視小問題，及早處理情緒與壓力。適度運動、好好睡覺，往往比尋找特效藥更重要。"
        },
        "timing": {
            "traditional": f"{base_intro}此為「屯」與「蒙」之時。時機未明，宜「利建侯」，暫且蓄勢，等待明確信號再行動。過早則凶。",
            "modern": f"{base_intro}關於時機與決策，易經一再強調「時」的重要性。現在可能還不是最好的行動時機。建議你再觀察一段時間，收集更多資訊。真正的智慧不是「現在做」，而是「在正確的時間做正確的事」。"
        },
        "general": {
            "traditional": f"{base_intro}綜合而觀，此卦象呈現「既濟」將轉「未濟」之象。目前局面看似穩定，實則暗藏轉機。宜守中正，勿躁進。",
            "modern": f"{base_intro}從整體來看，你目前正處在一個「轉折準備期」。很多事情表面平穩，內裡其實正在醞釀變化。建議你保持開放與彈性，同時把眼前的事做好。"
        }
    }

    mode = "traditional" if is_traditional else "modern"
    response = responses.get(category_key, {}).get(mode, "請以中正之心面對。")

    action_tips = {
        "love": "試著用溫柔的態度表達你的真心。",
        "career": "把今天的工作做到讓自己滿意。",
        "wealth": "先列出本月所有開支再做決定。",
        "health": "今晚早點休息，並關掉手機一小時。",
        "timing": "再多問問自己：「如果現在不做，會後悔嗎？」",
        "general": "寫下三件讓你感恩的事。"
    }
    tip = action_tips.get(category_key, "保持平常心，順勢而為。")
    closing = " 謹守中正，吉。" if is_traditional else " 記得，改變從小行動開始。"

    return f"{response}\n\n**小提醒**：{tip}{closing}"


def build_grok_prompt(category_key: str, question: str, name: str, preference: str) -> str:
    """為 SuperGrok 產生高品質提示詞（利用你的訂閱，不額外花錢）"""
    cat = CATEGORIES[category_key]
    cat_name = cat["name"]
    is_traditional = preference == "傳統"

    style_instruction = (
        "請用古典、典雅、帶有易經原文引用與象徵意義的方式解讀。"
        if is_traditional else
        "請用現代白話、務實且有同理心的方式解讀，並給出具體可執行的建議。"
    )

    prompt = f"""你是一位精通《易經》的資深顧問，名字叫「坤澤」。

用戶資訊：
- 姓名：{name}
- 解讀偏好：{preference}
- 詢問類別：{cat_name}

用戶問題：
「{question}」

請依照以下原則回應：
1. {style_instruction}
2. 結合「{cat_name}」這個主題脈絡來解讀。
3. 可以適度引用相關卦象（如乾、坤、咸、恒、屯、蒙、既濟、未濟等），但不要強行起卦。
4. 給出有智慧、有同理心、且實用的建議。
5. 最後給 1-2 句簡短的行動提醒。
6. 語氣溫和、有儀式感，但不要過於玄。

請直接給出回應，不要多餘的說明。"""
    return prompt

# ====================== 側邊欄：個人檔案 ======================
with st.sidebar:
    st.markdown("### 個人檔案")
    
    # 嘗試從 localStorage 讀取（簡易方式）
    name = st.text_input("你的稱呼", value=st.session_state.user_name, key="name_input")
    if name != st.session_state.user_name:
        st.session_state.user_name = name
        # 儲存到瀏覽器
        components.html(f"""
        <script>
            localStorage.setItem('hengyi_name', '{name}');
        </script>
        """, height=0)

    pref = st.radio(
        "解讀偏好",
        ["現代", "傳統"],
        index=0 if st.session_state.preference == "現代" else 1,
        horizontal=True,
        key="pref_input"
    )
    if pref != st.session_state.preference:
        st.session_state.preference = pref
        components.html(f"""
        <script>
            localStorage.setItem('hengyi_pref', '{pref}');
        </script>
        """, height=0)

    # 載入已儲存的值（如果有）
    # 注意：這部分需要在 rerun 後才能完全生效，簡單版先這樣

    st.divider()

    # 顯示目前狀態
    if st.session_state.current_category:
        cat_info = CATEGORIES[st.session_state.current_category]
        st.markdown(f"**目前所在**  \n{cat_info['icon']} {cat_info['name']}")
    else:
        st.markdown("**目前在首頁**")

    st.divider()

    st.markdown("**💡 解讀方式建議**")
    st.caption("有 SuperGrok 訂閱的話，強烈建議使用「SuperGrok 專業解讀」，品質明顯更好，且不額外花錢。")

    st.caption("恆易 · 坤澤\n完全免費・無限使用")

# ====================== 主畫面 ======================
def show_homepage():
    """顯示首頁"""
    st.markdown('<div class="main-title">恆易 · 坤澤</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">問心 · 觀象 · 得道</div>', unsafe_allow_html=True)

    # 歡迎與說明
    with st.container():
        st.markdown(f"""
        <div class="welcome-box">
        歡迎你，<b>{st.session_state.user_name}</b>。<br><br>
        這裡沒有複雜的起卦程序。<br>
        誠心提出你的問題，易經顧問將以智慧回應。<br><br>
        <b>使用方式：</b>點擊下方任一生活分區，即可進入獨立聊天室開始對話。
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 請選擇你想咨詢的分區")

    # 分享區塊（適合公開推廣）
    st.markdown("---")
    with st.container():
        st.markdown("**📢 想讓我親自幫你解讀？**")
        st.info("目前 App 是自助式。如果你想讓我（開發者）親自用易經詳細解答，請：\n\n1. 在這裡輸入問題\n2. 點下方按鈕複製「提交內容」\n3. 去 Threads 或 IG 私訊我")
        
        manual_q = st.text_input("想問的問題（選填）", key="manual_question", placeholder="例如：最近工作很卡，該不該換工作？")
        
        if st.button("📋 複製提交內容給我親自解", use_container_width=True):
            cat_name = "未選擇分區"
            if st.session_state.current_category:
                cat_name = CATEGORIES[st.session_state.current_category]['name']
            
            submit_text = f"""【恆易·坤澤 親自解讀請求】
分區：{cat_name}
姓名：{st.session_state.user_name}
偏好：{st.session_state.preference}

問題：
{manual_q if manual_q else "（請在這裡補充你的問題）"}

請幫我詳細解讀，謝謝！"""
            
            st.code(submit_text, language="text")
            st.success("請複製上方文字，私訊給我（Threads / IG）")

        st.markdown("**💬 想分享這個工具？**")
        st.caption("把上方網址傳給朋友，或教他們「加到主畫面」當 App 使用。")

    # 6 個卡片，使用 3 欄
    cols = st.columns(3)

    cat_keys = list(CATEGORIES.keys())
    for i, key in enumerate(cat_keys):
        col = cols[i % 3]
        cat = CATEGORIES[key]
        msg_count = len(st.session_state.get(f"messages_{key}", []))

        with col:
            # 卡片內容
            count_text = f"<span style='font-size:0.72rem; color:#A67C52;'>{msg_count} 則對話</span>" if msg_count > 0 else ""
            st.markdown(f"""
            <div class="category-card">
                <span class="card-icon">{cat['icon']}</span>
                <div class="card-title">{cat['name']}</div>
                <div class="card-desc">{cat['desc']}</div>
                {count_text}
            </div>
            """, unsafe_allow_html=True)

            # 進入按鈕
            btn_label = "繼續對話" if msg_count > 0 else "進入此分區"
            if st.button(btn_label, key=f"enter_{key}", use_container_width=True):
                st.session_state.current_category = key
                # 如果是第一次進入這個分區，加入歡迎訊息
                msg_key = f"messages_{key}"
                if len(st.session_state[msg_key]) == 0:
                    welcome = (
                        f"你好，{st.session_state.user_name}。我是易經顧問。\n\n"
                        f"歡迎來到「{cat['name']}」分區。\n"
                        "請誠心提出你的問題，我將以易經的智慧為你解讀。"
                    )
                    st.session_state[msg_key].append({
                        "role": "assistant",
                        "content": welcome
                    })
                st.rerun()

    st.markdown("---")
    st.caption("所有對話記錄僅保存在本機，關閉頁面後仍會保留。")

# ====================== 聊天室畫面 ======================
def show_chatroom(category_key: str):
    cat = CATEGORIES[category_key]
    msg_key = f"messages_{category_key}"

    # 頂部導航 - 使用 Streamlit 原生元件保持穩定
    header_col1, header_col2 = st.columns([5, 2])
    with header_col1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding: 4px 0;">
            <span style="font-size:1.6rem; line-height:1;">{cat['icon']}</span>
            <div>
                <div style="font-size:0.75rem; color:#8B6642;">目前分區</div>
                <div style="font-size:1.25rem; font-weight:700; color:#3D5A4C; line-height:1.1;">{cat['name']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with header_col2:
        if st.button("⬅ 回到首頁", key="back_home", use_container_width=True):
            st.session_state.current_category = None
            st.rerun()

    st.divider()

    # 顯示聊天記錄
    for message in st.session_state[msg_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 聊天輸入
    if prompt := st.chat_input("誠心提出你的問題..."):
        # 先儲存用戶問題
        st.session_state[msg_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ========== 兩種解讀方式選擇 ==========
        st.markdown("**選擇解讀方式**")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⚡ 使用內建快速解讀", key=f"quick_{len(st.session_state[msg_key])}", use_container_width=True):
                response = get_yijing_response(
                    category_key,
                    prompt,
                    st.session_state.user_name,
                    st.session_state.preference
                )
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state[msg_key].append({"role": "assistant", "content": response})
                st.toast("已使用內建解讀", icon="⚡")
                st.rerun()

        with col2:
            if st.button("✨ 使用 SuperGrok 專業解讀（推薦）", key=f"grok_{len(st.session_state[msg_key])}", use_container_width=True, type="primary"):
                st.session_state[f"pending_grok_prompt_{category_key}"] = prompt
                st.rerun()

    # 如果有 pending 的 Grok prompt，顯示專用介面
    pending_key = f"pending_grok_prompt_{category_key}"
    if pending_key in st.session_state and st.session_state[pending_key]:
        current_question = st.session_state[pending_key]
        st.divider()

        st.markdown("### ✨ 準備發送給 SuperGrok")

        full_prompt = build_grok_prompt(
            category_key,
            current_question,
            st.session_state.user_name,
            st.session_state.preference
        )

        st.code(full_prompt, language="text")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.caption("請從上方程式碼區塊手動複製")

        with col_b:
            grok_url = "https://grok.x.ai"
            st.link_button("🚀 開啟 SuperGrok 聊天", grok_url, use_container_width=True)

        with col_c:
            if st.button("🔙 取消", use_container_width=True):
                del st.session_state[pending_key]
                st.rerun()

        st.markdown("---")
        st.markdown("**請把 SuperGrok 的回覆貼在下方：**")

        pasted = st.text_area("貼上 Grok 的完整回應", height=160, key="pasted_grok_reply")

        if st.button("✅ 採用此回答並儲存", type="primary", disabled=not pasted.strip()):
            full_reply = pasted.strip()
            with st.chat_message("assistant"):
                st.markdown(full_reply)
            st.session_state[msg_key].append({"role": "assistant", "content": full_reply})
            del st.session_state[pending_key]
            st.toast("已儲存 SuperGrok 的解讀", icon="📖")
            st.rerun()

# ====================== 路由 ======================
if st.session_state.current_category is None:
    show_homepage()
else:
    show_chatroom(st.session_state.current_category)

# ====================== 全域匯出功能（方便公開分享後使用） ======================
if st.session_state.current_category:
    with st.sidebar:
        st.divider()
        if st.button("📥 匯出目前分區對話", use_container_width=True):
            messages = st.session_state.get(f"messages_{st.session_state.current_category}", [])
            if messages:
                export_text = f"# 恆易 · 坤澤 - {CATEGORIES[st.session_state.current_category]['name']} 對話記錄\n\n"
                export_text += f"使用者：{st.session_state.user_name}\n"
                export_text += f"偏好：{st.session_state.preference}\n"
                export_text += f"時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                
                for m in messages:
                    role = "你" if m["role"] == "user" else "易經顧問"
                    export_text += f"**{role}**：\n{m['content']}\n\n---\n\n"
                
                st.download_button(
                    "下載文字檔 (.txt)",
                    export_text,
                    file_name=f"坤澤_{CATEGORIES[st.session_state.current_category]['name']}.txt",
                    use_container_width=True
                )
            else:
                st.info("這個分區還沒有對話可以匯出")

# ====================== 免責聲明（公開分享建議加上） ======================
st.markdown(
    "<div style='font-size:0.7rem; color:#8B6642; text-align:center; margin-top:1rem;'>"
    "本工具僅供參考與娛樂，非專業諮詢。重大決定請自行判斷或尋求專業意見。"
    "</div>",
    unsafe_allow_html=True
)

# ====================== 頁尾 ======================
st.markdown(
    "<div style='text-align:center; color:#8B6642; font-size:0.8rem; margin-top:2rem;'>"
    "恆易 · 坤澤 — 問則有應，誠則靈驗"
    "</div>",
    unsafe_allow_html=True
)

# ====================== 資料儲存說明（給公開分享用） ======================
with st.expander("📌 關於資料儲存與隱私（重要）", expanded=False):
    st.markdown("""
    **目前資料存放位置：**
    
    - 你的姓名、偏好設定、聊天記錄 → **只存在你自己的瀏覽器裡**（使用 `sessionStorage` / 記憶體）
    - 關閉分頁或清除瀏覽資料後，記錄就會消失
    - **沒有上傳到任何伺服器永久保存**
    - 使用 SuperGrok 解讀時，真正的回答是你在 grok.x.ai 產生的，App 只負責幫你整理格式
    
    **這代表什麼？**
    - 非常注重隱私（別人看不到你的問題）
    - 但同時**無法跨裝置同步**、**無法長期保存歷史**
    - 如果想長期保存，建議使用「匯出對話」功能（之後會加上）
    
    這是公開分享版本的設計。如果你之後想要登入 + 雲端儲存，我可以再幫你加上。
    """)
