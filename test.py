import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="모금 KPI 대시보드", layout="wide")

# --- 사이드바 필터 ---
st.sidebar.title("필터")
campaign = st.sidebar.selectbox("캠페인", ["정기후원 전환", "연말모금", "긴급구호"])
channels = st.sidebar.multiselect("채널", ["Email","SNS","Ads","Offline"], ["Email","SNS"])
window = st.sidebar.slider("최근 N일", 7, 90, 30)

# 샘플 데이터 생성
rng = pd.date_range(end=pd.Timestamp.today().normalize(), periods=window)
np.random.seed(42)
df = pd.DataFrame({
    "date": rng,
    "donations": np.random.poisson(lam=120, size=len(rng)) + np.linspace(0, 30, len(rng)),
    "visitors": np.random.randint(800, 1500, size=len(rng)),
})
df["conv_rate"] = (df["donations"] / df["visitors"]).round(3)

tab1, tab2 = st.tabs(["📈 KPI", "🗺️ 현장 이벤트"])

with tab1:
    k1, k2, k3 = st.columns(3)
    k1.metric("총 기부 건수", int(df["donations"].sum()), delta=f"{int(df['donations'].iloc[-1]-df['donations'].iloc[-2])}건")
    k2.metric("방문자", int(df["visitors"].sum()))
    k3.metric("전환율(평균)", f"{(df['conv_rate'].mean()*100):.1f} %")

    st.line_chart(df.set_index("date")[["donations","visitors"]])

    with st.expander("지표 정의 보기"):
        st.markdown("""
        - **donations**: 일별 기부 건수  
        - **visitors**: 랜딩 페이지 일 방문자 수  
        - **conv_rate**: donations / visitors
        """)

with tab2:
    st.write("최근 오프라인 이벤트 위치(샘플)")
    loc = pd.DataFrame({
        "lat": [37.5665, 35.1796, 35.1595],
        "lon": [126.9780, 129.0756, 126.8526],
        "label": ["서울 시청", "부산 시청", "광주 시청"]
    })
    st.map(loc)
    st.image("https://placehold.co/800x200?text=Campaign+Banner")

c1, c2 = st.columns(2)
if c1.button("데이터 동기화"):
    bar = st.progress(0, text="동기화 중...")
    for i in range(100):
        time.sleep(0.01)
        bar.progress(i+1, text="동기화 중...")
    bar.empty()
    st.toast("동기화 완료! ✅")
    st.session_state.last_sync = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

if "last_sync" not in st.session_state:
    st.session_state.last_sync = "아직 없음"
c2.write(f"마지막 동기화: {st.session_state.last_sync}")