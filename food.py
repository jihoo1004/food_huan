import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="오늘 뭐 먹지? | 맞춤 메뉴 추천", 
    page_icon="🍽️", 
    layout="centered"
)

# --- STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E1E1E;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #666666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #ffffff;
        border: 2px solid #F0F0F0;
        padding: 2.5rem;
        border-radius: 24px;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .menu-name {
        font-size: 2.5rem;
        color: #FF4B4B;
        font-weight: 800;
        margin: 15px 0;
    }
    .similar-badge {
        display: inline-block;
        background-color: #F8F9FA;
        color: #555555;
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 6px;
        border: 1px solid #EAEAEA;
    }
    div.stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 14px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        border: none;
        width: 100%;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    div.stButton > button:hover {
        background-color: #E63946;
        color: white;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">🍽️ 오늘 뭐 먹지?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">당신의 답변을 분석하여 최고의 한 끼를 제안합니다.</p>', unsafe_allow_html=True)

# --- EXPANDED DATASET ---
# (Category, Style, Budget, Ingredient): [Recommended, Similar1, Similar2]
MENU_DATA = {
    # 한식 (Korean)
    ("한식", "든든한 국물", "1만원 이하", "고기"): ["순대국", "뼈해장국", "돼지국밥"],
    ("한식", "든든한 국물", "1만원 이하", "해산물"): ["동태탕", "순두부찌개", "바지락칼국수"],
    ("한식", "든든한 국물", "1만원 이상", "고기"): ["갈비탕", "한우곰탕", "소고기전골"],
    ("한식", "든든한 국물", "1만원 이상", "해산물"): ["해물탕", "전복삼계탕", "연포탕"],
    ("한식", "매콤한 볶음/비빔", "1만원 이하", "고기"): ["제육볶음", "불고기덮밥", "비빔밥"],
    ("한식", "매콤한 볶음/비빔", "1만원 이상", "해산물"): ["아구찜", "낙지볶음", "주꾸미볶음"],
    ("한식", "가벼운 식사", "1만원 이하", "채소"): ["보리밥뷔페", "산채비빔밥", "묵사발"],
    ("한식", "가벼운 식사", "1만원 이하", "면/빵"): ["잔치국수", "비빔국수", "수제비"],

    # 일식 (Japanese)
    ("일식", "든든한 국물", "1만원 이하", "면/빵"): ["돈코츠 라멘", "우동", "소바"],
    ("일식", "든든한 국물", "1만원 이상", "고기"): ["스키야키", "샤브샤브", "모츠나베"],
    ("일식", "매콤한 볶음/비빔", "1만원 이하", "고기"): ["가츠동", "규동", "부타동"],
    ("일식", "매콤한 볶음/비빔", "1만원 이상", "해산물"): ["사케동", "특초밥", "카이센동"],
    ("일식", "가벼운 식사", "1만원 이하", "해산물"): ["회덮밥", "텐동", "오니기리"],

    # 중식 (Chinese)
    ("중식", "든든한 국물", "1만원 이하", "해산물"): ["짬뽕", "울면", "기스면"],
    ("중식", "든든한 국물", "1만원 이상", "고기"): ["우육면", "훠궈", "마라탕"],
    ("중식", "매콤한 볶음/비빔", "1만원 이하", "면/빵"): ["짜장면", "볶음밥", "마파두부덮밥"],
    ("중식", "매콤한 볶음/비빔", "1만원 이상", "고기"): ["꿔바로우", "유린기", "깐풍기"],

    # 양식 (Western)
    ("양식", "가벼운 식사", "1만원 이하", "면/빵"): ["클럽 샌드위치", "치즈버거", "베이글"],
    ("양식", "매콤한 볶음/비빔", "1만원 이상", "면/빵"): ["아라비아따 파스타", "해산물 리조또", "라자냐"],
    ("양식", "든든한 국물", "1만원 이상", "고기"): ["비프 스튜", "어니언 스프", "크림 파스타"],
    ("양식", "매콤한 볶음/비빔", "1만원 이상", "고기"): ["안심 스테이크", "폭립", "함박 스테이크"],
    ("양식", "가벼운 식사", "1만원 이하", "채소"): ["리코타 치즈 샐러드", "그릭 샐러드", "포케"],
}

# --- QUESTIONNAIRE ---
with st.container():
    st.markdown("### 📝 맞춤형 질문지")
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.selectbox("1. 어떤 종류의 음식이 끌리나요?", ["한식", "일식", "중식", "양식"])
    with col2:
        q2 = st.selectbox("2. 선호하는 식사 스타일은?", ["든든한 국물", "매콤한 볶음/비빔", "가벼운 식사"])
        
    col3, col4 = st.columns(2)
    with col3:
        q3 = st.radio("3. 예산 범위를 선택해 주세요.", ["1만원 이하", "1만원 이상"], horizontal=True)
    with col4:
        q4 = st.selectbox("4. 선호하는 주재료는?", ["고기", "해산물", "채소", "면/빵"])

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("결과 보기")

# --- LOGIC & DISPLAY ---
if submit:
    user_key = (q1, q2, q3, q4)
    recommendations = MENU_DATA.get(user_key)
    
    # 데이터가 없을 경우를 위한 스마트 폴백(Fallback) 로직
    if not recommendations:
        # 카테고리(q1)와 재료(q4)가 일치하는 것 중 랜덤 선택
        matches = [v for k, v in MENU_DATA.items() if k[0] == q1 and k[3] == q4]
        if not matches:
            # 카테고리(q1)만 일치하는 것 중 선택
            matches = [v for k, v in MENU_DATA.items() if k[0] == q1]
            
        recommendations = random.choice(matches) if matches else ["김치찌개", "된장찌개", "순두부찌개"]

    st.markdown("---")
    st.balloons()
    
    st.markdown(f"""
        <div class="result-card">
            <div style="color: #FF4B4B; font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">Recommended for You</div>
            <div style="color: #888; font-size: 0.9rem; margin-bottom: 5px;">당신을 위한 맞춤 메뉴 추천</div>
            <div class="menu-name">{recommendations[0]}</div>
            <div style="margin: 30px 40px; border-bottom: 1px solid #F0F0F0;"></div>
            <div style="color: #666; font-size: 0.85rem; font-weight: 500; margin-bottom: 15px;">이 메뉴와 비슷한 유형의 추천</div>
            <div>
                <span class="similar-badge"># {recommendations[1]}</span>
                <span class="similar-badge"># {recommendations[2]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"📍 분석 결과: **{q1}** 카테고리에서 **{q4}**를 활용한 **{q2}** 스타일의 메뉴입니다.")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: #CCC; font-size: 0.8rem; letter-spacing: 0.5px;">
        AI 기반 개인 맞춤형 식단 큐레이션 서비스<br>
        <b>HAPPY MEAL MOMENT</b>
    </div>
""", unsafe_allow_html=True)
