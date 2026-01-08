# ============================================================================
# LBO MODEL - REUSABLE STREAMLIT COMPONENTS
# The Mountain Path - World of Finance
# ============================================================================

import streamlit as st
from config import COLORS, BRANDING

def hero_header(title, subtitle="", show_branding=True):
    """
    Create professional hero header
    
    Parameters:
    -----------
    title : str
        Main title
    subtitle : str
        Subtitle text
    show_branding : bool
        Whether to show company branding
    """
    header_html = f"""
    <div class="header-container">
        <h1>{title}</h1>
        {f'<h2>{subtitle}</h2>' if subtitle else ''}
        {f'''<div class="header-subtitle">
            {BRANDING['icon']} {BRANDING['name']}<br>
            {BRANDING['instructor']} | {BRANDING['experience']}
        </div>''' if show_branding else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def sidebar_header():
    """Create branded sidebar header"""
    sidebar_html = f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 2px solid {COLORS['accent_gold']};
    ">
        <h2 style="color: {COLORS['accent_gold']}; margin: 0;">
            {BRANDING['icon']} THE MOUNTAIN PATH
        </h2>
        <p style="color: white; font-size: 0.85rem; margin: 5px 0 0 0;">
            World of Finance
        </p>
    </div>
    """
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)


def metric_card(label, value, delta=None, delta_color="normal", icon=""):
    """
    Create styled metric card
    
    Parameters:
    -----------
    label : str
        Metric label
    value : str
        Metric value
    delta : str, optional
        Change value
    delta_color : str
        'normal', 'inverse', 'off'
    icon : str
        Emoji icon
    """
    delta_html = ""
    if delta:
        delta_html = f"""
        <div style="
            color: {COLORS['success'] if '+' in str(delta) else COLORS['danger']};
            font-size: 0.9rem;
            font-weight: 600;
        ">{delta}</div>
        """
    
    html = f"""
    <div class="metric-card">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def metric_row(metrics_data):
    """
    Create row of metric cards
    
    Parameters:
    -----------
    metrics_data : list of dict
        List of metric dictionaries with keys: label, value, delta, delta_color, icon
    """
    cols = st.columns(len(metrics_data))
    
    for col, metric in zip(cols, metrics_data):
        with col:
            metric_card(
                label=metric.get('label', ''),
                value=metric.get('value', ''),
                delta=metric.get('delta'),
                delta_color=metric.get('delta_color', 'normal'),
                icon=metric.get('icon', '')
            )


def input_section(title, icon=""):
    """
    Create styled input section header
    
    Parameters:
    -----------
    title : str
        Section title
    icon : str
        Emoji icon
    """
    html = f"""
    <div class="input-header">
        {icon} {title}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def data_table(df, title="", show_index=True, format_currency=None):
    """
    Create styled data table
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to display
    title : str
        Table title
    show_index : bool
        Show index column
    format_currency : list
        Columns to format as currency
    """
    if title:
        st.markdown(f"<h3 style='color: {COLORS['dark_blue']};'>{title}</h3>", 
                   unsafe_allow_html=True)
    
    # Format columns if specified
    styled_df = df.copy()
    if format_currency:
        for col in format_currency:
            if col in styled_df.columns:
                styled_df[col] = styled_df[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(styled_df, use_container_width=True)


def footer():
    """Create professional footer"""
    footer_html = f"""
    <div class="footer-container">
        <div class="footer-title">
            {BRANDING['icon']} {BRANDING['name']}
        </div>
        
        <div class="footer-links">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank">
                🔗 LinkedIn Profile
            </a>
            <a href="https://github.com/trichyravis" target="_blank">
                💻 GitHub Repository
            </a>
        </div>
        
        <div class="footer-credit">
            © 2026 <b>{BRANDING['instructor']}</b>. All rights reserved.<br>
            Empowering the next generation of Finance Professionals.
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def info_box(title, description, icon="ℹ️"):
    """
    Create information box
    
    Parameters:
    -----------
    title : str
        Box title
    description : str
        Box description
    icon : str
        Emoji icon
    """
    html = f"""
    <div style="
        background-color: {COLORS['light_blue']}15;
        border-left: 4px solid {COLORS['light_blue']};
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h4 style="color: {COLORS['light_blue']}; margin-top: 0;">
            {icon} {title}
        </h4>
        <p style="color: #555; margin: 0;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def warning_box(title, description, icon="⚠️"):
    """Create warning box"""
    html = f"""
    <div style="
        background-color: {COLORS['warning']}15;
        border-left: 4px solid {COLORS['warning']};
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h4 style="color: {COLORS['warning']}; margin-top: 0;">
            {icon} {title}
        </h4>
        <p style="color: #555; margin: 0;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def success_box(title, description, icon="✅"):
    """Create success box"""
    html = f"""
    <div style="
        background-color: {COLORS['success']}15;
        border-left: 4px solid {COLORS['success']};
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h4 style="color: {COLORS['success']}; margin-top: 0;">
            {icon} {title}
        </h4>
        <p style="color: #555; margin: 0;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def divider(margin="2rem"):
    """Create styled divider"""
    st.markdown(f"<hr style='margin: {margin} 0; border: none; border-top: 2px solid {COLORS['light_gray']};'>", 
               unsafe_allow_html=True)


def tab_divider():
    """Create light divider for tab separation"""
    st.markdown("---")


def waterfall_metrics(items):
    """
    Create waterfall visualization metrics
    
    Parameters:
    -----------
    items : list of dict
        List of items with 'label' and 'value' keys
    """
    html = '<div style="margin: 1.5rem 0;">'
    
    for i, item in enumerate(items):
        if i == 0:
            line_style = "solid"
            line_color = COLORS['dark_blue']
        else:
            line_style = "dashed"
            line_color = COLORS['light_blue']
        
        html += f"""
        <div style="
            padding: 10px;
            margin: 5px 0;
            border-left: 3px {line_style} {line_color};
            padding-left: 15px;
        ">
            <span style="font-weight: 600; color: {COLORS['dark_blue']};">
                {item.get('label', '')}
            </span>
            <span style="float: right; color: {COLORS['accent_gold']}; font-weight: 700;">
                {item.get('value', '')}
            </span>
        </div>
        """
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
