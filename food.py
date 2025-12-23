import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="오늘 뭐 먹지? | 맞춤 메뉴 추천", 
    page_icon="🍲", 
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
        background-color: #F9F9F9;
        border: 1px solid #EEEEEE;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 1.5rem;
    }
    
    .menu-name {
        font-size: 2.2rem;
        color: #FF4B4B;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .similar-badge {
        display: inline-block;
        background-color: #FFE5E5;
        color: #FF4B4B;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 5px;
    }

    /* Button Customization */
    div.stButton > button {
        background-color: #1E1E1E;
        color: white;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #FF4B4B;
        color: white;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">🍽️ 오늘 뭐 먹지?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">당신의 취향을 분석해 최적의 한 끼를 추천합니다.</p>', unsafe_allow_html=True)

# --- DATASET ---
# (Category, Style, Budget, Ingredient): [Recommended, Similar1, Similar2]
MENU_DATA = {
    ("한식", "국물 요리", "1만원 이하", "고기"): ["순대국", "뼈해장국", "돼지국밥"],
    ("한식", "볶음/비빔 요리", "1만원 이하", "고기"): ["제육볶음", "불고기 덮밥", "비빔밥"],
    ("한식", "국물 요리", "1만원 이상", "고기"): ["갈비탕", "소고기 전골", "곰탕"],
    ("한식", "국물 요리", "1만원 이하", "해산물"): ["해물라면", "동태탕", "순두부찌개"],
    
    ("일식", "볶음/비빔 요리", "1만원 이상", "해산물"): ["사케동", "초밥 세트", "카이센동"],
    ("일식", "볶음/비빔 요리", "1만원 이하", "고기"): ["가츠동", "규동", "돈까스"],
    ("일식", "면 요리", "1만원 이하", "면/빵"): ["라멘", "우동", "소바"],
    
    ("중식", "국물 요리", "1만원 이하", "고기/해산물"): ["짬뽕", "우육면", "마라탕"],
    ("중식", "볶음/비빔 요리", "1만원 이하", "면/빵"): ["짜장면", "볶음밥", "잡채밥"],
    ("중식", "볶음/비빔 요리", "1만원 이상", "고기"): ["꿔바로우", "유린기", "깐풍기"],
    
    ("양식", "면 요리", "1만원 이상", "면/빵"): ["파스타", "리조또", "라자냐"],
    ("양식", "볶음/비빔 요리", "1만원 이상", "고기"): ["스테이크", "함박 스테이크", "치킨 커틀릿"],
    ("양식", "면 요리", "1만원 이하", "면/빵"): ["샌드위치", "파니니", "버거"],
}

# Default categories for fallback
FALLBACK_GROUPS = [
    ["김치찌개", "된장찌개", "부대찌개"],
    ["샤브샤브", "스키야키", "밀푀유나베"],
    ["닭갈비", "찜닭", "치킨"],
    ["마라탕", "꿔바로우", "양꼬치"]
]

# --- QUESTIONNAIRE ---
with st.container():
    st.info("아래 질문에 답변해 주세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.selectbox("1. 선호하는 음식 종류", ["한식", "일식", "중식", "양식"])
    with col2:
        q2 = st.selectbox("2. 선호하는 조리 스타일", ["국물 요리", "볶음/비빔 요리", "면 요리"])
        
    col3, col4 = st.columns(2)
    with col3:
        q3 = st.selectbox("3. 예상 가격대", ["1만원 이하", "1만원 이상"])
    with col4:
        q4 = st.selectbox("4. 핵심 재료", ["고기", "해산물", "채소", "면/빵"])

    submit = st.button("내 취향에 맞는 메뉴 찾기")

# --- LOGIC & DISPLAY ---
if submit:
    # 매칭되는 데이터 찾기
    user_key = (q1, q2, q3, q4)
    # 완벽 매칭이 없는 경우를 대비해 일부 조건만으로 필터링하거나 랜덤 추천
    recommendations = MENU_DATA.get(user_key)
    
    if not recommendations:
        # 간단한 매칭이 안될 경우 카테고리별 랜덤 추천
        recommendations = random.choice(FALLBACK_GROUPS)

    st.markdown("---")
    st.balloons()
    
    # 결과 카드 출력
    st.markdown(f"""
        <div class="result-card">
            <div style="color: #888; font-weight: 500; margin-bottom: 10px;">당신을 위한 추천 메뉴</div>
            <div class="menu-name">{recommendations[0]}</div>
            <div style="margin: 25px 0; border-bottom: 1px solid #EEE;"></div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 15px;">이런 메뉴도 비슷해요!</div>
            <div>
                <span class="similar-badge"># {recommendations[1]}</span>
                <span class="similar-badge"># {recommendations[2]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"선택하신 '{q1} / {q2} / {q3} / {q4}' 조합을 바탕으로 엄선했습니다.")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #BBB; font-size: 0.8rem;">
        © 2024 AI Menu Recommender | 맛있는 식사 되세요!
    </div>
""", unsafe_allow_html=True)
