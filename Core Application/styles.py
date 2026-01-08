
# ============================================================================
# LBO MODEL - STREAMLIT STYLING & CSS
# The Mountain Path - World of Finance
# ============================================================================

import streamlit as st
from config import COLORS, FONTS

def apply_mountain_path_styles():
    """Apply Mountain Path design system to Streamlit app"""
    
    css = f"""
    <style>
    /* ===== GLOBAL STYLES ===== */
    :root {{
        --primary-color: {COLORS['dark_blue']};
        --secondary-color: {COLORS['light_blue']};
        --accent-color: {COLORS['accent_gold']};
        --text-color: #333;
        --light-bg: {COLORS['light_gray']};
    }}
    
    * {{
        font-family: {FONTS['family']};
    }}
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark_blue']} 0%, {COLORS['light_blue']} 100%);
        color: white;
    }}
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        padding: 1.5rem;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: white;
    }}
    
    [data-testid="stSidebar"] h3 {{
        color: {COLORS['accent_gold']};
        font-weight: bold;
        letter-spacing: 1px;
    }}
    
    /* ===== HEADER SECTION ===== */
    .header-container {{
        background: linear-gradient(135deg, {COLORS['dark_blue']} 0%, {COLORS['light_blue']} 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 5px solid {COLORS['accent_gold']};
        box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);
    }}
    
    .header-container h1 {{
        color: white;
        margin: 0;
        font-size: {FONTS['sizes']['title']}px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    .header-container h2 {{
        font-size: {FONTS['sizes']['subtitle']}px;
        opacity: 0.95;
        color: white;
        margin: 10px 0 0 0;
    }}
    
    .header-subtitle {{
        font-weight: bold;
        color: {COLORS['accent_gold']};
        margin-top: 12px;
        font-size: {FONTS['sizes']['subheading']}px;
        letter-spacing: 1px;
    }}
    
    /* ===== METRIC CARDS ===== */
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['light_blue']}15 0%, {COLORS['accent_gold']}05 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {COLORS['dark_blue']};
        box-shadow: 0 2px 8px rgba(0, 51, 102, 0.1);
    }}
    
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['dark_blue']};
        margin: 8px 0;
    }}
    
    .metric-label {{
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}
    
    /* ===== TABS ===== */
    [data-testid="stTabs"] {{
        margin: 1.5rem 0;
    }}
    
    [data-testid="stTabs"] [aria-selected="true"] {{
        border-bottom: 3px solid {COLORS['dark_blue']};
        color: {COLORS['dark_blue']};
    }}
    
    /* ===== INPUT SECTIONS ===== */
    .input-section {{
        background: {COLORS['light_gray']};
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {COLORS['accent_gold']};
        margin-bottom: 1rem;
    }}
    
    .input-header {{
        background: {COLORS['accent_gold']};
        color: {COLORS['dark_blue']};
        padding: 10px 15px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
    }}
    
    /* ===== TABLE STYLING ===== */
    .dataframe {{
        border-radius: 10px;
        border: 1px solid #ddd;
    }}
    
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    
    th {{
        background: {COLORS['dark_blue']};
        color: white;
        padding: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    
    td {{
        padding: 10px 12px;
        border-bottom: 1px solid #e0e0e0;
    }}
    
    tr:hover {{
        background-color: {COLORS['light_gray']};
    }}
    
    /* ===== BUTTONS ===== */
    .stButton > button {{
        background: {COLORS['dark_blue']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['light_blue']};
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.3);
    }}
    
    /* ===== SLIDERS ===== */
    .stSlider {{
        margin: 15px 0;
    }}
    
    /* ===== ALERTS & INFO BOXES ===== */
    .stInfo {{
        background: {COLORS['light_blue']}15;
        border-left: 4px solid {COLORS['light_blue']};
        border-radius: 5px;
    }}
    
    .stSuccess {{
        background: {COLORS['success']}15;
        border-left: 4px solid {COLORS['success']};
        border-radius: 5px;
    }}
    
    .stWarning {{
        background: {COLORS['warning']}15;
        border-left: 4px solid {COLORS['warning']};
        border-radius: 5px;
    }}
    
    /* ===== FOOTER ===== */
    .footer-container {{
        text-align: center;
        padding: 30px 20px;
        margin-top: 3rem;
        border-top: 2px solid {COLORS['dark_blue']};
        background: {COLORS['light_gray']};
        border-radius: 10px;
    }}
    
    .footer-title {{
        color: {COLORS['dark_blue']};
        font-weight: bold;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }}
    
    .footer-links {{
        margin: 15px 0;
    }}
    
    .footer-links a {{
        text-decoration: none;
        color: {COLORS['dark_blue']};
        font-weight: 600;
        margin: 0 15px;
        transition: color 0.3s ease;
    }}
    
    .footer-links a:hover {{
        color: {COLORS['accent_gold']};
    }}
    
    .footer-credit {{
        color: #999;
        font-size: 0.8rem;
        margin-top: 15px;
    }}
    
    /* ===== EXPANDABLE SECTIONS ===== */
    .expander {{
        border: 1px solid #ddd;
        border-radius: 8px;
        background: {COLORS['light_gray']};
    }}
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 640px) {{
        .header-container {{
            padding: 1.5rem;
        }}
        
        .header-container h1 {{
            font-size: 1.5rem;
        }}
        
        .metric-card {{
            margin-bottom: 1rem;
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def create_box(title, content_func, box_type='info'):
    """
    Create styled information boxes
    
    Parameters:
    -----------
    title : str
        Box title
    content_func : callable
        Function that renders content
    box_type : str
        'info', 'success', 'warning', 'danger'
    """
    color_map = {
        'info': COLORS['light_blue'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
    }
    
    color = color_map.get(box_type, color_map['info'])
    
    html = f"""
    <div style="
        background-color: {color}15;
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h4 style="color: {color}; margin-top: 0;">{title}</h4>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    content_func()
