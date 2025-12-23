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
    /* Main Background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header Style */
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

    /* Card Design */
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

    /* Form Design */
    .stSelectbox label, .stRadio label {
        font-weight: 600 !important;
        color: #333 !important;
    }

    /* Button Customization */
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
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">🍽️ 오늘 뭐 먹지?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">4개의 질문으로 당신의 취향에 딱 맞는 한 끼를 추천합니다.</p>', unsafe_allow_html=True)

# --- DATASET ---
# (Category, Style, Budget, Ingredient): [Recommended, Similar1, Similar2]
MENU_DATA = {
    ("한식", "국물 요리", "1만원 이하", "고기"): ["순대국", "뼈해장국", "돼지국밥"],
    ("한식", "국물 요리", "1만원 이하", "해산물"): ["동태탕", "순두부찌개", "꽃게탕"],
    ("한식", "볶음/비빔 요리", "1만원 이하", "고기"): ["제육볶음", "불고기 덮밥", "비빔밥"],
    ("한식", "국물 요리", "1만원 이상", "고기"): ["갈비탕", "소고기 수육 전골", "한우 소머리국밥"],
    ("한식", "볶음/비빔 요리", "1만원 이상", "해산물"): ["아구찜", "해물찜", "낙지볶음"],
    
    ("일식", "볶음/비빔 요리", "1만원 이상", "해산물"): ["사케동(연어덮밥)", "초밥 세트", "카이센동"],
    ("일식", "볶음/비빔 요리", "1만원 이하", "고기"): ["가츠동", "규동", "돈까스"],
    ("일식", "면 요리", "1만원 이하", "면/빵"): ["돈코츠 라멘", "우동", "메밀소바"],
    ("일식", "면 요리", "1만원 이상", "고기"): ["스테이크 덮밥", "스키야키", "샤브샤브"],
    
    ("중식", "국물 요리", "1만원 이하", "고기/해산물"): ["짬뽕", "우육면", "마라탕"],
    ("중식", "볶음/비빔 요리", "1만원 이하", "면/빵"): ["짜장면", "볶음밥", "잡채밥"],
    ("중식", "볶음/비빔 요리", "1만원 이상", "고기"): ["꿔바로우", "유린기", "깐풍기"],
    
    ("양식", "면 요리", "1만원 이상", "면/빵"): ["봉골레 파스타", "해산물 리조또", "라자냐"],
    ("양식", "볶음/비빔 요리", "1만원 이상", "고기"): ["안심 스테이크", "함박 스테이크", "폭립"],
    ("양식", "면 요리", "1만원 이하", "면/빵"): ["클럽 샌드위치", "치즈 버거", "핫도그"],
    ("양식", "볶음/비빔 요리", "1만원 이하", "채소"): ["리코타 치즈 샐러드", "그릭 샐러드", "시저 샐러드"],
}

# --- QUESTIONNAIRE ---
with st.container():
    st.markdown("### 📝 선호도 조사")
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.selectbox("1. 선호하는 음식 종류", ["한식", "일식", "중식", "양식"])
    with col2:
        q2 = st.selectbox("2. 선호하는 조리 스타일", ["국물 요리", "볶음/비빔 요리", "면 요리"])
        
    col3, col4 = st.columns(2)
    with col3:
        q3 = st.radio("3. 예상 가격대", ["1만원 이하", "1만원 이상"], horizontal=True)
    with col4:
        q4 = st.selectbox("4. 핵심 재료", ["고기", "해산물", "채소", "면/빵"])

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("내 맞춤 메뉴 확인하기")

# --- LOGIC & DISPLAY ---
if submit:
    # 1. 완벽 매칭 시도
    user_key = (q1, q2, q3, q4)
    recommendations = MENU_DATA.get(user_key)
    
    # 2. 완벽 매칭이 없을 경우 (부분 매칭 로직)
    if not recommendations:
        # 음식 종류와 재료만으로 필터링 시도
        filtered = [v for k, v in MENU_DATA.items() if k[0] == q1 and k[3] == q4]
        if filtered:
            recommendations = random.choice(filtered)
        else:
            # 아예 없을 경우 음식 종류만이라도 맞춤
            filtered_by_type = [v for k, v in MENU_DATA.items() if k[0] == q1]
            recommendations = random.choice(filtered_by_type) if filtered_by_type else ["김치찌개", "된장찌개", "순두부찌개"]

    st.markdown("---")
    st.balloons()
    
    # 결과 카드 출력
    st.markdown(f"""
        <div class="result-card">
            <div style="color: #FF4B4B; font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">Recommended for You</div>
            <div style="color: #888; font-size: 0.9rem; margin-bottom: 5px;">당신의 취향과 딱 맞는 추천 메뉴는?</div>
            <div class="menu-name">{recommendations[0]}</div>
            <div style="margin: 30px 40px; border-bottom: 1px solid #F0F0F0;"></div>
            <div style="color: #666; font-size: 0.85rem; font-weight: 500; margin-bottom: 15px;">유사한 스타일의 다른 음식 추천</div>
            <div>
                <span class="similar-badge"># {recommendations[1]}</span>
                <span class="similar-badge"># {recommendations[2]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 분석 요약 정보
    st.info(f"선택하신 조건: **{q1} · {q2} · {q3} · {q4}**")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: #CCC; font-size: 0.8rem; letter-spacing: 0.5px;">
        AI 기반 개인 맞춤형 식단 큐레이션 서비스<br>
        <b>HAPPY MEAL MOMENT</b>
    </div>
""", unsafe_allow_html=True)
