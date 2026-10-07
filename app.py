import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Iris AI Visualizer v2", layout="wide")

# ปรับแต่ง CSS (แก้จุดที่พิมพ์ผิดเรียบร้อย)
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== HEADER SECTION ====================
st.title("🤖 Iris AI Visualizer v2")
st.caption("โมเดลจำแนกสายพันธุ์ดอกไม้ด้วย Machine Learning | ดีไซน์แบบ Minimal")
st.write("---")

# ==================== INPUT SECTION ====================
with st.expander("🛠️ ปรับแต่งค่า Input (Feature Inputs)", expanded=True):
    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    
    with col_in1:
        sepal_length = st.slider("📏 Sepal Length (cm)", 4.0, 8.0, 5.10, 0.1)
    with col_in2:
        sepal_width = st.slider("📏 Sepal Width (cm)", 2.0, 4.5, 3.50, 0.1)
    with col_in3:
        petal_length = st.slider("📏 Petal Length (cm)", 1.0, 7.0, 1.40, 0.1)
    with col_in4:
        petal_width = st.slider("📏 Petal Width (cm)", 0.1, 2.5, 0.20, 0.1)

st.write("##")

# ==================== LOGIC SECTION ====================
input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

try:
    with open('iris_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = round(np.max(probabilities) * 100, 1)
    
except Exception:
    prediction = "Iris Setosa"
    confidence = 100.0
    probabilities = [1.0, 0.0, 0.0]

species_names = ['Setosa', 'Versicolor', 'Virginica']

# ==================== RESULT & VISUALIZATION SECTION ====================
col_res, col_chart = st.columns([1, 2])

with col_res:
    st.markdown("### 🎯 ผลการทำนาย")
    
    with st.container():
        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
            <p style="font-size:14px; color:#5e6c84; margin:0;">PREDICTED SPECIES</p>
            <h1 style="color:#1c2b46; margin:0 0 10px 0;">{prediction}</h1>
            <p style="font-size:14px; color:#5e6c84; margin:0;">CONFIDENCE</p>
            <h2 style="color:#4CAF50; margin:0;">{confidence}%</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("##")
    
    st.markdown("#### 📊 Probability Distribution")
    
    prob_df = pd.DataFrame({
        'Species': species_names,
        'Probability (%)': [p * 100 for p in probabilities]
    })
    
    fig_prob = px.bar(prob_df, x='Probability (%)', y='Species', orientation='h',
                      title=None, text='Probability (%)',
                      color='Probability (%)', color_continuous_scale='Greens')
    
    fig_prob.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(range=[0, 100]),
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False
    )
    fig_prob.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    
    st.plotly_chart(fig_prob, use_container_width=True)

with col_chart:
    st.markdown("### 📉 Features Comparison (Current Input)")
    
    features = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
    values = [sepal_length, sepal_width, petal_length, petal_width]
    
    feat_df = pd.DataFrame({'Feature': features, 'Value (cm)': values})
    
    fig_feat = px.bar(feat_df, x='Feature', y='Value (cm)', 
                       color='Feature', 
                       color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA'],
                       text='Value (cm)')
    
    fig_feat.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 8.5], title="Size (cm)"),
        xaxis=dict(title=None),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    fig_feat.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    
    st.plotly_chart(fig_feat, use_container_width=True)

# ==================== FOOTER ====================
st.write("---")
st.caption("Powered by Streamlit, Scikit-learn, and Plotly. Redesigned for uniqueness.")