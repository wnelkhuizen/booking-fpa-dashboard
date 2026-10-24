import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration (Booking.com Styling)
st.set_page_config(
    page_title="Booking.com | FP&A Storytelling Dashboard",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for Booking.com look & feel
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        color: #1a1a1a;
    }
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #003580 !important;
        color: white !important;
        border-radius: 4px;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #00224f !important;
        color: white !important;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #003580;
        color: #1a1a1a;
    }
    .metric-card h4 {
        color: #555555;
        margin-bottom: 5px;
    }
    .metric-card h2 {
        color: #003580;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Load Local CSV Dataset
@st.cache_data
def load_data():
    file_path = "booking_q3_financials.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"File '{file_path}' not found in current folder.")
        st.stop()

df = load_data()

# Header
st.title("✈️ Booking.com — FP&A Storytelling & Insights Engine")
st.markdown("*Innovation & Process Automation Proof-of-Concept for Planning & Analytics*")
st.divider()

# Sidebar Controls
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/be/Booking.com_logo.svg", width=200)
st.sidebar.header("Dashboard Controls")
selected_quarter = st.sidebar.selectbox("Select Quarter", df["Quarter"].unique(), index=2)
openai_api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", help="Enter key for live GPT-4o analysis, or use built-in response.")

filtered_df = df[df["Quarter"] == selected_quarter]

# 3. KPI Metrics
col1, col2, col3, col4 = st.columns(4)
total_gross = filtered_df["Gross_Bookings_MUSD"].sum()
total_rev = filtered_df["Revenue_MUSD"].sum()
avg_margin = filtered_df["EBITDA_Margin_Pct"].mean()

with col1:
    st.markdown(f"<div class='metric-card'><h4>Gross Bookings</h4><h2>${total_gross:,.0f} M</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h4>Total Revenue</h4><h2>${total_rev:,.0f} M</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h4>Avg EBITDA Margin</h4><h2>{avg_margin:.1f}%</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h4>Active Segments</h4><h2>{len(filtered_df)}</h2></div>", unsafe_allow_html=True)

st.write("")

# 4. Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Segment ($M)")
    fig_rev = px.bar(
        filtered_df, 
        x="Segment", 
        y="Revenue_MUSD", 
        color="Segment",
        text_auto=True,
        color_discrete_sequence=["#003580", "#006ce4", "#008009", "#ffb700"]
    )
    fig_rev.update_layout(showlegend=False, plot_bgcolor="white")
    st.plotly_chart(fig_rev, use_container_width=True)

with col_right:
    st.subheader("EBITDA Margin Trend (%)")
    fig_margin = px.line(
        df, 
        x="Quarter", 
        y="EBITDA_Margin_Pct", 
        color="Segment",
        markers=True,
        color_discrete_sequence=["#003580", "#006ce4", "#008009", "#ffb700"]
    )
    fig_margin.update_layout(plot_bgcolor="white")
    st.plotly_chart(fig_margin, use_container_width=True)

st.divider()

# 5. AI Storytelling Module
st.subheader("🤖 AI Executive Narrative Generator")
st.write("Convert raw financial rows into an executive summary with a single click.")

if st.button("Generate Executive Storyline (AI)"):
    with st.spinner("Analyzing financial bottlenecks and performance trends..."):
        if openai_api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_api_key)
                
                prompt = f"""
                You are VP FP&A at Booking.com. Analyze this financial dataset for {selected_quarter}:
                {filtered_df.to_string()}

                Write a concise executive summary in 3 distinct sections:
                1. Highlights: What drives top-line growth?
                2. Margin Pressure & Bottlenecks: Where are margins declining and why?
                3. Strategic Recommendations: 3 actionable steps for executive management.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                ai_output = response.choices[0].message.content
            except Exception as e:
                st.error(f"API Error: {e}")
                ai_output = None
        else:
            acc_rev = filtered_df[filtered_df['Segment'] == 'Accommodations']['Revenue_MUSD'].values[0]
            ai_output = (
                f"### Executive Financial Summary — {selected_quarter}\n\n"
                f"**1. Strong Top-line Momentum**\n"
                f"Accommodations continues to be the primary growth engine for Booking.com with record revenue of "
                f"**${acc_rev:,.0f}M** and a solid EBITDA margin of **36.1%**. Travel demand across EMEA and APAC remains strong.\n\n"
                f"**2. Margin Pressure in Flights & Car Rentals**\n"
                f"While Gross Bookings expand, EBITDA margins show a notable contraction in **Flight Tickets (4.8%)** and "
                f"**Car Rentals (9.5%)**. Key cost drivers include rising Customer Acquisition Costs (CAC) via performance marketing "
                f"and manual dispute resolution overheads.\n\n"
                f"**3. Strategic Recommendations for Management**\n"
                f"* **Automate Dispute Handling:** Deploy AI process automation in Car Rentals to eliminate manual dispute overhead and lower OPEX.\n"
                f"* **Optimize Marketing Efficiency:** Re-align performance marketing spend for Flights to push segment margins back above 7%.\n"
                f"* **Drive High-Margin Cross-Selling:** Leverage high-margin momentum in Attractions & Experiences (19.8%) via targeted mobile app cross-sells."
            )

        if ai_output:
            st.success("Analysis complete!")
            st.markdown(ai_output)

# Raw Data Inspection
with st.expander("View Raw Financial Dataset"):
    st.dataframe(df, use_container_width=True)