
# ============================================================================
# LBO MODEL - COMPLETE APPLICATION (SINGLE FILE)
# The Mountain Path - World of Finance
# Prof. V. Ravichandran
# 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================================
# SECTION 1: CONFIGURATION
# ============================================================================

COLORS = {
    'dark_blue': '#003366',
    'light_blue': '#004d80',
    'accent_gold': '#FFD700',
    'white': '#FFFFFF',
    'light_gray': '#f8f9fa',
    'dark_gray': '#2c3e50',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
}

FONTS = {
    'family': 'sans-serif',
    'sizes': {
        'title': 28,
        'subtitle': 20,
        'heading': 18,
        'subheading': 14,
        'body': 12,
    }
}

BRANDING = {
    'name': 'The Mountain Path - World of Finance',
    'instructor': 'Prof. V. Ravichandran',
    'experience': '28+ Years Corporate Finance & Banking Experience',
    'academic': '10+ Years Academic Excellence',
    'icon': '🏔️',
}

PAGE_CONFIG = {
    'layout': 'wide',
    'page_title': 'LBO Investment Model | The Mountain Path',
    'page_icon': '🏔️',
}

LBO_DEFAULTS = {
    'ltm_revenue': 3000000,
    'ltm_ebitda': 1500000,
    'revenue_growth': 0.10,
    'ebitda_margin': 0.50,
    'tax_rate': 0.30,
    'entry_multiple': 7.5,
    'entry_fee_pct': 0.05,
    'debt_financing_pct': 0.65,
    'exit_multiple': 8.0,
    'holding_period': 5,
    'senior_debt_pct': 0.50,
    'senior_rate': 0.04,
    'mezz_debt_pct': 0.15,
    'mezz_rate': 0.08,
    'mandatory_repay_pct': 0.10,
    'capex_pct_revenue': 0.15,
    'depreciation': 300000,
    'nwc_pct_revenue': 0.10,
    'nwc_change_pct': 0.05,
    'projection_years': 5,
    'sensitivity_ranges': {
        'exit_multiple': [-1.0, -0.5, 0, 0.5, 1.0],
        'entry_multiple': [-1.0, -0.5, 0, 0.5, 1.0],
        'revenue_growth': [-0.05, -0.025, 0, 0.025, 0.05],
        'interest_rate': [-0.02, -0.01, 0, 0.01, 0.02],
    }
}

WATERFALL_COLORS = {
    'increase': COLORS['success'],
    'decrease': COLORS['danger'],
    'total': COLORS['dark_blue'],
}

VALIDATION = {
    'min_revenue': 100000,
    'max_revenue': 10000000000,
    'min_margin': 0.01,
    'max_margin': 0.99,
    'min_multiple': 2.0,
    'max_multiple': 20.0,
    'min_rate': 0.0,
    'max_rate': 0.30,
    'min_growth': -0.30,
    'max_growth': 0.50,
}

# ============================================================================
# SECTION 2: STYLING FUNCTIONS
# ============================================================================

def apply_mountain_path_styles():
    """Apply Mountain Path design system to Streamlit app"""
    css = f"""
    <style>
    :root {{
        --primary-color: {COLORS['dark_blue']};
        --secondary-color: {COLORS['light_blue']};
        --accent-color: {COLORS['accent_gold']};
    }}
    
    * {{
        font-family: {FONTS['family']};
    }}
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark_blue']} 0%, {COLORS['light_blue']} 100%);
        color: white !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] label {{
        color: white !important;
        font-weight: 600;
    }}
    
    [data-testid="stSidebar"] h3 {{
        color: {COLORS['accent_gold']} !important;
        font-weight: bold;
        letter-spacing: 1px;
    }}
    
    [data-testid="stSidebar"] .stSlider {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] span {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] div {{
        color: white !important;
    }}
    
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
    }}
    
    .header-subtitle {{
        font-weight: bold;
        color: {COLORS['accent_gold']};
        margin-top: 12px;
        font-size: {FONTS['sizes']['subheading']}px;
        letter-spacing: 1px;
    }}
    
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
    
    .input-header {{
        background: {COLORS['accent_gold']};
        color: {COLORS['dark_blue']};
        padding: 10px 15px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
    }}
    
    th {{
        background: {COLORS['dark_blue']};
        color: white;
        padding: 12px;
        font-weight: 600;
    }}
    
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
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# SECTION 3: UI COMPONENTS
# ============================================================================

def hero_header(title, subtitle="", show_branding=True):
    """Create professional hero header"""
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

def metric_card(label, value, delta=None, icon=""):
    """Create styled metric card"""
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
    """Create row of metric cards"""
    cols = st.columns(len(metrics_data))
    for col, metric in zip(cols, metrics_data):
        with col:
            metric_card(
                label=metric.get('label', ''),
                value=metric.get('value', ''),
                delta=metric.get('delta'),
                icon=metric.get('icon', '')
            )

def input_section(title, icon=""):
    """Create styled input section header"""
    html = f"""
    <div class="input-header">
        {icon} {title}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def data_table(df, title="", format_currency=None):
    """Create styled data table"""
    if title:
        st.markdown(f"<h3 style='color: {COLORS['dark_blue']};'>{title}</h3>", unsafe_allow_html=True)
    
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
        <div class="footer-credit">
            © 2026 <b>{BRANDING['instructor']}</b>. All rights reserved.<br>
            Empowering the next generation of Finance Professionals.
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def divider(margin="2rem"):
    """Create styled divider"""
    st.markdown(f"<hr style='margin: {margin} 0; border: none; border-top: 2px solid {COLORS['light_gray']};'>", unsafe_allow_html=True)

def info_box(title, description, icon="ℹ️"):
    """Create information box"""
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

# ============================================================================
# SECTION 4: FINANCIAL MODELS
# ============================================================================

@dataclass
class Transaction:
    """Transaction inputs"""
    entry_ebitda_multiple: float
    exit_ebitda_multiple: float
    entry_fee_pct: float
    holding_period: int
    
    def calculate_total_cost(self, ltm_ebitda):
        """Calculate total acquisition cost"""
        ev = ltm_ebitda * self.entry_ebitda_multiple
        fees = ev * self.entry_fee_pct
        return ev + fees

@dataclass
class Financing:
    """Financing structure"""
    total_cost: float
    debt_pct: float
    senior_debt_pct: float
    senior_rate: float
    mezz_debt_pct: float
    mezz_rate: float
    equity_pct: float
    
    def calculate_tranche_amounts(self):
        """Calculate individual tranche amounts"""
        total_debt = self.total_cost * self.debt_pct
        equity = self.total_cost * self.equity_pct
        
        senior_debt = total_debt * self.senior_debt_pct
        mezz_debt = total_debt * self.mezz_debt_pct
        other_debt = total_debt - senior_debt - mezz_debt
        
        return {
            'senior': senior_debt,
            'mezz': mezz_debt,
            'other': other_debt,
            'equity': equity,
            'total_debt': total_debt,
        }

@dataclass
class Operations:
    """Operating assumptions"""
    revenue_growth: float
    ebitda_margin: float
    tax_rate: float
    capex_pct_revenue: float
    depreciation: float
    nwc_pct_revenue: float
    nwc_change_pct: float
    mandatory_repay_pct: float

class LBOModel:
    """Comprehensive LBO financial model"""
    
    def __init__(self, ltm_revenue: float, ltm_ebitda: float,
                 transaction: Transaction, financing: Financing,
                 operations: Operations):
        """Initialize LBO Model"""
        self.ltm_revenue = ltm_revenue
        self.ltm_ebitda = ltm_ebitda
        self.transaction = transaction
        self.financing = financing
        self.operations = operations
        
        self.ltm_ebitda_margin = ltm_ebitda / ltm_revenue
        self.entry_ev = ltm_ebitda * transaction.entry_ebitda_multiple
        self.entry_fees = self.entry_ev * transaction.entry_fee_pct
        self.total_cost = self.entry_ev + self.entry_fees
        
        self.tranches = financing.calculate_tranche_amounts()
        self.initial_debt = self.tranches['total_debt']
        self.equity_invested = self.tranches['equity']
        
        self.projection_df = None
        self.debt_schedule_df = None
    
    def project_operations(self, years: int = 5) -> pd.DataFrame:
        """Project operating performance"""
        results = []
        current_revenue = self.ltm_revenue
        
        for year in range(1, years + 1):
            current_revenue *= (1 + self.operations.revenue_growth)
            ebitda = current_revenue * self.operations.ebitda_margin
            depreciation = self.operations.depreciation
            ebit = ebitda - depreciation
            capex = current_revenue * self.operations.capex_pct_revenue
            nwc_increase = current_revenue * self.operations.nwc_change_pct
            
            results.append({
                'Year': year,
                'Revenue': current_revenue,
                'EBITDA': ebitda,
                'Depreciation': depreciation,
                'EBIT': ebit,
                'CapEx': capex,
                'NWC_Increase': nwc_increase,
            })
        
        self.projection_df = pd.DataFrame(results)
        return self.projection_df
    
    def calculate_debt_schedule(self) -> pd.DataFrame:
        """Calculate detailed debt amortization schedule"""
        if self.projection_df is None:
            self.project_operations()
        
        schedule = []
        senior_balance = self.tranches['senior']
        mezz_balance = self.tranches['mezz']
        other_balance = self.tranches['other']
        
        for idx, row in self.projection_df.iterrows():
            year = row['Year']
            
            senior_interest = senior_balance * self.financing.senior_rate
            mezz_interest = mezz_balance * self.financing.mezz_rate
            other_interest = other_balance * 0.07
            total_interest = senior_interest + mezz_interest + other_interest
            
            total_debt = senior_balance + mezz_balance + other_balance
            
            if total_debt > 0:
                mandatory_repay = total_debt * self.operations.mandatory_repay_pct
                senior_repay = mandatory_repay * (senior_balance / total_debt) if senior_balance > 0 else 0
                mezz_repay = mandatory_repay * (mezz_balance / total_debt) if mezz_balance > 0 else 0
                other_repay = mandatory_repay * (other_balance / total_debt) if other_balance > 0 else 0
            else:
                senior_repay = mezz_repay = other_repay = 0
            
            senior_balance = max(0, senior_balance - senior_repay)
            mezz_balance = max(0, mezz_balance - mezz_repay)
            other_balance = max(0, other_balance - other_repay)
            
            total_ending_debt = senior_balance + mezz_balance + other_balance
            
            schedule.append({
                'Year': year,
                'Senior_Beginning': senior_balance + senior_repay,
                'Senior_Interest': senior_interest,
                'Senior_Repay': senior_repay,
                'Senior_Ending': senior_balance,
                'Mezz_Beginning': mezz_balance + mezz_repay,
                'Mezz_Interest': mezz_interest,
                'Mezz_Repay': mezz_repay,
                'Mezz_Ending': mezz_balance,
                'Total_Interest': total_interest,
                'Total_Repay': senior_repay + mezz_repay + other_repay,
                'Total_Debt_Ending': total_ending_debt,
            })
        
        self.debt_schedule_df = pd.DataFrame(schedule)
        return self.debt_schedule_df
    
    def calculate_cash_flows(self) -> pd.DataFrame:
        """Calculate unlevered and levered free cash flows"""
        if self.projection_df is None:
            self.project_operations()
        if self.debt_schedule_df is None:
            self.calculate_debt_schedule()
        
        df = self.projection_df.copy()
        df['Total_Interest'] = self.debt_schedule_df['Total_Interest'].values
        
        df['EBT'] = df['EBIT'] - df['Total_Interest']
        df['Taxes'] = df['EBT'].apply(lambda x: max(0, x * self.operations.tax_rate))
        df['Net_Income'] = df['EBT'] - df['Taxes']
        
        df['FCFF'] = df['EBITDA'] - df['CapEx'] - df['NWC_Increase']
        df['Debt_Repayment'] = self.debt_schedule_df['Total_Repay'].values
        df['FCFE'] = df['Net_Income'] + df['Depreciation'] - df['CapEx'] - df['NWC_Increase'] - df['Debt_Repayment']
        df['Remaining_Debt'] = self.debt_schedule_df['Total_Debt_Ending'].values
        
        return df
    
    def calculate_exit(self, exit_multiple: float = None) -> Dict:
        """Calculate exit proceeds and returns"""
        if exit_multiple is None:
            exit_multiple = self.transaction.exit_ebitda_multiple
        
        cf_df = self.calculate_cash_flows()
        final_ebitda = cf_df.iloc[-1]['EBITDA']
        remaining_debt = cf_df.iloc[-1]['Remaining_Debt']
        
        exit_ev = final_ebitda * exit_multiple
        transaction_fees = exit_ev * 0.02
        exit_proceeds = exit_ev - transaction_fees
        
        equity_proceeds = max(0, exit_proceeds - remaining_debt)
        
        if self.equity_invested > 0:
            moic = equity_proceeds / self.equity_invested
            irr = (moic ** (1 / self.transaction.holding_period)) - 1
            tvpi = (equity_proceeds + sum(cf_df['FCFE'])) / self.equity_invested
        else:
            moic = irr = tvpi = 0
        
        return {
            'exit_multiple': exit_multiple,
            'exit_ev': exit_ev,
            'transaction_fees': transaction_fees,
            'exit_proceeds': exit_proceeds,
            'remaining_debt': remaining_debt,
            'equity_proceeds': equity_proceeds,
            'moic': moic,
            'irr': irr,
            'tvpi': tvpi,
            'final_ebitda': final_ebitda,
            'initial_equity': self.equity_invested,
        }
    
    def sensitivity_analysis(self, variable: str, ranges: List[float]) -> pd.DataFrame:
        """Perform sensitivity analysis"""
        results = []
        
        for value in ranges:
            if variable == 'exit_multiple':
                exit_val = value
            else:
                exit_val = self.transaction.exit_ebitda_multiple
            
            exit_data = self.calculate_exit(exit_multiple=exit_val)
            
            results.append({
                f'{variable}': value,
                'MOIC': exit_data['moic'],
                'IRR': exit_data['irr'] * 100,
                'Equity_Proceeds': exit_data['equity_proceeds'],
            })
        
        return pd.DataFrame(results)
    
    def get_summary_metrics(self) -> Dict:
        """Get key summary metrics"""
        cf_df = self.calculate_cash_flows()
        exit_data = self.calculate_exit()
        debt_sched = self.debt_schedule_df
        
        return {
            'ltm_revenue': self.ltm_revenue,
            'ltm_ebitda': self.ltm_ebitda,
            'ltm_margin': self.ltm_ebitda_margin * 100,
            'entry_ev': self.entry_ev,
            'total_cost': self.total_cost,
            'initial_debt': self.initial_debt,
            'initial_debt_ratio': (self.initial_debt / self.entry_ev) * 100,
            'equity_invested': self.equity_invested,
            'year_5_revenue': cf_df.iloc[-1]['Revenue'],
            'year_5_ebitda': cf_df.iloc[-1]['EBITDA'],
            'year_5_debt': cf_df.iloc[-1]['Remaining_Debt'],
            'total_interest_paid': debt_sched['Total_Interest'].sum(),
            'total_debt_repaid': debt_sched['Total_Repay'].sum(),
            'exit_value': exit_data['exit_ev'],
            'equity_proceeds': exit_data['equity_proceeds'],
            'moic': exit_data['moic'],
            'irr': exit_data['irr'] * 100,
        }

# ============================================================================
# SECTION 5: MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    st.set_page_config(**PAGE_CONFIG)
    apply_mountain_path_styles()
    
    sidebar_header()
    
    holding_period = st.sidebar.slider("Holding Period (Years)", 3, 10, LBO_DEFAULTS['holding_period'])
    projection_years = st.sidebar.slider("Projection Years", 3, 10, LBO_DEFAULTS['projection_years'])
    
    hero_header(
        "LBO Investment Model",
        "Comprehensive Leveraged Buyout & Debt Waterfall Analysis",
        show_branding=True
    )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Inputs & Assumptions",
        "📊 Transaction Summary",
        "💰 Waterfall Analysis",
        "📈 Financial Projections",
        "🎯 Sensitivity & Scenarios"
    ])
    
    # TAB 1: INPUTS
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            input_section("🏢 Company Financials")
            ltm_revenue = st.slider(
                "LTM Revenue ($)",
                VALIDATION['min_revenue'],
                VALIDATION['max_revenue'],
                LBO_DEFAULTS['ltm_revenue'],
                step=100000
            )
            ltm_ebitda = st.slider(
                "LTM EBITDA ($)",
                int(ltm_revenue * 0.01),
                int(ltm_revenue * 0.8),
                LBO_DEFAULTS['ltm_ebitda'],
                step=50000
            )
            st.metric("EBITDA Margin", f"{(ltm_ebitda/ltm_revenue)*100:.1f}%")
        
        with col2:
            input_section("🤝 Transaction Assumptions")
            entry_multiple = st.slider(
                "Entry Multiple (x EBITDA)",
                VALIDATION['min_multiple'],
                VALIDATION['max_multiple'],
                LBO_DEFAULTS['entry_multiple'],
                step=0.5
            )
            exit_multiple = st.slider(
                "Exit Multiple (x EBITDA)",
                VALIDATION['min_multiple'],
                VALIDATION['max_multiple'],
                LBO_DEFAULTS['exit_multiple'],
                step=0.5
            )
            entry_fee_pct = st.slider(
                "Entry Fees (%)",
                0.0,
                10.0,
                LBO_DEFAULTS['entry_fee_pct'] * 100,
                step=0.5
            ) / 100
        
        with col3:
            input_section("💳 Financing Structure")
            debt_pct = st.slider(
                "Total Debt %",
                VALIDATION['min_rate'],
                0.9,
                LBO_DEFAULTS['debt_financing_pct'],
                step=0.05
            )
            senior_rate = st.slider(
                "Senior Rate (%)",
                VALIDATION['min_rate'],
                VALIDATION['max_rate'],
                LBO_DEFAULTS['senior_rate'],
                step=0.5
            ) / 100
            mezz_rate = st.slider(
                "Mezz Rate (%)",
                senior_rate,
                VALIDATION['max_rate'],
                LBO_DEFAULTS['mezz_rate'],
                step=0.5
            ) / 100
        
        divider()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            input_section("📊 Operations", "")
            revenue_growth = st.slider(
                "Revenue Growth (%)",
                VALIDATION['min_growth'],
                VALIDATION['max_growth'],
                LBO_DEFAULTS['revenue_growth'],
                step=0.01
            )
        
        with col2:
            ebitda_margin = st.slider(
                "EBITDA Margin (%)",
                VALIDATION['min_margin'],
                VALIDATION['max_margin'],
                LBO_DEFAULTS['ebitda_margin'],
                step=0.01
            )
        
        with col3:
            tax_rate = st.slider(
                "Tax Rate (%)",
                VALIDATION['min_rate'],
                0.4,
                LBO_DEFAULTS['tax_rate'],
                step=0.01
            )
        
        with col4:
            capex_pct = st.slider(
                "CapEx (% Rev)",
                VALIDATION['min_rate'],
                0.3,
                LBO_DEFAULTS['capex_pct_revenue'],
                step=0.01
            )
        
        with col5:
            mandatory_repay = st.slider(
                "Mandatory Repay (%)",
                VALIDATION['min_rate'],
                0.3,
                LBO_DEFAULTS['mandatory_repay_pct'],
                step=0.01
            )
        
        # Create objects
        transaction = Transaction(entry_multiple, exit_multiple, entry_fee_pct, holding_period)
        total_cost = transaction.calculate_total_cost(ltm_ebitda)
        
        financing = Financing(
            total_cost, debt_pct, 0.50, senior_rate,
            0.15, mezz_rate, 1 - debt_pct
        )
        
        operations = Operations(
            revenue_growth, ebitda_margin, tax_rate,
            capex_pct, LBO_DEFAULTS['depreciation'],
            LBO_DEFAULTS['nwc_pct_revenue'],
            LBO_DEFAULTS['nwc_change_pct'],
            mandatory_repay
        )
        
        model = LBOModel(ltm_revenue, ltm_ebitda, transaction, financing, operations)
        model.project_operations(projection_years)
        model.calculate_debt_schedule()
    
    # TAB 2: SUMMARY
    with tab2:
        summary = model.get_summary_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Entry EV", f"${summary['entry_ev']:,.0f}")
        with col2:
            st.metric("Total Cost", f"${summary['total_cost']:,.0f}")
        with col3:
            st.metric("Debt", f"${summary['initial_debt']:,.0f}")
        with col4:
            st.metric("Equity", f"${summary['equity_invested']:,.0f}")
        
        divider()
        
        exit_data = model.calculate_exit()
        metrics = [
            {'label': 'MOIC', 'value': f"{summary['moic']:.2f}x", 'icon': '📊'},
            {'label': 'IRR', 'value': f"{summary['irr']:.1f}%", 'icon': '🎯'},
            {'label': 'Debt/EV', 'value': f"{summary['initial_debt_ratio']:.1f}%", 'icon': '💳'},
            {'label': 'Exit Value', 'value': f"${exit_data['exit_ev']:,.0f}", 'icon': '💰'},
        ]
        metric_row(metrics)
    
    # TAB 3: WATERFALL
    with tab3:
        debt_sched = model.debt_schedule_df.copy()
        debt_sched['Senior'] = debt_sched['Senior_Ending']
        debt_sched['Mezz'] = debt_sched['Mezz_Ending']
        debt_sched['Total'] = debt_sched['Total_Debt_Ending']
        
        display_cols = ['Year', 'Senior', 'Mezz', 'Total', 'Total_Interest', 'Total_Repay']
        debt_display = debt_sched[display_cols].copy()
        
        for col in ['Senior', 'Mezz', 'Total', 'Total_Interest', 'Total_Repay']:
            debt_display[col] = debt_display[col].apply(lambda x: f"${x:,.0f}")
        
        data_table(debt_display, "Debt Amortization Schedule")
    
    # TAB 4: PROJECTIONS
    with tab4:
        cf_df = model.calculate_cash_flows()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=cf_df['Year'],
            y=cf_df['Revenue'],
            name='Revenue',
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=cf_df['Year'],
            y=cf_df['EBITDA'],
            name='EBITDA',
            mode='lines+markers'
        ))
        fig.update_layout(
            title='Revenue & EBITDA Growth',
            xaxis_title='Year',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        proj_display = cf_df[['Year', 'Revenue', 'EBITDA', 'Net_Income']].copy()
        for col in ['Revenue', 'EBITDA', 'Net_Income']:
            proj_display[col] = proj_display[col].apply(lambda x: f"${x:,.0f}")
        
        data_table(proj_display, "Operating Metrics")
    
    # TAB 5: SENSITIVITY
    with tab5:
        st.subheader("Exit Multiple Sensitivity")
        
        exit_ranges = [
            model.transaction.exit_ebitda_multiple + x
            for x in LBO_DEFAULTS['sensitivity_ranges']['exit_multiple']
        ]
        
        sensitivity_df = model.sensitivity_analysis('exit_multiple', exit_ranges)
        sensitivity_df['exit_multiple'] = sensitivity_df['exit_multiple'].apply(lambda x: f"{x:.1f}x")
        sensitivity_df['MOIC'] = sensitivity_df['MOIC'].apply(lambda x: f"{x:.2f}x")
        sensitivity_df['Equity_Proceeds'] = sensitivity_df['Equity_Proceeds'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(sensitivity_df, use_container_width=True)
    
    divider()
    footer()

if __name__ == "__main__":
    main()
