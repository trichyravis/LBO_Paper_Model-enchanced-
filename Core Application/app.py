# ============================================================================
# LBO MODEL - MAIN STREAMLIT APPLICATION
# The Mountain Path - World of Finance
# Prof. V. Ravichandran
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# Import custom modules
from config import PAGE_CONFIG, COLORS, LBO_DEFAULTS
from styles import apply_mountain_path_styles
from components import (
    hero_header, sidebar_header, metric_row, input_section,
    data_table, footer, info_box, warning_box, divider, tab_divider
)
from models import Transaction, Financing, Operations, LBOModel

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
)

# Apply Mountain Path styling
apply_mountain_path_styles()

# ============================================================================
# SIDEBAR
# ============================================================================

sidebar_header()

with st.sidebar:
    st.write("---")
    st.markdown("### ⚙️ Model Settings")
    
    holding_period = st.slider(
        "Holding Period (Years)",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        help="Expected holding period for the investment"
    )
    
    projection_years = st.slider(
        "Projection Years",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        help="Number of years to project"
    )
    
    with st.expander("📊 Advanced Settings"):
        st.write("**Debt Structure**")
        senior_pct_of_debt = st.slider(
            "Senior Debt % of Total Debt",
            min_value=40,
            max_value=100,
            value=70,
            step=5,
            help="Percentage of debt that is senior"
        ) / 100
        
        st.write("**Exit Assumptions**")
        show_scenario_analysis = st.checkbox("Show Multiple Scenarios", value=True)

# ============================================================================
# MAIN HEADER
# ============================================================================

hero_header(
    title="LBO Investment Model",
    subtitle="Comprehensive Leveraged Buyout & Debt Waterfall Analysis",
    show_branding=True
)

# ============================================================================
# MAIN TABS
# ============================================================================

tab_inputs, tab_summary, tab_waterfall, tab_projections, tab_sensitivity = st.tabs([
    "📋 INPUTS & ASSUMPTIONS",
    "📊 TRANSACTION SUMMARY",
    "💰 WATERFALL ANALYSIS",
    "📈 FINANCIAL PROJECTIONS",
    "🎯 SENSITIVITY & SCENARIOS"
])

# ============================================================================
# TAB 1: INPUTS & ASSUMPTIONS
# ============================================================================

with tab_inputs:
    st.markdown("#### Provide your LBO transaction details below")
    
    col1, col2, col3 = st.columns(3)
    
    # ===== COMPANY FINANCIALS =====
    with col1:
        input_section("🏢 Company Financials", "")
        
        ltm_revenue = st.number_input(
            "LTM Revenue ($)",
            min_value=100000,
            max_value=10000000000,
            value=int(LBO_DEFAULTS['ltm_revenue']),
            step=100000,
            format="%d",
            help="Last Twelve Months Revenue"
        )
        
        ltm_ebitda = st.number_input(
            "LTM EBITDA ($)",
            min_value=10000,
            max_value=1000000000,
            value=int(LBO_DEFAULTS['ltm_ebitda']),
            step=50000,
            format="%d",
            help="Last Twelve Months EBITDA"
        )
        
        # Display calculated margin
        if ltm_revenue > 0:
            margin_pct = (ltm_ebitda / ltm_revenue) * 100
            st.metric("LTM EBITDA Margin", f"{margin_pct:.1f}%")
    
    # ===== TRANSACTION ASSUMPTIONS =====
    with col2:
        input_section("⚙️ Transaction Assumptions", "")
        
        entry_multiple = st.slider(
            "Entry EV/EBITDA Multiple",
            min_value=2.0,
            max_value=20.0,
            value=LBO_DEFAULTS['entry_multiple'],
            step=0.5,
            help="Entry valuation multiple"
        )
        
        entry_fee_pct = st.slider(
            "Transaction Fees (% of EV)",
            min_value=2,
            max_value=10,
            value=5,
            step=1,
            help="Advisory and transaction fees"
        ) / 100
        
        exit_multiple = st.slider(
            "Exit EV/EBITDA Multiple",
            min_value=2.0,
            max_value=20.0,
            value=LBO_DEFAULTS['exit_multiple'],
            step=0.5,
            help="Expected exit valuation multiple"
        )
    
    # ===== FINANCING STRUCTURE =====
    with col3:
        input_section("💳 Financing Structure", "")
        
        debt_pct = st.slider(
            "Total Debt (% of Total Cost)",
            min_value=10,
            max_value=90,
            value=65,
            step=5,
            help="Leverage ratio"
        ) / 100
        
        senior_rate = st.slider(
            "Senior Debt Rate (%)",
            min_value=1.0,
            max_value=12.0,
            value=4.0,
            step=0.25,
            help="Interest rate on senior debt"
        ) / 100
        
        mezz_rate = st.slider(
            "Mezzanine Rate (%)",
            min_value=6.0,
            max_value=15.0,
            value=8.0,
            step=0.25,
            help="Interest rate on mezz debt"
        ) / 100
    
    divider()
    
    col4, col5, col6 = st.columns(3)
    
    # ===== OPERATIONS ASSUMPTIONS =====
    with col4:
        input_section("📊 Operations Assumptions", "")
        
        revenue_growth = st.slider(
            "Annual Revenue Growth (%)",
            min_value=-20,
            max_value=50,
            value=10,
            step=1,
        ) / 100
        
        ebitda_margin = st.slider(
            "EBITDA Margin (%)",
            min_value=5,
            max_value=80,
            value=50,
            step=1,
        ) / 100
    
    with col5:
        input_section("💰 Cash Flow Assumptions", "")
        
        capex_pct = st.slider(
            "CapEx (% of Revenue)",
            min_value=0,
            max_value=30,
            value=15,
            step=1,
        ) / 100
        
        nwc_change_pct = st.slider(
            "NWC Change (% of Revenue Growth)",
            min_value=0,
            max_value=20,
            value=5,
            step=1,
        ) / 100
    
    with col6:
        input_section("📋 Other Assumptions", "")
        
        tax_rate = st.slider(
            "Tax Rate (%)",
            min_value=0,
            max_value=40,
            value=30,
            step=1,
        ) / 100
        
        mandatory_repay_pct = st.slider(
            "Mandatory Annual Debt Repay (%)",
            min_value=0,
            max_value=20,
            value=10,
            step=1,
        ) / 100
    
    info_box(
        "Methodology Notes",
        "This model assumes proportional debt repayment across tranches. "
        "Interest is calculated on beginning debt balances. "
        "Tax is applied to earnings before interest (EBT).",
        "ℹ️"
    )


# ============================================================================
# BUILD THE LBO MODEL
# ============================================================================

# Create transaction structure
transaction = Transaction(
    entry_ebitda_multiple=entry_multiple,
    exit_ebitda_multiple=exit_multiple,
    entry_fee_pct=entry_fee_pct,
    holding_period=holding_period,
)

# Create financing structure
equity_pct = 1 - debt_pct
financing = Financing(
    total_cost=0,  # Will be calculated
    debt_pct=debt_pct,
    senior_debt_pct=senior_pct_of_debt,
    senior_rate=senior_rate,
    mezz_debt_pct=(1 - senior_pct_of_debt) * 0.5,  # Mezz is 50% of non-senior
    mezz_rate=mezz_rate,
    equity_pct=equity_pct,
)

# Create operations structure
operations = Operations(
    revenue_growth=revenue_growth,
    ebitda_margin=ebitda_margin,
    tax_rate=tax_rate,
    capex_pct_revenue=capex_pct,
    depreciation=300000,  # Fixed depreciation assumption
    nwc_pct_revenue=0.10,
    nwc_change_pct=nwc_change_pct,
    mandatory_repay_pct=mandatory_repay_pct,
)

# Initialize and run model
lbo = LBOModel(ltm_revenue, ltm_ebitda, transaction, financing, operations)

# ============================================================================
# TAB 2: TRANSACTION SUMMARY
# ============================================================================

with tab_summary:
    st.markdown("#### Transaction Overview & Key Metrics")
    
    # Get summary data
    summary = lbo.get_summary_metrics()
    waterfall = lbo.get_waterfall_data()
    
    # Transaction waterfall
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Transaction Waterfall**")
        
        waterfall_items = [
            {'label': 'LTM EBITDA', 'value': f"${waterfall['LTM_EBITDA']:,.0f}"},
            {'label': f"× Entry Multiple ({waterfall['Entry_Multiple']:.1f}x)", 'value': f"${waterfall['Entry_EV']:,.0f}"},
            {'label': '+ Transaction Fees', 'value': f"${waterfall['Fees']:,.0f}"},
            {'label': '= Total Cost', 'value': f"${waterfall['Total_Cost']:,.0f}"},
        ]
        
        for item in waterfall_items:
            st.write(f"<div style='padding: 8px; margin: 5px 0; border-left: 3px solid {COLORS['dark_blue']}; padding-left: 12px;'>"
                    f"<span style='font-weight: 600;'>{item['label']}</span>"
                    f"<span style='float: right; color: {COLORS['accent_gold']}; font-weight: 700;'>{item['value']}</span>"
                    f"</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Sources & Uses**")
        
        uses_items = [
            {'label': 'Enterprise Value', 'value': f"${waterfall['Entry_EV']:,.0f}"},
            {'label': 'Transaction Fees', 'value': f"${waterfall['Fees']:,.0f}"},
            {'label': '= Total Uses', 'value': f"${waterfall['Total_Cost']:,.0f}"},
            {'label': '', 'value': ''},
            {'label': 'Debt Financing', 'value': f"${waterfall['Debt']:,.0f}"},
            {'label': 'Equity Financing', 'value': f"${waterfall['Equity']:,.0f}"},
            {'label': '= Total Sources', 'value': f"${waterfall['Total_Cost']:,.0f}"},
        ]
        
        for item in uses_items:
            if item['label']:
                st.write(f"<div style='padding: 8px; margin: 5px 0; border-left: 3px solid {COLORS['light_blue']}; padding-left: 12px;'>"
                        f"<span style='font-weight: 600;'>{item['label']}</span>"
                        f"<span style='float: right; color: {COLORS['accent_gold']}; font-weight: 700;'>{item['value']}</span>"
                        f"</div>", unsafe_allow_html=True)
            else:
                st.write("---")
    
    divider()
    
    # Key Metrics
    st.markdown("**Key Entry Metrics**")
    
    metrics = [
        {'label': 'Entry EV', 'value': f"${summary['entry_ev']:,.0f}", 'icon': '💰'},
        {'label': 'Total Debt', 'value': f"${summary['initial_debt']:,.0f}", 'icon': '💳'},
        {'label': 'Equity Invested', 'value': f"${summary['equity_invested']:,.0f}", 'icon': '📊'},
        {'label': 'Leverage (Debt/EV)', 'value': f"{waterfall['Debt_Pct']:.1f}%", 'icon': '⚙️'},
    ]
    
    metric_row(metrics)
    
    divider()
    
    # Exit metrics
    st.markdown("**Projected Exit Metrics (Year 5)**")
    
    exit_metrics = [
        {'label': 'Year 5 EBITDA', 'value': f"${summary['year_5_ebitda']:,.0f}", 'icon': '📈'},
        {'label': 'Remaining Debt', 'value': f"${summary['year_5_debt']:,.0f}", 'icon': '💳'},
        {'label': 'Exit Value (@{:.1f}x)'.format(transaction.exit_ebitda_multiple), 
         'value': f"${summary['exit_value']:,.0f}", 'icon': '🎯'},
        {'label': 'Equity Proceeds', 'value': f"${summary['equity_proceeds']:,.0f}", 'icon': '💎'},
    ]
    
    metric_row(exit_metrics)
    
    divider()
    
    # Return Metrics
    st.markdown("**Return Metrics**")
    
    return_metrics = [
        {'label': 'MOIC (Money Multiple)', 'value': f"{summary['moic']:.2f}x", 
         'delta': f"+{(summary['moic']-1)*100:.1f}%", 'icon': '📊'},
        {'label': 'IRR', 'value': f"{summary['irr']:.1f}%", 'icon': '🎯'},
    ]
    
    metric_row(return_metrics)


# ============================================================================
# TAB 3: WATERFALL ANALYSIS
# ============================================================================

with tab_waterfall:
    st.markdown("#### Detailed Debt Schedule & Cash Flow Waterfall")
    
    # Calculate cash flows and debt schedule
    cf_df = lbo.calculate_cash_flows()
    debt_sched = lbo.debt_schedule_df
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("**Debt Amortization Schedule**")
        
        # Create summary debt table
        debt_summary = pd.DataFrame({
            'Year': debt_sched['Year'],
            'Senior Debt': debt_sched['Senior_Ending'],
            'Mezz Debt': debt_sched['Mezz_Ending'],
            'Total Debt': debt_sched['Total_Debt_Ending'],
            'Interest Expense': debt_sched['Total_Interest'],
            'Principal Repaid': debt_sched['Total_Repay'],
        })
        
        st.dataframe(
            debt_summary.style.format({
                'Senior Debt': '${:,.0f}',
                'Mezz Debt': '${:,.0f}',
                'Total Debt': '${:,.0f}',
                'Interest Expense': '${:,.0f}',
                'Principal Repaid': '${:,.0f}',
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("**Debt Metrics**")
        
        initial_debt = debt_sched.iloc[0]['Senior_Beginning'] + debt_sched.iloc[0]['Mezz_Beginning']
        final_debt = debt_sched.iloc[-1]['Total_Debt_Ending']
        total_interest = debt_sched['Total_Interest'].sum()
        total_repay = debt_sched['Total_Repay'].sum()
        
        debt_metrics = [
            {'label': 'Initial Debt', 'value': f"${initial_debt:,.0f}", 'icon': '💳'},
            {'label': 'Final Debt', 'value': f"${final_debt:,.0f}", 'icon': '📉'},
            {'label': 'Total Repaid', 'value': f"${total_repay:,.0f}", 'icon': '✅'},
            {'label': 'Total Interest', 'value': f"${total_interest:,.0f}", 'icon': '📊'},
        ]
        
        metric_row(debt_metrics)
    
    tab_divider()
    
    st.markdown("**Free Cash Flow Waterfall**")
    
    # Create FCF summary
    fcf_summary = pd.DataFrame({
        'Year': cf_df['Year'],
        'EBITDA': cf_df['EBITDA'],
        'Interest': cf_df['Total_Interest'],
        'Taxes': cf_df['Taxes'],
        'CapEx': cf_df['CapEx'],
        'Debt Repayment': cf_df['Debt_Repayment'],
        'FCFE': cf_df['FCFE'],
    })
    
    st.dataframe(
        fcf_summary.style.format({
            'EBITDA': '${:,.0f}',
            'Interest': '${:,.0f}',
            'Taxes': '${:,.0f}',
            'CapEx': '${:,.0f}',
            'Debt Repayment': '${:,.0f}',
            'FCFE': '${:,.0f}',
        }),
        use_container_width=True,
        hide_index=True
    )


# ============================================================================
# TAB 4: FINANCIAL PROJECTIONS
# ============================================================================

with tab_projections:
    st.markdown("#### 5-Year Financial Projections")
    
    # Revenue and EBITDA growth chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Revenue & EBITDA Growth**")
        
        fig_growth = go.Figure()
        
        fig_growth.add_trace(go.Scatter(
            x=cf_df['Year'],
            y=cf_df['Revenue'],
            name='Revenue',
            mode='lines+markers',
            line=dict(color=COLORS['dark_blue'], width=3),
            marker=dict(size=8),
            hovertemplate='Year %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_growth.add_trace(go.Scatter(
            x=cf_df['Year'],
            y=cf_df['EBITDA'],
            name='EBITDA',
            mode='lines+markers',
            line=dict(color=COLORS['accent_gold'], width=3),
            marker=dict(size=8),
            hovertemplate='Year %{x}<br>EBITDA: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_growth.update_layout(
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            height=400,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
        st.markdown("**Debt Reduction Profile**")
        
        fig_debt = go.Figure()
        
        fig_debt.add_trace(go.Bar(
            x=debt_sched['Year'],
            y=debt_sched['Total_Debt_Ending'],
            name='Remaining Debt',
            marker=dict(color=COLORS['danger']),
            hovertemplate='Year %{x}<br>Debt: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_debt.update_layout(
            hovermode='x',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            height=400,
            showlegend=False,
        )
        
        st.plotly_chart(fig_debt, use_container_width=True)
    
    divider()
    
    # Operating metrics table
    st.markdown("**Detailed Operating Metrics**")
    
    operating_metrics = pd.DataFrame({
        'Year': cf_df['Year'],
        'Revenue': cf_df['Revenue'],
        'Growth %': cf_df['Revenue'].pct_change() * 100,
        'EBITDA': cf_df['EBITDA'],
        'Margin %': (cf_df['EBITDA'] / cf_df['Revenue'] * 100),
        'EBIT': cf_df['EBIT'],
        'Net Income': cf_df['Net_Income'],
    })
    
    operating_metrics.loc[0, 'Growth %'] = np.nan
    
    st.dataframe(
        operating_metrics.style.format({
            'Revenue': '${:,.0f}',
            'Growth %': '{:.1f}%',
            'EBITDA': '${:,.0f}',
            'Margin %': '{:.1f}%',
            'EBIT': '${:,.0f}',
            'Net Income': '${:,.0f}',
        }),
        use_container_width=True,
        hide_index=True
    )


# ============================================================================
# TAB 5: SENSITIVITY & SCENARIOS
# ============================================================================

with tab_sensitivity:
    st.markdown("#### Return Sensitivity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Exit Multiple Sensitivity**")
        
        exit_multiples = np.array([
            exit_multiple - 1.5,
            exit_multiple - 1.0,
            exit_multiple - 0.5,
            exit_multiple,
            exit_multiple + 0.5,
            exit_multiple + 1.0,
            exit_multiple + 1.5,
        ])
        
        sens_results = []
        for mult in exit_multiples:
            exit_data = lbo.calculate_exit(exit_multiple=mult)
            sens_results.append({
                'Exit Multiple': f"{mult:.1f}x",
                'Exit Value': f"${exit_data['exit_ev']:,.0f}",
                'Equity Proceeds': f"${exit_data['equity_proceeds']:,.0f}",
                'MOIC': f"{exit_data['moic']:.2f}x",
                'IRR': f"{exit_data['irr']*100:.1f}%",
            })
        
        sens_df = pd.DataFrame(sens_results)
        st.dataframe(sens_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**IRR Sensitivity Chart**")
        
        # Create sensitivity heatmap data
        entry_mults = np.array([entry_multiple - 1.5, entry_multiple - 1.0, entry_multiple - 0.5,
                               entry_multiple, entry_multiple + 0.5, entry_multiple + 1.0, entry_multiple + 1.5])
        exit_mults = np.array([exit_multiple - 1.0, exit_multiple - 0.5, exit_multiple,
                              exit_multiple + 0.5, exit_multiple + 1.0])
        
        # Note: This would require recalculating with different entry multiples
        # For now, show exit multiple sensitivity
        irr_values = []
        for mult in exit_multiples:
            exit_data = lbo.calculate_exit(exit_multiple=mult)
            irr_values.append(exit_data['irr'] * 100)
        
        fig_sens = go.Figure()
        
        fig_sens.add_trace(go.Scatter(
            x=exit_multiples,
            y=irr_values,
            mode='lines+markers',
            name='IRR',
            line=dict(color=COLORS['dark_blue'], width=3),
            marker=dict(size=10, color=irr_values, colorscale='RdYlGn', showscale=True),
            hovertemplate='Exit Multiple: %{x:.1f}x<br>IRR: %{y:.1f}%<extra></extra>'
        ))
        
        fig_sens.update_layout(
            hovermode='x',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            height=400,
            xaxis_title='Exit EBITDA Multiple',
            yaxis_title='IRR (%)',
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
    
    divider()
    
    if show_scenario_analysis:
        st.markdown("**Scenario Analysis**")
        
        scenarios = {
            'Base Case': {
                'entry': entry_multiple,
                'exit': exit_multiple,
                'growth': revenue_growth,
                'margin': ebitda_margin,
            },
            'Bull Case': {
                'entry': entry_multiple - 0.5,
                'exit': exit_multiple + 1.0,
                'growth': revenue_growth + 0.05,
                'margin': ebitda_margin + 0.05,
            },
            'Bear Case': {
                'entry': entry_multiple + 0.5,
                'exit': exit_multiple - 1.0,
                'growth': revenue_growth - 0.05,
                'margin': ebitda_margin - 0.05,
            },
        }
        
        scenario_results = []
        for scenario_name, assumptions in scenarios.items():
            # For this simple version, only change exit multiple
            exit_data = lbo.calculate_exit(exit_multiple=assumptions['exit'])
            
            scenario_results.append({
                'Scenario': scenario_name,
                'Entry Multiple': f"{assumptions['entry']:.1f}x",
                'Exit Multiple': f"{assumptions['exit']:.1f}x",
                'Equity Proceeds': f"${exit_data['equity_proceeds']:,.0f}",
                'MOIC': f"{exit_data['moic']:.2f}x",
                'IRR': f"{exit_data['irr']*100:.1f}%",
            })
        
        scenarios_df = pd.DataFrame(scenario_results)
        st.dataframe(scenarios_df, use_container_width=True, hide_index=True)
    
    divider()
    
    # Export functionality
    st.markdown("**Export Data**")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        csv_data = cf_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Cash Flows (CSV)",
            data=csv_data,
            file_name="lbo_cashflows.csv",
            mime="text/csv",
        )
    
    with col_export2:
        csv_debt = debt_sched.to_csv(index=False)
        st.download_button(
            label="📥 Download Debt Schedule (CSV)",
            data=csv_debt,
            file_name="lbo_debt_schedule.csv",
            mime="text/csv",
        )
    
    with col_export3:
        csv_sens = sens_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sensitivity (CSV)",
            data=csv_sens,
            file_name="lbo_sensitivity.csv",
            mime="text/csv",
        )

# ============================================================================
# FOOTER
# ============================================================================

divider(margin="3rem")
footer()
