import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.express as px
from db.connection import get_engine
from analysis.queries import top_students_per_subject, department_averages, at_risk_students

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Analyzer",
    page_icon="🎓",
    layout="wide"
)

# ─── Header ─────────────────────────────────────────────────────────────────
st.title("🎓 STUDENT PERFORMANCE ANALYZER")
st.markdown("A real-time dashboard powered by PostgreSQL & Pandas")
st.divider()

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

# ─── KPI Cards ──────────────────────────────────────────────────────────────
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Departments",
    value=len(dept_df)
)
col2.metric(
    label="Overall Avg Score",
    value=f"{dept_df['avg_score'].mean():.1f}"
)
col3.metric(
    label="⚠️ At-Risk Students",
    value=len(at_risk_df)
)

st.divider()

# ─── Department Averages ────────────────────────────────────────────────────
st.subheader("🏫 Average Score by Department")

col_left, col_right = st.columns([2, 1])

with col_left:
    fig = px.bar(
        dept_df,
        x="department",
        y="avg_score",
        color="avg_score",
        color_continuous_scale="Oranges",
        labels={"department": "Department", "avg_score": "Average Score"},
        text_auto=".1f"
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.dataframe(
        dept_df.rename(columns={
            "department": "Dept",
            "avg_score": "Avg Score",
            "num_students": "Students"
        }),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ─── Top Students Per Subject ───────────────────────────────────────────────
st.subheader("📊 Top 3 Students Per Subject")

subjects = top_df["subject"].unique().tolist()
selected_subject = st.selectbox("Filter by Subject:", ["All"] + subjects)

filtered_df = top_df if selected_subject == "All" else top_df[top_df["subject"] == selected_subject]

fig2 = px.bar(
    filtered_df,
    x="name",
    y="score",
    color="subject",
    barmode="group",
    labels={"name": "Student", "score": "Score"},
    text_auto=".1f"
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─── At-Risk Students ───────────────────────────────────────────────────────
st.subheader("⚠️ At-Risk Students")

threshold = st.slider("Set At-Risk Threshold (Avg Score below):", 30, 80, 50)
at_risk_df = at_risk_students(engine, threshold=threshold)

if at_risk_df.empty:
    st.success("✅ No at-risk students found for this threshold!")
else:
    st.warning(f"{len(at_risk_df)} student(s) are below the threshold of {threshold}")
    st.dataframe(
        at_risk_df.rename(columns={
            "name": "Student",
            "department": "Department",
            "avg_score": "Avg Score"
        }),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ─── Footer ─────────────────────────────────────────────────────────────────
st.caption("Built with Streamlit · PostgreSQL · Pandas · Plotly")