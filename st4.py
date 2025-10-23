import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import os

# # 한글 폰트 설정
# plt.rcParams['font.family'] = 'Noto Sans KR'
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# pd.set_option('display.max_columns', None)
# ✅ 폰트 경로 지정 (현재 디렉터리 기준)
font_path = os.path.join(os.path.dirname(__file__), "NotoSansKR-Regular.ttf")

if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    print(f"✅ 폰트 적용 완료: {fontprop.get_name()}")
else:
    print("⚠️ 폰트 파일을 찾을 수 없습니다. 기본 폰트로 진행합니다.")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False

# =============================
# 🎛️ 화면 기본 설정
# =============================
st.set_page_config(
    page_title="음식점 점포 위험 모니터링 대시보드",
    layout="wide",  # ✅ 가로 전체 확장
    initial_sidebar_state="expanded"
)

# =============================
# 🗂 데이터 불러오기
# =============================
@st.cache_data
def load_data():
    df = pd.read_csv("./배포용.csv")  # 파일 경로에 맞게 수정
    return df

df = load_data()

# ======================
# 🎛️ 사이드바
# ======================
st.sidebar.header("🏪 점포 선택")
selected_shop = st.sidebar.selectbox("가맹점구분번호", df["가맹점구분번호"].unique())
selected_df = df[df["가맹점구분번호"] == selected_shop].sort_values("기준년월")

min_date, max_date = selected_df["기준년월"].min(), selected_df["기준년월"].max()
start_date, end_date = st.sidebar.select_slider(
    "📆 분석 기간 선택",
    options=sorted(df["기준년월"].unique()),
    value=(min_date, max_date)
)
selected_df = selected_df[(selected_df["기준년월"] >= start_date) & (selected_df["기준년월"] <= end_date)]
latest = selected_df.iloc[-1]

# ======================
# 🧾 점포 기본정보
# ======================
# st.title("🍽 음식점 3개월 후 AI 위험 예측 대시보드")
# st.caption("※ 모든 위험 확률은 **3개월 뒤 리스크를 예측한 값**입니다.")

# info_cols = ['가맹점명', '가맹점지역', '업종', '상권']
# info_text = [f"**{col}**: {latest[col]}" for col in info_cols if col in latest]
# st.markdown(" | ".join(info_text))
# st.markdown("---")

# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     st.metric("📅 최근 기준월", latest["기준년월"])
# with col2:
#     st.metric("🧮 종합위험지수", f"{latest['종합위험지수']:.2f}")
# with col3:
#     st.metric("⚠️ 위험등급", latest["종합위험레벨"])
# with col4:
#     st.metric("🏪 군집", f"군집 {int(latest['cluster'])}")

# st.markdown("---")
# ======================
# 🧾 점포 기본정보 (중앙 정렬)
# ======================
     #    ※ 모든 위험 확률은 <b>3개월 뒤 리스크를 예측한 값</b>입니다.

st.markdown(
    """
    <h1 style='text-align:center;'>🍽 음식점 3개월 후 AI 위험 예측 대시보드</h1>
    <p style='text-align:center; font-size:16px; color:gray;'>
    <br>
    </p>
    """,
    unsafe_allow_html=True
)

# 점포 기본정보 중앙 정렬
info_cols = ['가맹점명', '가맹점지역', '업종', '상권']
info_text = [f"<b>{col}</b>: {latest[col]}" for col in info_cols if col in latest]
st.markdown(
    f"<p style='text-align:center; font-size:15px;'>{' | '.join(info_text)}</p>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# 메트릭 4개 중앙정렬
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📅 최근 기준월", latest["기준년월"])
with col2:
    st.metric("🧮 종합위험지수", f"{latest['종합위험지수']:.2f}")
with col3:
    st.metric("⚠️ 위험등급", latest["종합위험레벨"])
with col4:
    st.metric("🏪 군집", f"군집 {int(latest['cluster'])}")

st.markdown("<hr>", unsafe_allow_html=True)

# ======================
# 📉 주요 위험요인별 예측 확률
# ======================
st.subheader("  주요 위험요인별 예측 확률 (3개월 뒤 전망)")

left, right = st.columns([2.3, 1.1])

with left:
    risk_cols = ["p_신규", "p_매출", "p_재방문", "p_거주유동"]
    risk_labels = ["신규 고객 감소", "매출 하락", "재방문 하락", "유동인구 감소"]

    fig, ax = plt.subplots(figsize=(7.5, 3))
    bars = ax.bar(risk_labels, latest[risk_cols],
                  color=['#f4a261', '#e76f51', '#2a9d8f', '#457b9d'])
    for i, val in enumerate(latest[risk_cols]):
        ax.text(i, val + 0.02, f"{val:.2f}", ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.set_ylabel("예측 확률", fontsize=11)
    ax.set_title("AI가 예측한 3개월 후 주요 위험요인 확률", fontsize=13)
    st.pyplot(fig)

with right:
    st.markdown("##### 🧭 요약 진단")

    # st.markdown(f"""
    # **📊 종합위험지수:** `{latest['종합위험지수']:.2f}`  
    # **⚠️ 위험등급:** `{latest['종합위험레벨']}`  
    # ---
    # **가장 높은 리스크:**  
    # 👉 **{risk_labels[np.argmax(latest[risk_cols])]} ({latest[risk_cols].max():.2f})**
    
    # **가장 안정적인 지표:**  
    # 🟢 {risk_labels[np.argmin(latest[risk_cols])]} ({latest[risk_cols].min():.2f})
    
    # **📊 AI 해석:**  
    # - 값이 높을수록 3개월 뒤 리스크 확률 ↑  
    # - 0.5 이상이면 ‘주의 구간’으로 간주  
    # - 0.7 이상은 즉시 대응 필요 ⚠️
    # """)
    st.markdown(
    f"""
    <div style="font-size:16px; line-height:1.5">
    📊 종합위험지수: <b>{latest['종합위험지수']:.2f}</b><br>
    ⚠️ 위험등급: <b>{latest['종합위험레벨']}</b>
    <hr>
    가장 높은 리스크:<br>
    👉 <b>{risk_labels[np.argmax(latest[risk_cols])]} ({latest[risk_cols].max():.2f})</b><br><br>
    가장 안정적인 지표:<br>
    🟢 {risk_labels[np.argmin(latest[risk_cols])]} ({latest[risk_cols].min():.2f})<br><br>
    해석:<br>
    - 값이 높을수록 3개월 뒤 리스크 확률 ↑<br>
    - 0.5 이상이면 ‘주의 구간’으로 간주<br>
    - 0.7 이상은 즉시 대응 필요 ⚠️
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ======================
# 📊 업종별 평균 비교 분석
# ======================

st.subheader(f"  업종별 평균 위험 비교: {latest['업종']} 내 위치")

risk_cols_all = ["p_신규", "p_매출", "p_재방문", "p_거주유동", "종합위험지수"]
industry_df = df[df["업종"] == latest["업종"]]
industry_avg = industry_df[risk_cols_all].mean()

compare_df = pd.DataFrame({
    "지표": ["신규 고객 감소", "매출 하락", "재방문 하락", "유동인구 감소", "종합위험지수"],
    "내 점포": latest[risk_cols_all].values,
    "업종 평균": industry_avg.values
})

# 🔹 좌측 그래프 + 우측 인사이트 병렬 배치
col_left, col_right = st.columns([1.7, 1])

with col_left:
    fig, ax = plt.subplots(figsize=(7,3.5))  # ✅ 그래프 크기 살짝 축소
    width = 0.35
    x = np.arange(len(compare_df))
    ax.bar(x - width/2, compare_df["내 점포"], width, label="내 점포", color="#457b9d")
    ax.bar(x + width/2, compare_df["업종 평균"], width, label="업종 평균", color="#a6bddb")
    ax.set_xticks(x)
    ax.set_xticklabels(compare_df["지표"],  fontsize=9)
    ax.legend(fontsize=9, loc='upper right')
    ax.set_ylim(0, 1)
    ax.set_title(f"내 점포 vs 업종 평균 위험 비교", fontsize=12)
    st.pyplot(fig)

with col_right:
    gap = latest["종합위험지수"] - industry_avg["종합위험지수"]
    
    # 📊 인사이트 블록 - HTML로 보기 좋게 정렬
    if gap > 0.1:
        color = "#f94144"
        msg = f"🚨 업종 평균보다 **{gap:.2f}p 높습니다.** 경쟁 대비 리스크가 큰 상태입니다."
    elif gap < -0.1:
        color = "#2a9d8f"
        msg = f"✅ 업종 평균보다 **{abs(gap):.2f}p 낮습니다.** 상대적으로 안정적입니다."
    else:
        color = "#ffb12b"
        msg = "ℹ️ 업종 평균과 유사한 수준의 위험도를 보이고 있습니다."

    st.markdown(
        f"""
        <div style='font-size:16px; line-height:1.6;'>
            <b style='font-size:20px;'>🧩 업종 리스크 인사이트</b><br><br>
            <span style='color:{color}; font-weight:600;'>{msg}</span><br><br>
            🔸 <b>{latest['업종']}</b> 업종의 평균 종합위험지수는 
            <b>{industry_avg['종합위험지수']:.2f}</b> 입니다.<br>
            🔸 내 점포는 <b>{latest['종합위험지수']:.2f}</b> 로 { '조금 높은' if gap>0 else '비슷한' } 수준을 보입니다.<br><br>
        
  
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# =============================
# 🏪 군집 비교 인사이트
# =============================
st.subheader("🏪 군집별 위험 비교 인사이트")

# 군집 ID (현재 점포)
cluster_id = int(latest["cluster"])

# 군집별 평균 위험지수 계산
avg_cluster = (
    df.groupby("cluster")[["종합위험지수"] + risk_cols]
    .mean()
    .reset_index()
    .sort_values("cluster")
)

col1, col2 = st.columns([1.5, 1])

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))

    # ✅ 막대그래프: x축 0, 1, 2
    bars = ax.bar(
        avg_cluster["cluster"].astype(int),
        avg_cluster["종합위험지수"],
        color="#6baed6",
        alpha=0.8
    )

    # 내 점포 기준선
    my_score = latest["종합위험지수"]
    ax.axhline(my_score, color="red", linestyle="--", label="내 점포", linewidth=1.5)
    ax.legend()

        # ✅ 점선 오른쪽에 점수 표시
    xmax = avg_cluster["cluster"].max() + 0.2
    ax.text(
        xmax, my_score + 0.01,
        f"내 점포 {my_score:.2f}  ",
        color="red",
        fontsize=8,
        fontweight="bold",
        va="bottom",
        ha="left"
    )

    # ✅ x축 레이블 설정
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["군집 0", "군집 1", "군집 2"])
    ax.set_title("군집별 평균 위험지수 비교", fontsize=13)
    ax.set_xlabel("군집 번호")
    ax.set_ylabel("평균 위험지수")

    # ✅ 막대 위에 수치 표시
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.2f}",
                ha="center", va="bottom", fontsize=7)

    st.pyplot(fig)

with col2:
    st.markdown(f"#### 📍 현재 매장은 **군집 {cluster_id}** 에 속해 있습니다.")

    # ✅ 군집 번호를 정수로 포맷팅해서 표시
    df_display = avg_cluster.copy()
    df_display["cluster"] = df_display["cluster"].astype(int)

    # ✅ 표시용 데이터프레임 (cluster 컬럼 제외)
    df_display_show = df_display.drop(columns=["cluster"])

    st.dataframe(
        df_display_show.style.format("{:.2f}").highlight_max(color="#ffb048", axis=0),
        use_container_width=True
    )

    st.markdown("""
    **군집 해석 예시**
    - **군집 0️⃣** : 민감형 (2030 중심, 재방문 낮음)
    - **군집 1️⃣** : 안정형 (4060 중심, 재방문 높음)
    - **군집 2️⃣** : 신규오픈형 (전연령 신규 고객 중심)
    """)

st.markdown("---")



# ======================
# 📆 월별 추이 그래프 (버튼형)
# ======================
st.subheader("  월별 위험 추이 분석")

risk_options = {
    "종합위험지수": "종합위험지수",
    "매출 하락": "p_매출",
    "재방문 하락": "p_재방문",
    "신규 고객 감소": "p_신규",
    "유동인구 감소": "p_거주유동"
}

selected_label = st.radio(
    "🔍 분석할 요인을 선택하세요:",
    list(risk_options.keys()),
    horizontal=True,
    index=0
)
selected_col = risk_options[selected_label]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(selected_df["기준년월"], selected_df[selected_col],
        marker='o', color='#1f77b4', linewidth=2)
ax.set_ylim(0, 1)
ax.set_xlabel("기준년월")
ax.set_ylabel("예측확률" if selected_col != "종합위험지수" else "위험지수")
ax.set_title(f"월별 '{selected_label}' 추이 (3개월 후 예측)", fontsize=13)
plt.xticks(rotation=45, ha='right')
ax.grid(alpha=0.3)
st.pyplot(fig)

# =============================
# 💡 종합 인사이트
# =============================
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🎯 AI 종합 인사이트 (3개월 후 종합 진단)")
st.markdown("AI 모델이 주요 요인·업종 평균·군집 정보를 종합해 분석한 결과입니다.")

risk_level = latest["종합위험레벨"]
top_factor = risk_labels[np.argmax(latest[risk_cols])]
lowest_factor = risk_labels[np.argmin(latest[risk_cols])]
gap = latest["종합위험지수"] - industry_avg["종합위험지수"]

# ✅ 리스크 요약 텍스트 생성
summary = ""
action = ""

if risk_level == "매우 높음":
    summary = (
        f"현재 매장의 종합위험지수는 **{latest['종합위험지수']:.2f}** 로 매우 높은 수준입니다.\n\n"
        f"특히 **{top_factor}** 리스크가 뚜렷하며, 업종 평균보다 **{gap:+.2f}p 높습니다.**\n\n"
        "이는 상권 내 경쟁이 심화되고 고객 유지력이 약화된 신호입니다."
    )
    action = (
        "- 단골 고객 확보 및 재방문 이벤트 강화\n"
        "- 리뷰/후기 관리로 신뢰 회복\n"
        "- SNS·배달앱 등 외부 채널에서 신규 고객 유입 집중"
    )
    color = "error"

elif risk_level == "높음":
    summary = (
        f"매장의 종합위험지수는 **{latest['종합위험지수']:.2f}**이며,\n"
        f"업종 평균보다 **{gap:+.2f}p 높아 주의가 필요합니다.**\n\n"
        f"현재 주요 리스크 요인은 **{top_factor}**, 안정적인 항목은 **{lowest_factor}** 입니다."
    )
    action = (
        "- 고객 충성도 프로그램 및 포인트 적립 제도 도입\n"
        "- 업종 내 경쟁 매장과의 차별화 마케팅 기획\n"
        "- 매출 하락 구간 파악 후 집중 개선"
    )
    color = "warning"

elif risk_level == "보통":
    summary = (
        f"현재 위험 수준은 **보통({latest['종합위험지수']:.2f})**이며,\n"
        f"단기적 위험은 낮으나 추세 모니터링이 필요합니다.\n\n"
        f"{top_factor} 요인의 개선 여지가 있으며, 업종 평균과의 차이는 **{gap:+.2f}p** 입니다."
    )
    action = (
        "- 매출 변동이 큰 구간 중심으로 원인 점검\n"
        "- 신규 고객 확보 대비 재방문율 균형 유지\n"
        "- 업종 내 안정형 매장 벤치마킹 추천"
    )
    color = "info"

else:
    summary = (
        f"현재 매장은 **안정적({latest['종합위험지수']:.2f})**이며,\n"
        f"업종 평균 대비 **{abs(gap):.2f}p {'낮은' if gap < 0 else '비슷한'} 수준**입니다.\n\n"
        "모든 주요 요인이 안정 구간(0.5 이하)에 머물러 있습니다."
    )
    action = (
        "- 고객 경험 품질 유지 (서비스/맛/위생 등)\n"
        "- 단골 관리 및 지역 기반 고객 유지 전략 지속\n"
        "- 상권 변화(유동인구, 신규 매장 등) 정기 모니터링"
    )
    color = "success"

# ✅ Streamlit 블록으로 출력
if color == "error":
    st.error(summary)
elif color == "warning":
    st.warning(summary)
elif color == "info":
    st.info(summary)
else:
    st.success(summary)

# # ✍️ 액션 제안 블록 (줄바꿈 적용)
# st.markdown(
#     f"""
#     <div style='padding:15px 20px; border-left:5px solid #4B9CD3; background-color:#f8faff; border-radius:6px;'>
#         <p style='font-size:16px; line-height:1.7; font-family:Inter, sans-serif;'>
#         <b>💡 추천 대응 전략</b><br><br>
#         {'<br>'.join(action.split('\n'))}
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# ✍️ 액션 제안 블록 (줄바꿈 적용 + 다크모드 대응)
st.markdown(
    f"""
    <div style='
        padding:15px 20px;
        border-left:5px solid #4B9CD3;
        background-color:rgba(248,250,255,0.05);
        border-radius:6px;
        color:inherit;  /* ✅ 다크모드 글씨 유지 */
        '>
        <p style='
            font-size:16px;
            line-height:1.7;
            font-family:Inter, sans-serif;
            color:inherit;
        '>
        <b>💡 추천 대응 전략</b><br><br>
        {'<br>'.join(action.split('\n'))}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# 📊 하단 구분선 및 카피라이트
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("ⓒ 2025. AI 기반 음식점 리스크 모니터링 시스템")
