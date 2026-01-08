
# ============================================================================
# LBO MODEL - CONFIGURATION & DESIGN SYSTEM
# The Mountain Path - World of Finance
# Prof. V. Ravichandran
# ============================================================================

# MOUNTAIN PATH COLOR SCHEME
COLORS = {
    'dark_blue': '#003366',      # RGB(0, 51, 102) - Primary
    'light_blue': '#004d80',     # RGB(0, 77, 128) - Secondary
    'accent_gold': '#FFD700',    # RGB(255, 215, 0) - Accent
    'white': '#FFFFFF',
    'light_gray': '#f8f9fa',
    'dark_gray': '#2c3e50',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
}

# TYPOGRAPHY
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

# COMPANY BRANDING
BRANDING = {
    'name': 'The Mountain Path - World of Finance',
    'instructor': 'Prof. V. Ravichandran',
    'experience': '28+ Years Corporate Finance & Banking Experience',
    'academic': '10+ Years Academic Excellence',
    'icon': '🏔️',
}

# PAGE CONFIG
PAGE_CONFIG = {
    'layout': 'wide',
    'page_title': 'LBO Investment Model | The Mountain Path',
    'page_icon': '🏔️',
}

# LBO MODEL CONSTANTS & DEFAULTS
LBO_DEFAULTS = {
    # Company Financials
    'ltm_revenue': 3000000,
    'ltm_ebitda': 1500000,
    'revenue_growth': 0.10,
    'ebitda_margin': 0.50,
    'tax_rate': 0.30,
    
    # Transaction
    'entry_multiple': 7.5,
    'entry_fee_pct': 0.05,
    'debt_financing_pct': 0.65,
    'exit_multiple': 8.0,
    'holding_period': 5,
    
    # Debt
    'senior_debt_pct': 0.50,
    'senior_rate': 0.04,
    'mezz_debt_pct': 0.15,
    'mezz_rate': 0.08,
    'mandatory_repay_pct': 0.10,
    
    # Operations
    'capex_pct_revenue': 0.15,
    'depreciation': 300000,
    'nwc_pct_revenue': 0.10,
    'nwc_change_pct': 0.05,
    
    # Projections
    'projection_years': 5,
    'sensitivity_ranges': {
        'exit_multiple': [-1.0, -0.5, 0, 0.5, 1.0],
        'entry_multiple': [-1.0, -0.5, 0, 0.5, 1.0],
        'revenue_growth': [-0.05, -0.025, 0, 0.025, 0.05],
        'interest_rate': [-0.02, -0.01, 0, 0.01, 0.02],
    }
}

# WATERFALL COLORS
WATERFALL_COLORS = {
    'increase': COLORS['success'],
    'decrease': COLORS['danger'],
    'total': COLORS['dark_blue'],
}

# EXPORT SETTINGS
EXPORT = {
    'excel_format': '.xlsx',
    'csv_format': '.csv',
    'datetime_format': '%Y-%m-%d',
}

# VALIDATION RULES
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
