"""
Reusable UI components for the Crypto AI Agent dashboard
"""
import streamlit as st
from datetime import datetime
import time


def inject_css():
    """Inject custom CSS for glassmorphism and animations"""
    st.markdown("""
    <style>
        /* Root Variables */
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --accent: #ec4899;
            --success: #10b981;
            --danger: #ef4444;
            --dark-bg: #0f172a;
            --dark-secondary: #1e293b;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(148, 163, 184, 0.2);
        }

        /* Main Background */
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 50%, #2d1b69 100%);
            color: #f1f5f9;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 50%, #2d1b69 100%) !important;
        }

        /* Custom Container - Glassmorphism */
        .glass-container {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .glass-container:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(148, 163, 184, 0.3);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
            transform: translateY(-4px);
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .metric-card:hover {
            background: rgba(99, 102, 241, 0.1);
            border-color: rgba(99, 102, 241, 0.5);
            transform: scale(1.02);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
        }

        .metric-value {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 10px 0;
        }

        .metric-label {
            font-size: 13px;
            color: rgba(241, 245, 249, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .metric-change {
            font-size: 14px;
            font-weight: 600;
            margin-top: 8px;
        }

        .metric-change.positive {
            color: #10b981;
        }

        .metric-change.negative {
            color: #ef4444;
        }

        /* Chat Messages */
        .chat-message {
            display: flex;
            margin-bottom: 16px;
            animation: slideIn 0.3s ease;
        }

        .chat-message.user {
            justify-content: flex-end;
        }

        .chat-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.5;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }

        .chat-message.ai .chat-content {
            background: rgba(99, 102, 241, 0.15);
            border-color: rgba(99, 102, 241, 0.3);
            border-left: 3px solid #6366f1;
        }

        .chat-message.user .chat-content {
            background: rgba(99, 102, 241, 0.3);
            border-color: rgba(99, 102, 241, 0.5);
            border-right: 3px solid #6366f1;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            color: #f1f5f9 !important;
            border-radius: 10px !important;
            padding: 12px !important;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            background: rgba(30, 41, 59, 0.9) !important;
            border-color: rgba(99, 102, 241, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }

        /* Slider */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #6366f1, #ec4899);
        }

        /* Headers */
        h1 {
            background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -1px;
        }

        h2 {
            color: #f1f5f9;
            font-weight: 700;
            border-bottom: 2px solid rgba(99, 102, 241, 0.2);
            padding-bottom: 12px;
        }

        h3 {
            color: rgba(241, 245, 249, 0.9);
            font-weight: 600;
        }

        /* Animations */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }

        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
            }
            50% {
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
            }
        }

        .fade-in {
            animation: fadeIn 0.5s ease;
        }

        .loading-spinner {
            animation: pulse 1.5s ease-in-out infinite;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.5);
        }

        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(45, 27, 105, 0.5) 100%);
        }

        /* Streamlit Components Overrides */
        .stMetric {
            background: transparent !important;
        }

        /* Divider */
        hr {
            border: none !important;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
            margin: 20px 0 !important;
        }

    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render premium header with branding"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 48px; margin-bottom: 5px;">🚀 AI Crypto Analyst</h1>
            <p style="color: rgba(241, 245, 249, 0.7); font-size: 16px; letter-spacing: 1px;">
                Real-time AI-powered crypto insights powered by Gemma
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, change: str = None, icon: str = "📊"):
    """Render a single metric card with glassmorphism"""
    change_html = ""
    if change:
        change_class = "positive" if float(change.replace("%", "").replace("+", "")) >= 0 else "negative"
        change_sign = "📈" if float(change.replace("%", "").replace("+", "")) >= 0 else "📉"
        change_html = f'<div class="metric-change {change_class}">{change_sign} {change}</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 32px;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_title(title: str, icon: str = ""):
    """Render a section title with styling"""
    st.markdown(f"""
    <div style="margin: 30px 0 20px 0;">
        <h2 style="font-size: 24px;">{icon} {title}</h2>
    </div>
    """, unsafe_allow_html=True)


def render_separator():
    """Render a styled separator"""
    st.markdown("<hr>", unsafe_allow_html=True)


def render_loading_animation(message: str = "Loading..."):
    """Render loading animation with message"""
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div class="loading-spinner" style="display: inline-block; font-size: 40px; animation: pulse 1.5s ease-in-out infinite;">
            ⚡
        </div>
        <p style="color: rgba(241, 245, 249, 0.8); margin-top: 15px; font-size: 14px;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_confidence_score(score: float):
    """Render AI confidence score with visual indicator"""
    color = "#10b981" if score > 70 else "#f59e0b" if score > 40 else "#ef4444"
    
    st.markdown(f"""
    <div class="glass-container" style="text-align: center; margin: 10px 0;">
        <div style="font-size: 12px; color: rgba(241, 245, 249, 0.6); text-transform: uppercase; letter-spacing: 1px;">
            🧠 AI Confidence Score
        </div>
        <div style="
            font-size: 28px; 
            font-weight: 700; 
            color: {color}; 
            margin: 10px 0;
            text-shadow: 0 0 10px {color}40;
        ">
            {score}%
        </div>
        <div style="
            width: 100%;
            height: 6px;
            background: rgba(148, 163, 184, 0.2);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 10px;
        ">
            <div style="
                width: {score}%;
                height: 100%;
                background: linear-gradient(90deg, #6366f1, {color});
                border-radius: 3px;
                transition: width 0.5s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str, confidence: float = None):
    """Render a chat message with styling"""
    role_class = "user" if role == "user" else "ai"
    role_icon = "👤" if role == "user" else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {role_class}">
        <div class="chat-content">
            <span style="color: {('rgba(241, 245, 249, 0.7)' if role == 'user' else 'rgba(99, 102, 241, 0.8)')}; font-weight: 600; display: block; margin-bottom: 4px;">
                {role_icon} {'You' if role == 'user' else 'AI Analyst'}
            </span>
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if confidence and role == "ai":
        render_confidence_score(confidence)


def render_footer():
    """Render footer with branding"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 30px 0 20px 0;
        border-top: 1px solid rgba(99, 102, 241, 0.1);
        margin-top: 50px;
        color: rgba(241, 245, 249, 0.5);
        font-size: 12px;
    ">
        <p>
            ✨ Powered by <span style="color: #6366f1; font-weight: 600;">Gemma AI</span> 
            × <span style="color: #ec4899; font-weight: 600;">CoinGecko API</span> ✨
        </p>
        <p style="font-size: 11px; margin-top: 10px;">
            Real-time crypto analysis. Privacy-first. Local-first.
        </p>
    </div>
    """, unsafe_allow_html=True)
