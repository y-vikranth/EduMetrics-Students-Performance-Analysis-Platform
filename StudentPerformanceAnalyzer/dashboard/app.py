import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.express as px
from db.connection import get_engine
from analysis.queries import top_students_per_subject, department_averages, at_risk_students

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Analyzer Horizon",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS for Premium Look ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Dynamic Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #09090b 0%, #18181b 100%);
        color: #fafafa;
    }
    
    /* Header Gradient Text */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    h1 {
        background: linear-gradient(120deg, #c084fc, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: hue-rotate 5s linear infinite alternate;
    }
    
    @keyframes hue-rotate {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(30deg); }
    }
    
    /* Metrics Glassmorphism */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetric"] {
        background: rgba(24, 24, 27, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.4);
    }
    
    /* Hide specific streamlit elements to make it look like a standalone app */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(24, 24, 27, 0.5);
        padding: 10px 20px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: transparent;
        border-radius: 8px;
        color: #a1a1aa;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #fff !important;
        background: rgba(255, 255, 255, 0.1) !important;
        box-shadow: inset 0 -2px 0 0 #38bdf8 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #e4e4e7;
    }
    
    /* Dataframes enhancement */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ─── DB Connection ──────────────────────────────────────────────────────────
@st.cache_resource
def load_engine():
    return get_engine()

engine = load_engine()

# ─── Load Data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    top     = top_students_per_subject(engine)
    dept    = department_averages(engine)
    at_risk = at_risk_students(engine)
    return top, dept, at_risk

top_df, dept_df, at_risk_df = load_data()

# ─── Header Section ──────────────────────────────────────────────────────────
st.markdown("<h1>✨ Student Analytics Horizon</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #a1a1aa; font-size: 1.1rem; margin-bottom: 2rem;'>Intelligent insights into academic performance powered by <strong>PostgreSQL</strong> & <strong>Pandas</strong></p>", unsafe_allow_html=True)

# ─── KPI Cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Departments", value=len(dept_df))
with col2:
    st.metric(label="Overall Avg Score", value=f"{dept_df['avg_score'].mean():.1f}")
with col3:
    total_students = int(dept_df['num_students'].sum()) if 'num_students' in dept_df else "N/A"
    st.metric(label="Students Tracked", value=total_students)
with col4:
    st.metric(label="⚠️ At-Risk Students", value=len(at_risk_df))

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Department Overview", "🥇 Honors Board", "⚠️ Risk Interventions"])

with tab1:
    st.markdown("### 🏫 Academic Performance by Department")
    st.markdown("<p style='color: #71717a;'>Compare average scores and identify top performing domains.</p>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1], gap="large")
    
    with col_left:
        fig = px.bar(
            dept_df,
            x="department",
            y="avg_score",
            color="avg_score",
            color_continuous_scale="Purpor",
            labels={"department": "Department", "avg_score": "Average Score"},
            text_auto=".1f",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20, l=0, r=0, b=0),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Avg Score"),
            coloraxis_showscale=False,
            font=dict(family="Outfit", color="#a1a1aa")
        )
        fig.update_traces(marker_line_width=0, opacity=0.85, hovertemplate="%{x}: <b>%{y}</b><extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            dept_df.rename(columns={
                "department": "Dept",
                "avg_score": "Avg Score",
                "num_students": "Students"
            }),
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.markdown("### 🌟 Top Performers by Subject")
    st.markdown("<p style='color: #71717a;'>Highlighting the highest achievers in individual courses.</p>", unsafe_allow_html=True)
    
    subjects = top_df["subject"].unique().tolist()
    
    filter_col, empty_col = st.columns([1, 3])
    with filter_col:
        selected_subject = st.selectbox("Select Dimension:", ["Global / All Subjects"] + subjects)
    
    selected_subject_filter = "All" if "Global" in selected_subject else selected_subject
    filtered_df = top_df if selected_subject_filter == "All" else top_df[top_df["subject"] == selected_subject_filter]
    
    if selected_subject_filter == "All":
        fig2 = px.bar(
            filtered_df,
            x="name",
            y="score",
            color="subject",
            barmode="group",
            labels={"name": "Student", "score": "Score", "subject": "Subject"},
            text_auto=".1f",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    else:
        fig2 = px.bar(
            filtered_df,
            x="name",
            y="score",
            color="score",
            color_continuous_scale="Tealgrn",
            labels={"name": "Student", "score": "Score"},
            text_auto=".1f",
            template="plotly_dark"
        )

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        coloraxis_showscale=False,
        font=dict(family="Outfit", color="#a1a1aa")
    )
    fig2.update_traces(marker_line_width=0, opacity=0.9)
    
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("### 🚨 Intervention Dashboard")
    st.markdown("<p style='color: #71717a;'>Identify students requiring academic assistance and support.</p>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.markdown("<div style='padding:20px; background:rgba(239,68,68,0.1); border-left: 4px solid #ef4444; border-radius: 8px;'>", unsafe_allow_html=True)
        threshold = st.slider("🎯 Set Risk Threshold (Avg Score <):", 30, 80, 50, help="Any student with an average below this mark will be flagged.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    at_risk_dyn_df = at_risk_students(engine, threshold=threshold)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if at_risk_dyn_df.empty:
        st.markdown('''
        <div style="background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.5); padding: 20px; border-radius: 12px; text-align: center;">
            <h3 style="color: #4ade80; margin: 0;">✅ All clear!</h3>
            <p style="color: #a1a1aa; margin: 5px 0 0 0;">No students fall below the specified threshold.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.3); padding: 15px 20px; border-radius: 12px; margin-bottom: 20px;">
            <strong style="color: #f87171;">⚠️ Alert:</strong> {len(at_risk_dyn_df)} student(s) identified for academic intervention.
        </div>
        ''', unsafe_allow_html=True)
        
        st.dataframe(
            at_risk_dyn_df.rename(columns={
                "name": "Student Name",
                "department": "Department",
                "avg_score": "Current Avg Score"
            }),
            use_container_width=True,
            hide_index=True
        )

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("<br><br><p style='text-align: center; color: #52525b; font-size: 0.9rem;'>Powered by Antigravity · Streamlit & Plotly</p>", unsafe_allow_html=True)
