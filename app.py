import streamlit as st
import time
from datetime import datetime, timedelta
import random
from agent import analyze_crypto
from data import get_coin_price, get_top_movers, get_trending_coins, get_market_summary
from ui_components import (
    inject_css, render_header, render_metric_card, render_section_title,
    render_separator, render_loading_animation, render_chat_message, render_footer
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Crypto Analyst",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_coin" not in st.session_state:
    st.session_state.selected_coin = "bitcoin"

if "time_range" not in st.session_state:
    st.session_state.time_range = 7

# ============================================================================
# INJECT CUSTOM STYLING
# ============================================================================
inject_css()

# ============================================================================
# SIDEBAR - NAVIGATION & CONTROLS
# ============================================================================
st.sidebar.markdown("""
<div class="glass-container" style="margin-bottom: 20px;">
    <h3 style="text-align: center; margin-top: 0;">⚙️ Dashboard Controls</h3>
</div>
""", unsafe_allow_html=True)

# Cryptocurrency Selection
st.sidebar.markdown("<div style='font-weight: 600; color: rgba(241, 245, 249, 0.8); margin: 15px 0 8px 0;'>🪙 Select Cryptocurrency</div>", unsafe_allow_html=True)
coin_options = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Solana": "solana",
    "Polkadot": "polkadot",
    "Ripple": "ripple",
    "Dogecoin": "dogecoin",
    "Binance Coin": "binancecoin"
}

selected_coin_name = st.sidebar.selectbox(
    label="Select cryptocurrency",
    options=coin_options.keys(),
    label_visibility="collapsed",
    key="coin_select"
)
st.session_state.selected_coin = coin_options[selected_coin_name]

# Time Range Slider
st.sidebar.markdown("<div style='font-weight: 600; color: rgba(241, 245, 249, 0.8); margin: 20px 0 8px 0;'>📅 Time Range (Days)</div>", unsafe_allow_html=True)
st.session_state.time_range = st.sidebar.slider(
    label="Select time range",
    min_value=1,
    max_value=90,
    value=st.session_state.time_range,
    step=1,
    label_visibility="collapsed"
)

# Analysis Button
st.sidebar.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

if st.sidebar.button("🔍 Analyze Market", use_container_width=True):
    st.session_state.trigger_analysis = True

# Additional Info
st.sidebar.markdown("""
<div class="glass-container" style="margin-top: 30px; text-align: center;">
    <div style="font-size: 12px; color: rgba(241, 245, 249, 0.6);">
        <p>✅ Real-time data from CoinGecko</p>
        <p>🧠 Local AI analysis</p>
        <p>🔒 Privacy-first architecture</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
render_header()

# ============================================================================
# METRICS SECTION
# ============================================================================
render_section_title("📊 Market Snapshot", icon="📈")

try:
    # Fetch live data
    coin_data = get_coin_price(st.session_state.selected_coin)
    market_summary = get_market_summary()
    
    if coin_data and "error" in coin_data:
        st.warning(f"⚠️ {coin_data['error']}")
    elif coin_data and "price" in coin_data:
        # Create 4-column metric layout
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_metric_card(
                label="Current Price",
                value=f"${coin_data['price']:,.2f}",
                icon="💰"
            )
        
        with col2:
            change_pct = coin_data.get('change', 0)
            change_str = f"{'+' if change_pct >= 0 else ''}{change_pct}%"
            render_metric_card(
                label="24h Change",
                value=f"{change_str}",
                change=f"{change_str}",
                icon="📊"
            )
        
        with col3:
            render_metric_card(
                label="Market Status",
                value="ACTIVE",
                icon="🟢"
            )
        
        with col4:
            render_metric_card(
                label="Last Updated",
                value=datetime.now().strftime("%H:%M"),
                icon="🕐"
            )
    else:
        st.info("📊 Unable to load market data")
except Exception as e:
    st.error(f"Error fetching market data: {str(e)}")

render_separator()

# ============================================================================
# TOP MOVERS SECTION
# ============================================================================
render_section_title("🚀 Top Movers", icon="🎯")

try:
    movers = get_top_movers(limit=3)
    
    if movers and "error" in movers:
        st.warning(f"⚠️ {movers['error']}")
    elif movers and "gainers" in movers:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div style='margin-bottom: 10px;'><strong style='color: #10b981;'>📈 Top Gainers</strong></div>", unsafe_allow_html=True)
            for gainer in movers["gainers"]:
                st.markdown(f"""
                <div class="glass-container" style="margin-bottom: 10px; padding: 12px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>{gainer['name']}</span>
                        <span style="color: #10b981; font-weight: 600;">+{gainer['change']:.2f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='margin-bottom: 10px;'><strong style='color: #ef4444;'>📉 Top Losers</strong></div>", unsafe_allow_html=True)
            for loser in movers["losers"]:
                st.markdown(f"""
                <div class="glass-container" style="margin-bottom: 10px; padding: 12px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>{loser['name']}</span>
                        <span style="color: #ef4444; font-weight: 600;">{loser['change']:.2f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📊 No movers data available")
except Exception as e:
    st.error(f"Error loading movers: {str(e)}")

render_separator()

# ============================================================================
# TRENDING COINS SECTION
# ============================================================================
render_section_title("📰 Trending Now", icon="🔥")

try:
    trending = get_trending_coins()
    
    if isinstance(trending, dict) and "error" in trending:
        st.warning(f"⚠️ {trending['error']}")
    elif isinstance(trending, list) and len(trending) > 0:
        cols = st.columns(5)
        for idx, coin in enumerate(trending):
            with cols[idx]:
                st.markdown(f"""
                <div class="glass-container" style="text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 8px;">🪙</div>
                    <div style="font-weight: 600; font-size: 14px;">{coin.get('name', 'Unknown')}</div>
                    <div style="color: rgba(241, 245, 249, 0.6); font-size: 12px;">{coin.get('symbol', '?').upper()}</div>
                    <div style="color: #6366f1; font-weight: 600; font-size: 13px; margin-top: 8px;">Rank #{coin.get('rank', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📰 No trending data available")
except Exception as e:
    st.error(f"Error loading trending: {str(e)}")

render_separator()

# ============================================================================
# AI ANALYSIS SECTION
# ============================================================================
render_section_title("🤖 AI Analysis & Chat", icon="💬")

# Display chat history
chat_container = st.container()

with chat_container:
    for role, content in st.session_state.chat_history:
        with st.container():
            if role == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                    <div class="glass-container" style="max-width: 70%; background: rgba(99, 102, 241, 0.3); border-color: rgba(99, 102, 241, 0.5); border-right: 3px solid #6366f1;">
                        <span style="font-weight: 600; color: #6366f1;">👤 You</span><br>
                        {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 16px; animation: slideIn 0.3s ease;">
                    <div class="glass-container" style="max-width: 70%; background: rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.3); border-left: 3px solid #6366f1;">
                        <span style="font-weight: 600; color: #6366f1;">🤖 AI Analyst</span><br>
                        {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input(
    placeholder="Ask about crypto trends, prices, market sentiment... 🚀",
    key="chat_input"
)

if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))
    
    # Show loading animation
    with st.spinner(""):
        render_loading_animation("🧠 Analyzing market with AI...")
        time.sleep(0.5)
        
        # Get AI response
        response = analyze_crypto(user_input)
        
        # Generate confidence score (70-95%)
        confidence = random.randint(72, 94)
        
        # Add AI response
        st.session_state.chat_history.append(("ai", response))
    
    # Rerun to show the new message
    st.rerun()

render_separator()

# ============================================================================
# FOOTER
# ============================================================================
render_footer()

# ============================================================================
# CUSTOM ANIMATIONS & EFFECTS
# ============================================================================
st.markdown("""
<style>
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
</style>
""", unsafe_allow_html=True)