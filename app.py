import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="FP&A Variance Assistant", page_icon="📊", layout="wide")
st.title("📊 AI-Powered FP&A Variance Assistant")
st.caption("Upload your budget vs actual CSV — get instant variance analysis and AI-generated commentary.")
st.divider()

uploaded_file = st.file_uploader("Upload your CSV file (required columns: Department, Budget, Actual)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Variance ($)"] = df["Actual"] - df["Budget"]
    df["Variance (%)"] = ((df["Variance ($)"] / df["Budget"]) * 100).round(1)
    df["Status"] = df["Variance ($)"].apply(lambda x: "⚠️ Over Budget" if x > 0 else "✅ Under Budget")
    st.subheader("Variance Summary Table")
    st.dataframe(df.style.format({"Budget": "${:,.0f}", "Actual": "${:,.0f}", "Variance ($)": "${:,.0f}", "Variance (%)": "{:.1f}%"}), use_container_width=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"${df['Budget'].sum():,.0f}")
    col2.metric("Total Actual", f"${df['Actual'].sum():,.0f}")
    total_var = df["Variance ($)"].sum()
    col3.metric("Net Variance", f"${abs(total_var):,.0f}", delta=f"{'Over' if total_var > 0 else 'Under'} budget", delta_color="inverse")
    st.divider()
    st.subheader("Budget vs Actual by Department")
    df_melted = df.melt(id_vars="Department", value_vars=["Budget", "Actual"], var_name="Type", value_name="Amount")
    fig = px.bar(df_melted, x="Department", y="Amount", color="Type", barmode="group", color_discrete_map={"Budget": "#4A90D9", "Actual": "#E85D5D"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    fig.update_yaxes(tickprefix="$", tickformat=",")
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.subheader("AI-Generated Variance Commentary")
    st.caption("Click below to generate executive-ready commentary for your finance report.")
    if st.button("✨ Generate Commentary", type="primary"):
        with st.spinner("AI is analyzing your variances..."):
            variance_text = df[["Department", "Budget", "Actual", "Variance ($)", "Variance (%)"]].to_string(index=False)
            prompt = f"""You are a senior FP&A analyst. Write professional variance commentary for each department below, flag risks, note favorable variances, and end with a 2-sentence executive summary.\n\nData:\n{variance_text}"""
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            commentary = response.choices[0].message.content
            st.markdown("### Commentary")
            st.write(commentary)
            st.divider()
            st.download_button(label="📥 Download Commentary as .txt", data=commentary, file_name="variance_commentary.txt", mime="text/plain")