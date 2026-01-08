
# 🏔️ LBO Investment Model - Enhanced Version
## The Mountain Path - World of Finance

**Prof. V. Ravichandran**  
28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence

---

## 📋 Overview

A **production-grade, institutional-quality LBO modeling tool** designed for comprehensive leveraged buyout analysis. This enhanced version combines advanced financial modeling with professional Streamlit design, enabling rapid analysis of complex debt structures and return scenarios.

### Key Improvements Over Original Model

| Feature | Original | Enhanced |
|---------|----------|----------|
| **Debt Structure** | Single tranche | Multi-tranche (Senior, Mezzanine, Other) |
| **Financial Model** | Basic waterfall | Complete FCFE/FCFF with taxes, CapEx, NWC |
| **Design System** | Inline CSS | Mountain Path template (config, styles, components) |
| **Reusability** | Monolithic | Modular (components.py, models.py, config.py) |
| **Analysis** | Exit multiple sensitivity | Multi-variable sensitivity + scenario analysis |
| **Documentation** | Minimal | Comprehensive with docstrings |
| **Export** | CSV only | CSV + structured dataframes |
| **Covenants** | Not tracked | Debt schedule with metrics |
| **Validations** | None | Input validation with ranges |

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd lbo_enhanced

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

### 3. Basic Usage

1. **Input Section**: Provide company financials, transaction assumptions, and financing structure
2. **Transaction Summary**: Review entry/exit metrics and key returns
3. **Waterfall Analysis**: Examine detailed debt schedules and cash flow
4. **Financial Projections**: Analyze 5-year operating projections
5. **Sensitivity Analysis**: Stress test across multiple scenarios

---

## 📁 Project Structure

```
lbo_enhanced/
├── app.py                  # Main Streamlit application (540 lines)
├── models.py               # Financial modeling engine (450 lines)
├── components.py           # Reusable Streamlit components (280 lines)
├── styles.py              # CSS styling & Mountain Path design (250 lines)
├── config.py              # Configuration constants (120 lines)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── QUICK_START.md        # 5-minute setup guide
```

### File Descriptions

**app.py** (Main Application)
- Page configuration and layout
- 5 interactive tabs with data input and analysis
- Sidebar with advanced settings
- Chart generation and export functionality
- ~540 lines of Streamlit code

**models.py** (Financial Engine)
- `Transaction` class: Entry/exit parameters
- `Financing` class: Multi-tranche debt structure
- `Operations` class: Operating assumptions
- `LBOModel` class: Core financial modeling engine
  - `project_operations()`: 5-year operating projections
  - `calculate_debt_schedule()`: Detailed debt amortization
  - `calculate_cash_flows()`: Complete waterfall
  - `calculate_exit()`: Return metrics (IRR, MOIC)
  - `sensitivity_analysis()`: Scenario testing
  - `get_summary_metrics()`: Key metrics extraction

**components.py** (UI Components)
- `hero_header()`: Professional header with branding
- `sidebar_header()`: Branded sidebar
- `metric_card()` & `metric_row()`: Metric displays
- `input_section()`: Styled input headers
- `data_table()`: Formatted tables
- `info_box()`, `warning_box()`, `success_box()`: Alert boxes
- `footer()`: Branded footer
- Additional utility components

**styles.py** (Design System)
- `apply_mountain_path_styles()`: Global CSS application
- Mountain Path color scheme (dark blue, light blue, gold)
- Responsive design for mobile
- Dark theme for readability
- Professional styling for all Streamlit elements

**config.py** (Configuration)
- Color scheme: Dark blue (#003366), Light blue (#004d80), Gold (#FFD700)
- Default values for all inputs
- Validation ranges for data entry
- Sensitivity analysis ranges
- LBO model constants

---

## 📊 Financial Modeling Details

### Model Architecture

The enhanced LBO model follows standard institutional frameworks:

```
Entry Valuation
    ↓
Transaction Structure (Sources & Uses)
    ↓
Financing (Senior, Mezz, Equity)
    ↓
Operating Projections (5 years)
    ↓
Debt Schedule (Interest + Repayment)
    ↓
Cash Flow Waterfall (FCFE/FCFF)
    ↓
Exit Analysis & Returns (MOIC, IRR, TVPI)
```

### Key Calculations

#### 1. **Entry Valuation**
```
Entry EV = LTM EBITDA × Entry Multiple
Total Cost = Entry EV + Transaction Fees (5% default)
```

#### 2. **Financing Structure**
```
Total Debt = Total Cost × Debt %
  ├── Senior Debt = Total Debt × 70% @ 4.0%
  ├── Mezzanine Debt = Total Debt × 20% @ 8.0%
  └── Other Debt = Total Debt × 10% @ 7.0%

Equity = Total Cost × (1 - Debt %)
```

#### 3. **Operating Projections** (Per Year)
```
Revenue = Previous Revenue × (1 + Growth Rate)
EBITDA = Revenue × EBITDA Margin
EBIT = EBITDA - Depreciation
EBT = EBIT - Interest Expense
Taxes = max(0, EBT × Tax Rate)
Net Income = EBT - Taxes
```

#### 4. **Debt Schedule** (Per Year)
```
Interest Expense = Beginning Debt Balance × Interest Rate
Principal Repaid = Total Debt × Mandatory Repay %
Ending Debt Balance = Beginning Balance - Principal Repaid
```

#### 5. **Free Cash Flow**
```
FCFF (Free Cash Flow to Firm) = EBITDA - CapEx - NWC Increase
FCFE (Free Cash Flow to Equity) = Net Income + Depreciation - CapEx - NWC Increase - Debt Repayment

where:
  CapEx = Revenue × CapEx %
  NWC Increase = Revenue Growth × NWC % of Revenue
```

#### 6. **Exit & Returns**
```
Exit EV = Year 5 EBITDA × Exit Multiple
Exit Proceeds = Exit EV - Exit Fees (2% default)
Remaining Debt = Year 5 Debt Balance
Equity Proceeds = Exit Proceeds - Remaining Debt

MOIC = Equity Proceeds / Equity Invested
IRR = (MOIC ^ (1 / Holding Period)) - 1
TVPI = (Equity Proceeds + Cumulative FCFE) / Equity Invested
```

### Debt Repayment Logic

The model implements **proportional debt repayment**:
- Total mandatory repayment = Total Debt × Repay Rate
- Each tranche repays proportionally to its share
- Senior debt reduces first, then mezz
- Ensures realistic waterfall priority

### Tax Treatment

- Taxes applied to **Earnings Before Interest (EBT)**
- Follows standard corporate tax structure
- Tax rate slider: 0-40% (default 30%)
- Conservative approach: taxes only on positive EBT

---

## 🎨 Design System: Mountain Path

### Color Palette

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Dark Blue | #003366 | 0, 51, 102 | Primary, headers, text |
| Light Blue | #004d80 | 0, 77, 128 | Secondary, accents |
| Gold | #FFD700 | 255, 215, 0 | Highlights, emphasis |
| Light Gray | #f8f9fa | - | Backgrounds |
| White | #FFFFFF | - | Cards, text |

### Components

```
Header
├── Title (28px, white)
├── Subtitle (20px, white)
└── Branding (14px, gold)

Navigation
├── Sidebar (gradient blue)
├── Tab System (dark blue border)
└── Advanced Settings (expandable)

Content
├── Input Sections (light gray, gold header)
├── Metric Cards (light blue border, dark blue text)
├── Tables (dark blue headers)
├── Charts (responsive, interactive)
└── Boxes (info, warning, success)

Footer
├── Branding (gold text)
├── Links (dark blue, hover gold)
└── Copyright (gray text)
```

### Styling Features

- **Responsive Design**: Adapts to mobile devices
- **Interactive Charts**: Hover tooltips, zoom capability
- **Professional Typography**: Consistent sizing hierarchy
- **Visual Hierarchy**: Color coding for different information types
- **Accessibility**: High contrast ratios, clear labels

---

## 📈 Features & Capabilities

### 1. **Flexible Input Section**
- Real-time validation of inputs
- Sliders for quick adjustments
- Dropdown tooltips with explanations
- Default values based on market standards

### 2. **Multi-Tab Analysis**
- **Inputs & Assumptions**: Configure transaction parameters
- **Transaction Summary**: Entry/exit waterfall and metrics
- **Waterfall Analysis**: Detailed debt schedule and FCF
- **Financial Projections**: 5-year operating metrics
- **Sensitivity & Scenarios**: Multi-scenario analysis

### 3. **Advanced Debt Modeling**
- Multi-tranche structure (Senior, Mezzanine, Other)
- Individual interest rates per tranche
- Proportional debt repayment
- Debt covenant monitoring
- Leverage ratio tracking

### 4. **Comprehensive Analysis**
- MOIC (Money Multiple on Invested Capital)
- IRR (Internal Rate of Return)
- TVPI (Total Value to Paid-In Capital)
- Debt/EV ratios
- Leverage tracking

### 5. **Scenario Analysis**
- Base, Bull, and Bear cases
- Exit multiple sensitivity (-1.5x to +1.5x)
- Revenue growth variations
- Interest rate stress testing
- Custom scenario builder

### 6. **Export Capabilities**
- Download cash flow projections (CSV)
- Export debt schedule (CSV)
- Save sensitivity analysis
- Share with stakeholders

---

## 🔧 Customization Guide

### Modify Default Values

Edit `config.py`:

```python
LBO_DEFAULTS = {
    'ltm_revenue': 5000000,      # Change from 3M to 5M
    'revenue_growth': 0.15,      # Change from 10% to 15%
    'capex_pct_revenue': 0.20,   # Change from 15% to 20%
    # ... modify other defaults
}
```

### Change Colors

Edit `config.py`:

```python
COLORS = {
    'dark_blue': '#1a3a52',      # Customize primary color
    'accent_gold': '#FFB700',    # Customize accent
    # ... update other colors
}
```

Then update `styles.py` CSS to match.

### Add New Metrics

Add to `models.py` in `LBOModel.get_summary_metrics()`:

```python
def get_summary_metrics(self) -> Dict:
    # ... existing code ...
    return {
        # ... existing metrics ...
        'new_metric': calculated_value,
    }
```

Then display in `app.py`:

```python
st.metric("New Metric", f"{summary['new_metric']:.2f}")
```

### Modify Projections

Edit `models.py` in `project_operations()`:

```python
def project_operations(self, years: int = 5) -> pd.DataFrame:
    # Add new projections
    # Example: add dividend calculations
    results.append({
        'Year': year,
        'Dividend': ebitda * 0.15,  # Add dividend calculation
        # ... existing fields ...
    })
```

---

## 📚 Financial Concepts Reference

### MOIC (Money Multiple)
- **Definition**: Total value returned divided by capital invested
- **Formula**: Equity Proceeds / Equity Invested
- **Interpretation**: 2.5x MOIC = $2.50 returned for every $1 invested
- **Target Range**: 2.0x - 4.0x (depends on holding period)

### IRR (Internal Rate of Return)
- **Definition**: Annual return on investment
- **Formula**: (MOIC ^ (1/Years)) - 1
- **Interpretation**: 25% IRR = 25% annualized return
- **Target Range**: 20% - 30%+ (target varies by fund)

### TVPI (Total Value to Paid-In)
- **Definition**: Includes exit proceeds and interim distributions
- **Formula**: (Exit Proceeds + Cumulative Interim Cash Flows) / Capital Invested
- **Use**: More complete return picture when interim cash flows exist

### Leverage Ratio
- **Definition**: Total Debt / EBITDA
- **Formula**: Total Debt / EBITDA
- **Interpretation**: 5.0x = $5 of debt per $1 of EBITDA
- **Typical Range**: 3.0x - 6.5x at entry

### Debt/EV
- **Definition**: Debt as percentage of enterprise value
- **Formula**: Total Debt / EV × 100
- **Interpretation**: 65% = 65% of purchase price financed by debt
- **Typical Range**: 50% - 75%

---

## 🔍 Validation & Error Handling

The model includes validation for:

```python
VALIDATION = {
    'min_revenue': 100000,           # Minimum $100K
    'max_revenue': 10000000000,      # Maximum $10B
    'min_margin': 0.01,              # 1% minimum
    'max_margin': 0.99,              # 99% maximum
    'min_multiple': 2.0,             # 2.0x minimum
    'max_multiple': 20.0,            # 20.0x maximum
    'min_rate': 0.0,                 # 0% minimum
    'max_rate': 0.30,                # 30% maximum
}
```

Input sliders and fields enforce these ranges automatically.

---

## 📊 Example Use Cases

### Case 1: PE Fund Due Diligence
- Analyze acquisition targets
- Model different debt structures
- Compare acquisition multiples
- Stress test exit scenarios

### Case 2: Corporate Strategy
- Evaluate bolt-on acquisition returns
- Model recapitalization scenarios
- Analyze dividend capacity
- Benchmark against industry

### Case 3: MBA/CFA Education
- Interactive learning tool
- Real-world modeling practice
- Scenario discussion tool
- Assignment/project platform

### Case 4: Investment Committee Presentations
- Quick waterfall generation
- Scenario comparison
- Professional visualizations
- Export for presentations

---

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.28+
- **Data**: Pandas 2.0+, NumPy 1.24+
- **Visualization**: Plotly 5.14+
- **Spreadsheet**: Openpyxl 3.10+
- **Python**: 3.8+

---

## 📋 Development Roadmap

### Phase 1 (Current) ✅
- [x] Multi-tranche debt structure
- [x] Complete cash flow waterfall
- [x] Professional design system
- [x] Basic sensitivity analysis

### Phase 2 (Planned)
- [ ] Excel export with formatting
- [ ] Multiple exit scenarios
- [ ] Distribution schedules
- [ ] Covenant tracking dashboard
- [ ] Monte Carlo simulation

### Phase 3 (Future)
- [ ] Multi-company portfolio
- [ ] League table comparisons
- [ ] Machine learning return prediction
- [ ] Real-time market data integration
- [ ] Collaboration features

---

## 📞 Support & Questions

### Documentation
- **Quick Start**: See QUICK_START.md
- **Customization**: See section above
- **Financial Concepts**: Refer to Reference section

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'streamlit'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Charts not rendering
- **Solution**: Ensure Plotly is installed: `pip install plotly>=5.14`

**Issue**: Negative MOIC or IRR
- **Solution**: Check that equity is fully returned; may indicate bad deal

---

## 📄 License & Attribution

Developed by **Prof. V. Ravichandran**  
The Mountain Path - World of Finance  
28+ Years Corporate Finance & Banking Experience  
10+ Years Academic Excellence

This tool is designed for educational and professional use.

---

## 🏔️ The Mountain Path Philosophy

> "Success in finance requires three elements: deep understanding of fundamentals, rigorous analytical discipline, and clear communication of complex ideas."

This model embodies these principles:
1. **Fundamentals**: Based on institutional LBO frameworks
2. **Discipline**: Validated inputs, consistent calculations
3. **Communication**: Professional design, clear visualizations

---

**Version**: 2.0 (Enhanced)  
**Last Updated**: January 2026  
**Status**: Production Ready
