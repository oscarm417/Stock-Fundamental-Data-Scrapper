
import pandas as pd
import requests
import numpy as np
import requests
from dateutil import parser
from datetime import datetime 
from abc import ABC

class Financials(ABC):
    """ Returns a stocks fundamental data:
    Example:
    stocks_fundamental_data = Financials().get_financials('GOOGL')
    """
    def __init__(self):
        self.ticker = None
    def download(self,ticker):
        """Returns a dictionary with 8 data frames containing different financial metrics.
         Each data frame can be called with the following keys:
            'Income Statements'
            'Income % Statements'
            'Return Ratios'
            'Revenue Growth'
            'Cashflow Growth'
            'Balance Sheet'
            'Financial Health Ratios'

        Args:
            ticker (String): Receives the Stocks Ticker as String

        Returns:
            Dictionary[DataFrames]:
            'Income Statements': ['Revenue USD Mil', 'Gross Margin %', 'Operating Income USD Mil',
                                'Operating Margin %', 'Net Income USD Mil', 'Earnings Per Share USD',
                                'Dividends USD', 'Payout Ratio % *', 'Shares Mil',
                                'Book Value Per Share * USD', 'Operating Cash Flow USD Mil',
                                'Cap Spending USD Mil', 'Free Cash Flow USD Mil',
                                'Free Cash Flow Per Share * USD', 'Working Capital USD Mil']

            'Margins % of Sales': ['Revenue', 'COGS', 'Gross Margin', 'SG&A', 'R&D', 'Other',
                                    'Operating Margin', 'Net Int Inc & Other', 'EBT Margin']

            'Profitability': ['Tax Rate %', 'Net Margin %', 'Asset Turnover (Average)',
                            'Return on Assets %', 'Financial Leverage (Average)',
                            'Return on Equity %', 'Return on Invested Capital %',
                            'Interest Coverage']

            'Revenue Growth': ['Revenue %', 'Year over Year', '3-Year Average', '5-Year Average',
                                '10-Year Average', 'Operating Income %', 'Net Income %', 'EPS %']

            'Cash Flow Ratios': ['Operating Cash Flow Growth % YOY', 'Free Cash Flow Growth % YOY',
                                'Cap Ex as a % of Sales', 'Free Cash Flow/Sales %',
                                'Free Cash Flow/Net Income']
            'Balance Sheet Items in %': ['Cash & Short-Term Investments', 'Accounts Receivable', 'Inventory',
                                        'Other Current Assets', 'Total Current Assets', 'Net PP&E',
                                        'Intangibles', 'Other Long-Term Assets', 'Total Assets',
                                        'Accounts Payable', 'Short-Term Debt', 'Taxes Payable',
                                        'Accrued Liabilities', 'Other Short-Term Liabilities',
                                        'Total Current Liabilities', 'Long-Term Debt',
                                        'Other Long-Term Liabilities', 'Total Liabilities',
                                        'Total Stockholders' Equity', 'Total Liabilities & Equity']

            'Financial Health Ratios': ['Current Ratio', 'Quick Ratio', 'Financial Leverage', 'Debt/Equity']
            
            'Efficiency': ['Days Sales Outstanding', 'Days Inventory', 'Payables Period',
                        'Cash Conversion Cycle', 'Receivables Turnover', 'Inventory Turnover',
                        'Fixed Assets Turnover', 'Asset Turnover']
                        """
        
        self.ticker = ticker
        all_data = self._get_data()
        all_data_labels = [i.columns[0] for i in all_data]
        all_data = [all_data[i].dropna(axis=0).set_index(all_data_labels[i]).T.replace("-",np.nan) for i in range(len(all_data))]
        all_data_labels[0] = "Income Statement"
        all_data_labels[3] = "Income Statement %"
        all_data = self._clean_tables(all_data)
        data = {all_data_labels[i].replace("(","").replace(")",""): all_data[i] for i in range(len(all_data_labels))}
        return data

    def _get_data(self):
        urlFinancials = "https://financials.morningstar.com/finan/financials/getFinancePart.html?&callback=?&t={}&region=usa&culture=en-US&cur=&order=asc".format(self.ticker)
        urlRatios = "http://financials.morningstar.com/finan/financials/getKeyStatPart.html?&callback=?&t={}&region=usa&culture=en-US&cur=&order=asc".format(self.ticker)
        data_Financials = requests.get(urlFinancials).content.decode("utf8").replace("'",'""')
        data_Ratios  =  requests.get(urlRatios).content.decode("utf8").replace("'",'""')
        financials= pd.read_html(data_Financials.replace("\\",'')[2:-1])
        ratios  = pd.read_html(data_Ratios.replace("\\",'')[2:-1])
        all_data = [financials[0]]+ratios
        return all_data
    
    def _clean_tables(self,all_data):
        temp_data = []
        #clean Columns
        count = 0
        for table in all_data:
            table.columns = [table.columns[i].replace("\xa0", u" ").replace(" *","") for i in range(0,len(table.columns))]
            table = table.replace(to_replace = '—', value = np.nan)
            table.index = [parser.parse(i) if "-" in i else datetime.now().date() for i in table.index]

            table.index = pd.to_datetime(table.index)

            table = table.astype('float',errors = 'ignore')
            temp_data.append(table)
            count+=1
        return temp_data





