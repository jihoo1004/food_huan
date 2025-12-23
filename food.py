import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍴", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
        color: white;
    }
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 2rem;
    }
    .recommend-title {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP TITLE ---
st.title("🍴 오늘 뭐 먹지?")
st.write("4가지 질문을 통해 당신에게 딱 맞는 메뉴를 추천해 드릴게요!")

# --- MENU DATA ---
# 구조: (종류1, 종류2, 가격대, 주재료): [추천메뉴, 유사메뉴1, 유사메뉴2]
menu_db = {
    ("한식", "국물형", "만원 이하", "고기"): ["감자탕", "순대국", "뼈해장국"],
    ("한식", "비빔/볶음형", "만원 이하", "고기"): ["제육볶음", "불고기덮밥", "육회비빔밥"],
    ("한식", "국물형", "만원 이상", "고기"): ["한우 소머리국밥", "갈비탕", "곰탕"],
    ("일식", "비빔/볶음형", "만원 이상", "해산물"): ["카이센동", "회덮밥", "초밥"],
    ("중식", "국물형", "만원 이하", "채소"): ["짬뽕 (채수 베이스)", "울면", "기스면"],
    ("양식", "비빔/볶음형", "만원 이상", "면/빵"): ["알리오올리오", "까르보나라", "봉골레 파스타"],
    # ... 데이터가 없을 경우를 대비해 기본값 로직 추가 필요
}

def get_recommendation(q1, q2, q3, q4):
    key = (q1, q2, q3, q4)
    # DB에 정확한 키가 없을 경우 랜덤 추천 (데모용)
    if key in menu_db:
        return menu_db[key]
    else:
        # 간단한 매칭 로직 (랜덤 보정)
        defaults = [
            ["김치찌개", "된장찌개", "부대찌개"],
            ["돈까스", "치킨까스", "규카츠"],
            ["쌀국수", "팟타이", "나시고랭"],
            ["샌드위치", "샐러드", "포케"],
            ["짜장면", "짬뽕", "탕수육"]
        ]
        return random.choice(defaults)

# --- QUESTIONNAIRE FORM ---
with st.form("menu_form"):
    st.subheader("1. 어떤 스타일의 음식이 당기시나요?")
    q1 = st.selectbox("음식 종류", ["한식", "일식", "중식", "양식", "아시안"], label_visibility="collapsed")

    st.subheader("2. 선호하는 조리 형태는?")
    q2 = st.radio("식사 형태", ["국물형", "비빔/볶음형", "간편식(빵/면)"], horizontal=True, label_visibility="collapsed")

    st.subheader("3. 생각하시는 예산 범위는?")
    q3 = st.select_slider("가격대", options=["5천원 이하", "만원 이하", "만원 이상", "3만원 이상"])

    st.subheader("4. 선호하는 주재료는?")
    q4 = st.selectbox("재료 선택", ["고기", "해산물", "채소", "면/빵"], label_visibility="collapsed")

    submit_button = st.form_submit_button(label="메뉴 추천받기")

# --- RESULT DISPLAY ---
if submit_button:
    result = get_recommendation(q1, q2, q3, q4)
    
    st.balloons()
    
    st.markdown(f"""
        <div class="result-card">
            <p style="font-size: 1.2rem; color: #666;">오늘의 추천 메뉴는 바로...</p>
            <h1 class="recommend-title">{result[0]}</h1>
            <hr style="margin: 2rem 0;">
            <p style="font-size: 1rem; color: #888;">이런 음식은 어떠세요?</p>
            <div style="display: flex; justify-content: center; gap: 20px;">
                <span style="background: #eee; padding: 5px 15px; border-radius: 20px;"># {result[1]}</span>
                <span style="background: #eee; padding: 5px 15px; border-radius: 20px;"># {result[2]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 {q1} 기반의 {q2} 요리이며, 주재료인 {q4}의 풍미를 잘 느낄 수 있는 메뉴들입니다.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #aaa;'>Enjoy your meal!</p>", unsafe_allow_html=True)
