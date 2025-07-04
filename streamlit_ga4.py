import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GA4 데이터 시각화", layout="wide")
st.title("GA4 데이터 자동 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV 파일이 성공적으로 업로드되었습니다.")

    # 데이터가 너무 많으면 샘플링
    if len(df) > 2000:
        st.warning(f"데이터가 {len(df)}행으로 많아, 1000행만 무작위로 샘플링하여 시각화합니다.")
        df = df.sample(n=1000, random_state=42)

    if st.button("시각화 그래프 만들기"):
        # date 컬럼 날짜형 변환
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception:
                pass

        # 1. 소스/매체별 세션 트렌드 (line chart)
        if set(['date', 'sessions', 'source_medium']).issubset(df.columns):
            st.subheader("1. 소스/매체별 세션 트렌드 (Line Chart)")
            fig1 = px.line(df, x='date', y='sessions', color='source_medium', markers=True,
                           title='소스/매체별 세션 트렌드')
            st.plotly_chart(fig1, use_container_width=True)

        # 2. 신규/기존 사용자 비율 (stacked bar chart)
        if set(['date', 'users', 'new_users']).issubset(df.columns):
            st.subheader("2. 신규/기존 사용자 비율 (Stacked Bar Chart)")
            df['기존사용자'] = df['users'] - df['new_users']
            users_melt = df.melt(id_vars=['date'], value_vars=['new_users', '기존사용자'],
                                 var_name='사용자구분', value_name='수')
            fig2 = px.bar(users_melt, x='date', y='수', color='사용자구분',
                          title='신규/기존 사용자 비율', barmode='stack')
            st.plotly_chart(fig2, use_container_width=True)

        # 3. 퍼널 단계별 사용자수 (bar chart)
        if set(['event_name', 'users']).issubset(df.columns):
            st.subheader("3. 퍼널 단계별 사용자수 (Bar Chart)")
            funnel_df = df.groupby('event_name', as_index=False)['users'].sum()
            fig3 = px.bar(funnel_df, x='event_name', y='users',
                          title='퍼널 단계별 사용자수')
            st.plotly_chart(fig3, use_container_width=True)

        # 4. 기기별 세션 비교 (bar chart)
        if set(['device_category', 'sessions']).issubset(df.columns):
            st.subheader("4. 기기별 세션 비교 (Bar Chart)")
            device_df = df.groupby('device_category', as_index=False)['sessions'].sum()
            fig4 = px.bar(device_df, x='device_category', y='sessions',
                          title='기기별 세션 비교')
            st.plotly_chart(fig4, use_container_width=True)

        st.info("그래프는 ga4_mock_dataset.csv의 칼럼 구조에 맞춰 자동 생성됩니다.")
else:
    st.info("CSV 파일을 먼저 업로드해주세요.")