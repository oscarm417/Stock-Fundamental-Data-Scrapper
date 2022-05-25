
import pandas as pd
import requests
import numpy as np
import requests
from dateutil import parser
from datetime import datetime  



class Financials:
    """ Returns a stocks fundamental data:
        Example:
        stocks_fundamental_data = Financials().get_financials('GOOGL')
    """
    def __init__(self):
        self.fundamentals = None
        
    def get_financials(self,ticker):
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
        data = self._get_stock_data(ticker)
        bucket = []
        for i in data:
            bucket.append(self._clean_list2(i))

        bucket = self._remove_empty(bucket)
        df_end_points = [i for i,a in enumerate(bucket) if len(a) == 0]
        tables = self._split_tables(df_end_points,bucket)
        # clean_dates(bucket[2])
        self._clean_tables(tables)
        self._add_dates_label(tables)
        self._add_missing_values(tables)
        financials = self._create_df_collection(tables)
        self.fundamentals = financials
        return self.fundamentals

    def _get_stock_data(self,ticker):
        headers = {
        'Referer': 'http://financials.morningstar.com/ratios/r.html?t=EXPE&region=usa&culture=en-US',
        }

        r = requests.get("http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=XNAS:{}&region=usa&culture=en-US&cur=&order=asc".format(ticker), headers=headers)
        data = r.content.decode('utf-8=sig').split('\n')
        return data
    
    def _clean_list2(self,dirty_list):
        long_num_ind = [i for i,a in enumerate(dirty_list) if a == '"']
        ind_ends = [[long_num_ind[i],long_num_ind[i+1]] for i in range(0,len(long_num_ind),2)]
        possible_ranges = [list(range(i[0],i[1]-1)) for i in ind_ends]
        possible_ranges = [num for sub in possible_ranges for num in sub]

        shift = 0
        for i,a in enumerate(dirty_list):
            try:
                if dirty_list[i] == "," and i in possible_ranges:
                    dirty_list = dirty_list[:i]+dirty_list[i+1:]
                    shift+=1
                    possible_ranges = [num-1 for num in possible_ranges]
            except:
                    pass
        return dirty_list.replace('"','').split(',')

    def _remove_empty(self,bucket):
        bucket2 = []
        for i in bucket:
            temp = []
            for x in i:
                if len(x) != 0:
                    temp.append(x)
            bucket2.append(temp)
        return bucket2

    def _clean_dates(self,date_list):
        dates = []
        for i in date_list:
            if "-" in i:
                dates.append(i.split("-")[0])
            else:
                new_year = int(dates[-1])+1
                dates.append(str(new_year))
        return dates

    def _split_tables(self,df_end_points,bucket):
        tables = []
        df_end_points = [0] + df_end_points
        for i,a in enumerate(df_end_points):
            tables.append(bucket[df_end_points[i-1]:a])
        tables = self._remove_empty(tables)[1:]
        return tables

    def _clean_tables(self,tables):
        lyl = [1,4,5,7]
        lly = [0]
        yl = [2,6]
        ly = [3]
        dic = {}
        for a in range(0,len(tables)):
            table_name = ""

            if a in lly:
                table_name = tables[a][1]
                tables[a] = tables[a][2:]
            elif a in lyl:
                table_name = tables[a][1][0]
                tables[a][1] = tables[a][1][1:]
                tables[a] = tables[a][1:]
            elif a in yl:
                table_name = tables[a][0][0]
                tables[a][0] = tables[a][0][1:]
            else:

                table_name = tables[a][0]
                tables[a] = tables[a][1:]


    def _clean_tables2(self,tables):
        temp = []
        for i in tables:
            temp2 = []
            for d in i:
                if len(d)>1:
                    temp2.append(d)
            temp.append(temp2)
        return temp



    def _add_dates_label(self,tables):
        for i in range(0,len(tables)):
            tables[i][0] = ['Date']+ tables[i][0]

    def _add_missing_values(self,tables):
        for i  in range(0,len(tables)):
            max_count = max(map(len,tables[i]))
            for lst in range(0,len(tables[i])):
                if len(tables[i][lst]) < max_count:
                    times = max_count - len(tables[i][lst])
                    missing_values = [np.nan]*times
                    tables[i][lst] = tables[i][lst]+missing_values

    def _replace_date(self,date):
        if "-" not in date:
            return datetime.today().date()

        else:
            return parser.parse(date)



    def _create_df_collection(self,tables):
        table_names = ['Income Statements','Income % Statements','Return Ratios','Revenue Growth','Cashflow Growth','Balance Sheet','Financial Health Ratios','Inventory Ratios']
        financials = {}
        for count in range(0,7):
            temp_df = pd.DataFrame({i[0]: i[1:] for i in tables[count]})
            dates = [self._replace_date(i) for i in temp_df['Date']]
            temp_df['Date'] = dates
            temp_df = temp_df.set_index("Date",drop = True)
            financials[table_names[count]] = temp_df.astype('float')
        return financials





