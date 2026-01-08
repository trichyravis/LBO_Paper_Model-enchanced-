# ============================================================================
# LBO MODEL - FINANCIAL MODELING ENGINE
# The Mountain Path - World of Finance
# Advanced Leveraged Buyout Analysis with Multi-Tranche Debt
# ============================================================================

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
from config import LBO_DEFAULTS

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
    """
    Comprehensive LBO financial model with:
    - Multi-tranche debt structure
    - Detailed cash flow waterfall
    - Debt covenants monitoring
    - Sensitivity analysis
    - Return metrics (IRR, MOIC, TVPI)
    """
    
    def __init__(self, ltm_revenue: float, ltm_ebitda: float,
                 transaction: Transaction, financing: Financing,
                 operations: Operations):
        """
        Initialize LBO Model
        
        Parameters:
        -----------
        ltm_revenue : float
            Last twelve months revenue
        ltm_ebitda : float
            Last twelve months EBITDA
        transaction : Transaction
            Transaction parameters
        financing : Financing
            Financing structure
        operations : Operations
            Operating assumptions
        """
        self.ltm_revenue = ltm_revenue
        self.ltm_ebitda = ltm_ebitda
        self.transaction = transaction
        self.financing = financing
        self.operations = operations
        
        # Calculate metrics
        self.ltm_ebitda_margin = ltm_ebitda / ltm_revenue
        
        # Transaction metrics
        self.entry_ev = ltm_ebitda * transaction.entry_ebitda_multiple
        self.entry_fees = self.entry_ev * transaction.entry_fee_pct
        self.total_cost = self.entry_ev + self.entry_fees
        
        # Financing metrics
        self.tranches = financing.calculate_tranche_amounts()
        self.initial_debt = self.tranches['total_debt']
        self.equity_invested = self.tranches['equity']
        
        # Initialize projections
        self.projection_df = None
        self.debt_schedule_df = None
        
    def project_operations(self, years: int = 5) -> pd.DataFrame:
        """
        Project operating performance
        
        Parameters:
        -----------
        years : int
            Number of projection years
            
        Returns:
        --------
        pd.DataFrame
            Operating projections
        """
        results = []
        current_revenue = self.ltm_revenue
        
        for year in range(1, years + 1):
            # Revenue projection
            current_revenue *= (1 + self.operations.revenue_growth)
            
            # EBITDA and margins
            ebitda = current_revenue * self.operations.ebitda_margin
            
            # Depreciation & Amortization
            depreciation = self.operations.depreciation
            
            # EBIT
            ebit = ebitda - depreciation
            
            # Tax
            # Note: Tax calculated on EBT (EBIT - Interest)
            # Will be calculated after debt schedule
            
            # CapEx
            capex = current_revenue * self.operations.capex_pct_revenue
            
            # NWC Change
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
        """
        Calculate detailed debt amortization schedule
        
        Returns:
        --------
        pd.DataFrame
            Debt schedule with interest and repayment
        """
        if self.projection_df is None:
            self.project_operations()
        
        schedule = []
        
        # Initialize debt balances
        senior_balance = self.tranches['senior']
        mezz_balance = self.tranches['mezz']
        other_balance = self.tranches['other']
        
        for idx, row in self.projection_df.iterrows():
            year = row['Year']
            
            # Interest expense
            senior_interest = senior_balance * self.financing.senior_rate
            mezz_interest = mezz_balance * self.financing.mezz_rate
            other_interest = other_balance * 0.07  # Assume 7% for other debt
            
            total_interest = senior_interest + mezz_interest + other_interest
            
            # Mandatory repayment (senior first, then mezz)
            # For simplicity: proportional repayment across tranches
            total_debt = senior_balance + mezz_balance + other_balance
            
            if total_debt > 0:
                # Mandatory repayment is on total debt
                mandatory_repay = total_debt * self.operations.mandatory_repay_pct
                
                # Proportional repayment
                senior_repay = mandatory_repay * (senior_balance / total_debt) if senior_balance > 0 else 0
                mezz_repay = mandatory_repay * (mezz_balance / total_debt) if mezz_balance > 0 else 0
                other_repay = mandatory_repay * (other_balance / total_debt) if other_balance > 0 else 0
            else:
                senior_repay = mezz_repay = other_repay = 0
            
            # Update balances
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
                'Other_Beginning': other_balance + other_repay,
                'Other_Interest': other_interest,
                'Other_Repay': other_repay,
                'Other_Ending': other_balance,
                'Total_Interest': total_interest,
                'Total_Repay': senior_repay + mezz_repay + other_repay,
                'Total_Debt_Ending': total_ending_debt,
            })
        
        self.debt_schedule_df = pd.DataFrame(schedule)
        return self.debt_schedule_df
    
    def calculate_cash_flows(self) -> pd.DataFrame:
        """
        Calculate unlevered and levered free cash flows
        
        Returns:
        --------
        pd.DataFrame
            Detailed cash flow waterfall
        """
        if self.projection_df is None:
            self.project_operations()
        if self.debt_schedule_df is None:
            self.calculate_debt_schedule()
        
        # Merge projections and debt schedule
        df = self.projection_df.copy()
        df['Total_Interest'] = self.debt_schedule_df['Total_Interest'].values
        
        # Calculate FCF
        df['EBT'] = df['EBIT'] - df['Total_Interest']
        df['Taxes'] = df['EBT'].apply(lambda x: max(0, x * self.operations.tax_rate))
        df['Net_Income'] = df['EBT'] - df['Taxes']
        
        # Unlevered FCF (Free Cash Flow to Firm)
        df['FCFF'] = df['EBITDA'] - df['CapEx'] - df['NWC_Increase']
        
        # Levered FCF (Free Cash Flow to Equity)
        df['Debt_Repayment'] = self.debt_schedule_df['Total_Repay'].values
        df['FCFE'] = df['Net_Income'] + df['Depreciation'] - df['CapEx'] - df['NWC_Increase'] - df['Debt_Repayment']
        
        # Remaining debt
        df['Remaining_Debt'] = self.debt_schedule_df['Total_Debt_Ending'].values
        
        return df
    
    def calculate_exit(self, exit_multiple: float = None) -> Dict:
        """
        Calculate exit proceeds and returns
        
        Parameters:
        -----------
        exit_multiple : float, optional
            Exit EV/EBITDA multiple (uses transaction value if not provided)
            
        Returns:
        --------
        dict
            Exit value, equity proceeds, and return metrics
        """
        if exit_multiple is None:
            exit_multiple = self.transaction.exit_ebitda_multiple
        
        cf_df = self.calculate_cash_flows()
        final_ebitda = cf_df.iloc[-1]['EBITDA']
        remaining_debt = cf_df.iloc[-1]['Remaining_Debt']
        
        # Exit calculations
        exit_ev = final_ebitda * exit_multiple
        transaction_fees = exit_ev * 0.02  # Assume 2% exit fees
        exit_proceeds = exit_ev - transaction_fees
        
        equity_proceeds = max(0, exit_proceeds - remaining_debt)
        
        # Return metrics
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
        """
        Perform sensitivity analysis on exit returns
        
        Parameters:
        -----------
        variable : str
            'exit_multiple', 'entry_multiple', 'revenue_growth', 'margin'
        ranges : list
            List of values to test
            
        Returns:
        --------
        pd.DataFrame
            Sensitivity results
        """
        results = []
        
        for value in ranges:
            # Create modified model
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
    
    def get_waterfall_data(self) -> Dict:
        """
        Get transaction waterfall data
        
        Returns:
        --------
        dict
            Waterfall components
        """
        return {
            'Entry_EV': self.entry_ev,
            'Fees': self.entry_fees,
            'Total_Cost': self.total_cost,
            'Debt': self.initial_debt,
            'Equity': self.equity_invested,
            'LTM_EBITDA': self.ltm_ebitda,
            'Entry_Multiple': self.transaction.entry_ebitda_multiple,
            'Debt_Pct': self.financing.debt_pct * 100,
        }
    
    def get_summary_metrics(self) -> Dict:
        """
        Get key summary metrics
        
        Returns:
        --------
        dict
            Summary metrics
        """
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
