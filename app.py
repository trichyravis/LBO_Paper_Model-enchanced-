
# ============================================================================
# LBO INVESTMENT MODEL - PRODUCTION VERSION (CONSTRAINT LOGIC)
# The Mountain Path - World of Finance
# Prof. V. Ravichandran
# 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence
# ============================================================================
# CONSTRAINT: If Mandatory_Repay >= FCF, then Repay = FCF (liquidity cap)
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="LBO Investment Model | The Mountain Path", page_icon="🏔️")

COLORS = {'dark_blue': '#003366', 'light_blue': '#004d80', 'accent_gold': '#FFD700'}
BRANDING = {'name': 'The Mountain Path - World of Finance', 'instructor': 'Prof. V. Ravichandran', 'icon': '🏔️'}

st.markdown(f"""
<style>
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {COLORS['dark_blue']} 0%, {COLORS['light_blue']} 100%); color: white !important; }}
[data-testid="stSidebar"] * {{ color: white !important; }}
[data-testid="stSidebar"] label {{ color: white !important; font-weight: 600; }}
[data-testid="stSidebar"] h3 {{ color: {COLORS['accent_gold']} !important; }}
.header {{ background: linear-gradient(135deg, {COLORS['dark_blue']} 0%, {COLORS['light_blue']} 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="header">
    <h1 style="margin: 0;">LBO Investment Model</h1>
    <div style="color: {COLORS['accent_gold']}; margin-top: 10px;">
        {BRANDING['icon']} {BRANDING['name']}<br>
        <span style="font-size: 12px;">{BRANDING['instructor']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

DEFAULTS = {
    'purchase_price': 100000000,
    'fees_pct': 0.02,
    'debt_amount': 60000000,
    'entry_revenue': 100000000,
    'revenue_growth': 0.05,
    'ebitda_margin': 0.25,
    'exit_multiple': 10.0,
    'tax_rate': 0.25,
    'capex': 5000000,
    'depreciation': 3000000,
    'nwc_pct': -0.01,
    'debt_rate': 0.07,
    'mandatory_repay_pct': 0.10,
    'hold_years': 4,
}

# ============================================================================
# MODEL WITH CONSTRAINT LOGIC
# ============================================================================

class LBOModel:
    def __init__(self, purchase_price, fees_pct, debt_amount, entry_revenue,
                 revenue_growth, ebitda_margin, exit_multiple, tax_rate,
                 capex, depreciation, nwc_pct, debt_rate, mandatory_repay_pct, hold_years):
        self.purchase_price = purchase_price
        self.fees = purchase_price * fees_pct
        self.total_cost = purchase_price + self.fees
        self.debt = debt_amount
        self.equity = self.total_cost - debt_amount
        self.entry_revenue = entry_revenue
        self.entry_ebitda = entry_revenue * ebitda_margin
        self.revenue_growth = revenue_growth
        self.ebitda_margin = ebitda_margin
        self.exit_multiple = exit_multiple
        self.tax_rate = tax_rate
        self.capex = capex
        self.depreciation = depreciation
        self.nwc_pct = nwc_pct
        self.debt_rate = debt_rate
        self.mandatory_repay_pct = mandatory_repay_pct
        self.hold_years = hold_years
        self.df = None
        
    def project(self):
        """
        CONSTRAINT LOGIC: 
        IF(Mandatory_Repay >= FCF, use FCF, use Mandatory_Repay)
        Ending_Debt = Beginning_Debt - Actual_Repayment
        """
        results = []
        current_debt = self.debt
        accumulated_balance_fcf = 0
        current_revenue = self.entry_revenue
        
        for year in range(1, self.hold_years + 1):
            # Revenue & EBITDA growth
            current_revenue = current_revenue * (1 + self.revenue_growth)
            ebitda = current_revenue * self.ebitda_margin
            ebit = ebitda - self.depreciation
            
            # Interest calculation
            interest = current_debt * self.debt_rate
            ebt = ebit - interest
            tax = ebt * self.tax_rate
            net_income = ebt - tax
            
            # Free Cash Flow calculation
            nwc_change = current_revenue * self.nwc_pct
            fcf = net_income + self.depreciation - self.capex - nwc_change
            
            # CONSTRAINT: Mandatory Repayment
            # IF(Mandatory_Repay >= FCF, use FCF, use Mandatory_Repay)
            calculated_repay = current_debt * self.mandatory_repay_pct
            actual_repay = min(calculated_repay, fcf) if calculated_repay >= fcf else calculated_repay
            
            # Actually, the constraint logic is:
            # If calculated >= FCF, cap at FCF
            # Otherwise use calculated
            if calculated_repay >= fcf:
                actual_repay = fcf  # Limited by available cash
            else:
                actual_repay = calculated_repay  # Full repayment possible
            
            balance_fcf = fcf - actual_repay
            accumulated_balance_fcf += balance_fcf
            
            # Ending Debt = Beginning Debt - Actual Repayment (from FCFF)
            ending_debt = current_debt - actual_repay
            
            results.append({
                'Year': 2024 + year,
                'Revenue': current_revenue,
                'EBITDA': ebitda,
                'Depreciation': self.depreciation,
                'EBIT': ebit,
                'Interest': interest,
                'EBT': ebt,
                'Tax': tax,
                'Net_Income': net_income,
                'NWC_Change': nwc_change,
                'FCF': fcf,
                'Calc_Repay': calculated_repay,
                'Actual_Repay': actual_repay,
                'Balance_FCF': balance_fcf,
                'Beginning_Debt': current_debt,
                'Ending_Debt': ending_debt,
                'Accumulated_FCF': accumulated_balance_fcf,
            })
            
            current_debt = ending_debt
        
        self.df = pd.DataFrame(results)
        return self.df
    
    def get_returns(self):
        if self.df is None:
            self.project()
        
        final = self.df.iloc[-1]
        exit_ev = final['EBITDA'] * self.exit_multiple
        accumulated_fcf = final['Accumulated_FCF']
        remaining_debt = final['Ending_Debt']
        equity_proceeds = exit_ev + accumulated_fcf - remaining_debt
        moic = equity_proceeds / self.equity if self.equity > 0 else 0
        irr = (moic ** (1/self.hold_years)) - 1 if moic > 0 else 0
        
        return {
            'exit_ev': exit_ev,
            'accumulated_fcf': accumulated_fcf,
            'remaining_debt': remaining_debt,
            'equity_proceeds': equity_proceeds,
            'moic': moic,
            'irr': irr,
        }

# ============================================================================
# SIDEBAR INPUTS
# ============================================================================

st.sidebar.markdown(f"""
<div style="text-align: center; padding: 1.5rem; background: rgba(255,215,0,0.1); border-radius: 10px; margin-bottom: 1.5rem; border: 2px solid {COLORS['accent_gold']};">
    <h3 style="color: {COLORS['accent_gold']}; margin: 0;">{BRANDING['icon']} LBO MODEL</h3>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Inputs", "📊 Summary", "💰 Projections", "🎯 Returns", "📈 Analysis"])

# TAB 1: INPUTS
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div style='background: {COLORS['accent_gold']}; color: {COLORS['dark_blue']}; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 15px;'>💰 Transaction</div>", unsafe_allow_html=True)
        purchase_price = st.number_input("Purchase Price", value=DEFAULTS['purchase_price'], step=10000000)
        fees_pct = st.slider("Fees (%)", 0.0, 5.0, DEFAULTS['fees_pct']*100, 0.5) / 100
        exit_multiple = st.slider("Exit Multiple (x EBITDA)", 5.0, 15.0, DEFAULTS['exit_multiple'], 0.5)
    
    with col2:
        st.markdown(f"<div style='background: {COLORS['accent_gold']}; color: {COLORS['dark_blue']}; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 15px;'>💳 Financing</div>", unsafe_allow_html=True)
        debt_amount = st.number_input("Debt Amount", value=DEFAULTS['debt_amount'], step=5000000)
        debt_rate = st.slider("Interest Rate (%)", 2.0, 12.0, DEFAULTS['debt_rate']*100, 0.5) / 100
        mandatory_repay = st.slider("Mandatory Repay (%)", 2.0, 20.0, DEFAULTS['mandatory_repay_pct']*100, 1.0) / 100
    
    with col3:
        st.markdown(f"<div style='background: {COLORS['accent_gold']}; color: {COLORS['dark_blue']}; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 15px;'>📈 Operations</div>", unsafe_allow_html=True)
        entry_revenue = st.number_input("Entry Revenue", value=DEFAULTS['entry_revenue'], step=10000000)
        revenue_growth = st.slider("Revenue Growth (%)", 0.0, 15.0, DEFAULTS['revenue_growth']*100, 0.5) / 100
        ebitda_margin = st.slider("EBITDA Margin (%)", 5.0, 50.0, DEFAULTS['ebitda_margin']*100, 1.0) / 100
    
    st.divider()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        capex = st.number_input("Annual CapEx", value=int(DEFAULTS['capex']), step=500000)
    with col2:
        depreciation = st.number_input("Annual D&A", value=int(DEFAULTS['depreciation']), step=500000)
    with col3:
        nwc_pct = st.slider("NWC Change (%)", -5.0, 5.0, DEFAULTS['nwc_pct']*100, 0.5) / 100
    with col4:
        tax_rate = st.slider("Tax Rate (%)", 10.0, 40.0, DEFAULTS['tax_rate']*100, 1.0) / 100
    with col5:
        hold_years = st.slider("Hold Period (Years)", 3, 10, DEFAULTS['hold_years'])
    
    model = LBOModel(purchase_price, fees_pct, debt_amount, entry_revenue, revenue_growth,
                     ebitda_margin, exit_multiple, tax_rate, capex, depreciation, nwc_pct,
                     debt_rate, mandatory_repay, hold_years)
    model.project()

# TAB 2: SUMMARY
with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cost", f"${model.total_cost:,.0f}")
        st.metric("Debt", f"${model.debt:,.0f}")
    with col2:
        st.metric("Equity", f"${model.equity:,.0f}")
        st.metric("Leverage", f"{(model.debt/model.entry_ebitda):.2f}x")
    with col3:
        st.metric("Entry EBITDA", f"${model.entry_ebitda:,.0f}")
        st.metric("Entry EV/EBITDA", f"{(model.purchase_price/model.entry_ebitda):.2f}x")
    
    st.divider()
    
    returns = model.get_returns()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("MOIC", f"{returns['moic']:.2f}x", delta=f"{(returns['moic']-1)*100:.0f}%")
    with col2:
        target_irr = 40.0
        st.metric("IRR", f"{returns['irr']*100:.1f}%", delta=f"{returns['irr']*100 - target_irr:.1f}% vs 40%")
    with col3:
        st.metric("Exit EV", f"${returns['exit_ev']:,.0f}")
    with col4:
        st.metric("Equity Proceeds", f"${returns['equity_proceeds']:,.0f}")

# TAB 3: PROJECTIONS
with tab3:
    st.subheader("📊 Levered Free Cash Flow")
    fcf_df = model.df[['Year', 'Revenue', 'EBITDA', 'Net_Income', 'FCF', 'Actual_Repay', 'Balance_FCF']].copy()
    fcf_df['Year'] = fcf_df['Year'].astype(int)
    for col in ['Revenue', 'EBITDA', 'Net_Income', 'FCF', 'Actual_Repay', 'Balance_FCF']:
        fcf_df[col] = fcf_df[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(fcf_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("💳 Debt Schedule (Constraint Applied)")
    debt_df = model.df[['Year', 'Beginning_Debt', 'Interest', 'Actual_Repay', 'Ending_Debt']].copy()
    debt_df['Year'] = debt_df['Year'].astype(int)
    for col in ['Beginning_Debt', 'Interest', 'Actual_Repay', 'Ending_Debt']:
        debt_df[col] = debt_df[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(debt_df, use_container_width=True, hide_index=True)
    
    st.info("**Constraint Logic:** IF(Mandatory_Repay >= FCF, use FCF, use Mandatory_Repay)\n\nEnding Debt = Beginning Debt - Actual Repayment (from FCFF)")

# TAB 4: RETURNS
with tab4:
    st.subheader("🎯 Exit Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Exit Year EBITDA", f"${model.df.iloc[-1]['EBITDA']:,.0f}")
    with col2:
        st.metric("Exit Multiple", f"{model.exit_multiple:.1f}x")
    with col3:
        st.metric("Enterprise Value", f"${returns['exit_ev']:,.0f}")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accumulated FCF", f"${returns['accumulated_fcf']:,.0f}")
    with col2:
        st.metric("Remaining Debt", f"${returns['remaining_debt']:,.0f}")
    with col3:
        st.metric("Equity Proceeds", f"${returns['equity_proceeds']:,.0f}")

# TAB 5: ANALYSIS
with tab5:
    st.subheader("📊 Sensitivity Analysis - Exit Multiple")
    
    sensitivity = []
    for exit_m in np.arange(model.exit_multiple - 2, model.exit_multiple + 3, 1):
        if exit_m > 0:
            exit_val = model.df.iloc[-1]['EBITDA'] * exit_m
            eq_proc = exit_val + returns['accumulated_fcf'] - returns['remaining_debt']
            m = eq_proc / model.equity if model.equity > 0 else 0
            i = (m ** (1/model.hold_years)) - 1 if m > 0 else 0
            sensitivity.append({
                'Exit Multiple': f"{exit_m:.1f}x",
                'MOIC': f"{m:.2f}x",
                'IRR': f"{i*100:.1f}%",
                'Status': '✅' if i >= 0.40 else '❌'
            })
    
    st.dataframe(pd.DataFrame(sensitivity), use_container_width=True, hide_index=True)

st.divider()
st.markdown(f"""
<div style="text-align: center; padding: 20px;">
    <p style="color: {COLORS['dark_blue']}; font-weight: bold;">Connect with {BRANDING['instructor']}</p>
    <div style="display: flex; gap: 10px; justify-content: center;">
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="background: #0A66C2; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none;">🔗 LinkedIn</a>
        <a href="https://github.com/trichyravis/" target="_blank" style="background: #333; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none;">💻 GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)
