import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="لوحة تحكم الكيلو 607", layout="wide", page_icon="🏗️")

DB_PATH = 'Project_607_DB.sqlite'

@st.cache_data
def load_all_data():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    df_reports = pd.read_sql_query("SELECT * FROM Daily_Reports ORDER BY Report_No", conn)
    df_phases = pd.read_sql_query("SELECT * FROM Payment_Phases ORDER BY Phase_No", conn)
    df_walls = pd.read_sql_query("SELECT * FROM Wall_Execution_Sequence ORDER BY Exec_Sequence", conn)
    df_boq = pd.read_sql_query("SELECT * FROM BOQ_Items", conn)
    conn.close()
    return df_reports, df_phases, df_walls, df_boq

data = load_all_data()

st.markdown("""
<style>
    .stMetric { direction: rtl; text-align: right; }
    .stDataFrame { direction: rtl; }
    h1, h2, h3 { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)

if data is None:
    st.error("⚠️ لم يتم العثور على قاعدة البيانات. تأكد من رفع الملف.")
else:
    df_reports, df_phases, df_walls, df_boq = data

    df_walls_ar = df_walls.rename(columns={
        'Exec_Sequence': 'التسلسل', 'Wall_Name': 'اسم الحائط', 
        'Direction': 'الاتجاه', 'Current_Status': 'الحالة'
    })
    
    df_phases_ar = df_phases.rename(columns={
        'Phase_No': 'المرحلة', 'Net_Amount': 'المبلغ الصافي', 'Status': 'الحالة'
    })

    st.title("🏗️ لوحة القيادة التنفيذية - عبارة الكيلو 607")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي التقارير", f"{len(df_reports)} تقرير")
    col2.metric("قيمة العقد الإجمالية", "5.76 مليار جنيه")
    paid_amount = df_phases[df_phases['Status'] == 'Paid']['Net_Amount'].sum()
    col3.metric("المبلغ المدفوع (المعادل)", f"{paid_amount:,.0f} جنيه")
    col4.metric("نسبة إنجاز الحديد", "65%", "المتبقي 35 طناً")
    
    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("💰 الموقف المالي للمراحل")
        fig_fin = px.bar(df_phases_ar, x='المرحلة', y='المبلغ الصافي', 
                         title="صافي الصرفية لكل مرحلة",
                         color='الحالة', color_discrete_map={'Paid': 'green', 'Pending': 'orange'})
        st.plotly_chart(fig_fin, use_container_width=True)
        
    with col_right:
        st.subheader("🧱 خريطة حالة الحوائط (التسلسل التنفيذي)")
        st.dataframe(df_walls_ar, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📋 سجل التقارير اليومية")
    st.dataframe(df_reports, use_container_width=True, hide_index=True)
