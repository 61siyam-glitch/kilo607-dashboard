import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="لوحة تحكم الكيلو 607", layout="wide", page_icon="🏗️")

# المسار الجديد: الملف موجود في نفس مجلد الكود
DB_PATH = 'Project_607_DB.sqlite'

@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    df_reports = pd.read_sql_query("SELECT * FROM Daily_Reports", conn)
    conn.close()
    return df_reports

df = load_data()

st.markdown("""
<style>
    .stMetric { direction: rtl; text-align: right; }
    .stDataFrame { direction: rtl; }
</style>
""", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ لم يتم العثور على قاعدة البيانات. تأكد من رفع ملف Project_607_DB.sqlite في نفس المجلد.")
else:
    st.title("🏗️ لوحة التحكم التنفيذية - عبارة الكيلو 607")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي التقارير المسجلة", f"{len(df)} تقرير")
    col2.metric("قيمة العقد الإجمالية", "5.76 مليار جنيه")
    col3.metric("نسبة إنجاز الحديد", "65%", "المتبقي 35 طناً")
    
    st.markdown("---")
    st.subheader("📈 تحليل البيانات")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        challenges = df[df['Challenges'].notna() & (df['Challenges'] != 'لا توجد') & (df['Challenges'] != '')]
        if not challenges.empty:
            fig1 = px.pie(challenges, names='Challenges', title="أبرز التحديات في الموقع")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("لا توجد تحديات مسجلة.")

    with col_chart2:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        valid_dates = df.dropna(subset=['Date'])
        if not valid_dates.empty:
            fig2 = px.histogram(valid_dates, x='Date', title="تسلسل التقارير الزمني")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 سجل التقارير اليومية")
    st.dataframe(df, use_container_width=True)
