import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# إعدادات الصفحة
st.set_page_config(page_title="لوحة تحكم الكيلو 607", layout="wide", page_icon="🏗️")

# مسار قاعدة البيانات
DB_PATH = 'Project_607_DB.sqlite'

@st.cache_data
def load_all_data():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    
    # جلب البيانات من الجداول المختلفة
    df_reports = pd.read_sql_query("SELECT * FROM Daily_Reports ORDER BY Report_No", conn)
    df_phases = pd.read_sql_query("SELECT * FROM Payment_Phases ORDER BY Phase_No", conn)
    df_walls = pd.read_sql_query("SELECT * FROM Wall_Execution_Sequence ORDER BY Exec_Sequence", conn)
    df_boq = pd.read_sql_query("SELECT * FROM BOQ_Items", conn)
    
    conn.close()
    return df_reports, df_phases, df_walls, df_boq

data = load_all_data()

# تنسيق عربي (RTL) للواجهة
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

    st.title("🏗️ لوحة القيادة التنفيذية - عبارة الكيلو 607")
    st.markdown("---")

    # ==========================================
    # 1. المؤشرات الرئيسية (KPIs)
    # ==========================================
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي التقارير", f"{len(df_reports)} تقرير")
    col2.metric("قيمة العقد الإجمالية", "5.76 مليار جنيه")
    # حساب المبلغ المدفوع من جدول المراحل
    paid_amount = df_phases[df_phases['Status'] == 'Paid']['Net_Amount'].sum()
    col3.metric("المبلغ المدفوع (المعادل)", f"{paid_amount:,.0f} جنيه")
    col4.metric("نسبة إنجاز الحديد", "65%", "المتبقي 35 طناً")
    
    st.markdown("---")

    # ==========================================
    # 2. البيانات المالية وخريطة الحوائط
    # ==========================================
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💰 الموقف المالي للمراحل")
        # رسم بياني للمراحل
        fig_fin = px.bar(df_phases, x='Phase_No', y='Net_Amount', 
                         title="صافي الصرفية لكل مرحلة",
                         labels={'Phase_No': 'رقم المرحلة', 'Net_Amount': 'المبلغ (جنيه)'},
                         color='Status', color_discrete_map={'Paid': 'green', 'Pending': 'orange'})
        st.plotly_chart(fig_fin, use_container_width=True)
        
    with col_right:
        st.subheader("🧱 خريطة حالة الحوائط (التسلسل التنفيذي)")
        st.dataframe(df_walls, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ==========================================
    # 3. تحليل الكميات (BOQ) والتحديات
    # ==========================================
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📦 الكميات المتبقية (أهم البنود)")
        # فلترة بنود معينة لعرضها
        boq_filtered = df_boq[df_boq['Item_No'].isin(['104', '404', '409'])]
        fig_boq = px.bar(boq_filtered, x='Description', y=['Executed_Qty', 'Remaining_Qty'], 
                         title="المنفذ مقابل المتبقي", barmode='group')
        st.plotly_chart(fig_boq, use_container_width=True)

    with col_chart2:
        st.subheader("⚠️ أبرز التحديات")
        challenges = df_reports[df_reports['Challenges'].notna() & (df_reports['Challenges'] != 'لا توجد') & (df_reports['Challenges'] != '')]
        if not challenges.empty:
            fig_chal = px.pie(challenges, names='Challenges', title="توزيع التحديات")
            st.plotly_chart(fig_chal, use_container_width=True)
        else:
            st.info("لا توجد تحديات مسجلة.")

    st.markdown("---")

    # ==========================================
    # 4. سجل التقارير اليومية
    # ==========================================
    st.subheader("📋 سجل التقارير اليومية")
    st.dataframe(df_reports, use_container_width=True, hide_index=True)
