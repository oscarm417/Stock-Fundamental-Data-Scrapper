# Stock-Fundamental-Data-Scrapper
GIven a stocks ticker this will return 8 data frames containing the following data:
'Income Statements', 'Income % Statements', 'Return Ratios', 'Revenue Growth', 'Cashflow Growth', 'Balance Sheet', 'Financial Health Ratios'

Each of the data frames contains the following headers:

Dictionary[DataFrames]:

            'Income Statements': ['Revenue USD Mil', 'Gross Margin %', 'Operating Income USD Mil',
                                'Operating Margin %', 'Net Income USD Mil', 'Earnings Per Share USD',
                                'Dividends USD', 'Payout Ratio % *', 'Shares Mil',
                                'Book Value Per Share * USD', 'Operating Cash Flow USD Mil',
                                'Cap Spending USD Mil', 'Free Cash Flow USD Mil',
                                'Free Cash Flow Per Share * USD', 'Working Capital USD Mil']

            'Income % Statements': ['Revenue', 'COGS', 'Gross Margin', 'SG&A', 'R&D', 'Other',
                                    'Operating Margin', 'Net Int Inc & Other', 'EBT Margin']

            'Return Ratios': ['Tax Rate %', 'Net Margin %', 'Asset Turnover (Average)',
                            'Return on Assets %', 'Financial Leverage (Average)',
                            'Return on Equity %', 'Return on Invested Capital %',
                            'Interest Coverage']

            'Revenue Growth': ['Revenue %', 'Year over Year', '3-Year Average', '5-Year Average',
                                '10-Year Average', 'Operating Income %', 'Net Income %', 'EPS %']

            'Cashflow Growth': ['Operating Cash Flow Growth % YOY', 'Free Cash Flow Growth % YOY',
                                'Cap Ex as a % of Sales', 'Free Cash Flow/Sales %',
                                'Free Cash Flow/Net Income']
            'Balance Sheet': ['Cash & Short-Term Investments', 'Accounts Receivable', 'Inventory',
                            'Other Current Assets', 'Total Current Assets', 'Net PP&E',
                            'Intangibles', 'Other Long-Term Assets', 'Total Assets',
                            'Accounts Payable', 'Short-Term Debt', 'Taxes Payable',
                            'Accrued Liabilities', 'Other Short-Term Liabilities',
                            'Total Current Liabilities', 'Long-Term Debt',
                            'Other Long-Term Liabilities', 'Total Liabilities',
                            'Total Stockholders' Equity', 'Total Liabilities & Equity']

            'Financial Health Ratios': ['Current Ratio', 'Quick Ratio', 'Financial Leverage', 'Debt/Equity']
            """
