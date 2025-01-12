#Importing the necessary Liraries 
#Packaging them in one file to define the dependancies 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_table


#[Valuation Metrics - Single Value Output]



#Creating the function which takes the ticket as input and returns the price to earnings ratio

def get_pe_ratio(ticker):
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    
    try:
        # Get the current price
        current_price = stock.info['currentPrice']
        
        # Get the earnings per share (EPS)
        eps = stock.info['trailingEps']
        
        # Calculate the P/E ratio
        pe_ratio = current_price / eps
        
        return pe_ratio
    except KeyError:
        print(f"Unable to calculate P/E ratio for {ticker}. Required data not available.")
        return None
    
    
#Testing the created function 
#print(get_pe_ratio("AAPL"))






#Creating a function to get the Price to Book Ratio , it takes the ticker as input.

def get_pb_ratio(ticker):
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    
    try:
        # Get the current price
        current_price = stock.info['currentPrice']
        
        # Get the book value per share
        book_value_per_share = stock.info['bookValue']
        
        # Calculate the P/B ratio
        pb_ratio = current_price / book_value_per_share
        
        return pb_ratio
    except KeyError:
        print(f"Unable to calculate P/B ratio for {ticker}. Required data not available.")
        return None

# Testing the created function
#print(get_pb_ratio("AAPL"))




#Creating a function to get the 3.	Price-to-Sales (P/S) Ratio , which takes the ticker as input 

def get_ps_ratio(ticker):
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    
    try:
        # Get the current price
        current_price = stock.info['currentPrice']
        
        # Get the revenue per share
        revenue_per_share = stock.info['revenuePerShare']
        
        # Calculate the P/S ratio
        ps_ratio = current_price / revenue_per_share
        
        return ps_ratio
    except KeyError:
        print(f"Unable to calculate P/S ratio for {ticker}. Required data not available.")
        return None

# Testing the created function
#print(get_ps_ratio("AAPL"))




#Creating a function which gives out the Enterprise Value (EV) and takes the ticker as an input 

def get_enterprise_value(ticker):
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    
    try:
        # Get the enterprise value
        enterprise_value = stock.info['enterpriseValue']
        
        return enterprise_value
    except KeyError:
        print(f"Unable to retrieve Enterprise Value for {ticker}. Required data not available.")
        return None

# Testing the created function
#print(get_enterprise_value("AAPL"))




#Creating a function which gives the EV/EBITDA and takes the ticker as an input 

def get_ev_ebitda(ticker):
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    
    try:
        # Get the Enterprise Value
        enterprise_value = stock.info['enterpriseValue']
        
        # Get the EBITDA
        ebitda = stock.info['ebitda']
        
        # Calculate the EV/EBITDA ratio
        ev_ebitda_ratio = enterprise_value / ebitda
        
        return ev_ebitda_ratio
    except KeyError:
        print(f"Unable to calculate EV/EBITDA ratio for {ticker}. Required data not available.")
        return None

# Testing the created function
#print(get_ev_ebitda("TSLA"))


#[Valuation Metrics - Date input and graph overtime output]



#Creating a function which takes the ticker , start date  and end date as an input and returns a graph made by plotly and dash for 	Price-to-Earnings (P/E) Ratio



def create_pe_ratio_graph(ticker, start_date, end_date):
    # Nested function to fetch and calculate the current P/E ratio using yfinance
    def get_pe_ratio(stock):
        try:
            current_price = stock.info['currentPrice']
            eps = stock.info['trailingEps']  # Fetch trailing EPS

            if eps is None or eps == 0:
                raise ValueError("EPS data not available or invalid")

            pe_ratio = current_price / eps  # Calculate P/E ratio
            return eps, pe_ratio
        except KeyError:
            print(f"Unable to calculate P/E ratio for {ticker}. Required data not available.")
            return None, None

    # Fetch stock data using yfinance
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)

    # Use the nested get_pe_ratio to fetch EPS and calculate the P/E ratio for each date in the range
    try:
        eps, current_pe_ratio = get_pe_ratio(stock)
        if eps is None or eps == 0:
            raise ValueError("EPS data not available or invalid")

        # Calculate P/E ratio for each date (using the same EPS for the date range, due to data limitations)
        stock_data['P/E Ratio'] = stock_data['Close'] / eps
    except KeyError:
        print(f"Unable to fetch EPS data for {ticker}.")
        return

    # Create a dark-themed graph with the area below the line shaded
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['P/E Ratio'],
        mode='lines',
        name=f'{ticker} P/E Ratio',
        line=dict(color='deepskyblue', width=2),  # Neon blue line
        fill='tozeroy',  # Shade the area under the line
        fillcolor='rgba(0, 191, 255, 0.2)',  # Transparent neon blue shade
    ))

    # Add title and axis labels with dark theme
    fig.update_layout(
        title=f'{ticker} P/E Ratio from {start_date} to {end_date}',
        xaxis_title='Date',
        yaxis_title='P/E Ratio',
        template='plotly_dark',  # Dark background theme
        plot_bgcolor='#1e2130',  # Custom background color (dark)
        paper_bgcolor='#1e2130',  # Custom paper color (dark)
        font=dict(color='white'),  # White text for labels
        xaxis=dict(showgrid=False),  # Turn off grid for a cleaner look
        yaxis=dict(showgrid=False)
    )

    # Create a brief summary of the P/E ratio
    pe_mean = stock_data['P/E Ratio'].mean()
    pe_latest = stock_data['P/E Ratio'][-1]

    if pe_latest > pe_mean:
        summary = f"The P/E ratio is higher than the historical average, indicating the stock might be overvalued compared to its past performance."
    else:
        summary = f"The P/E ratio is lower than the historical average, indicating the stock might be undervalued compared to its past performance."

    # Create the Dash layout
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div([
        dcc.Graph(figure=fig),
        html.Hr(),
        html.Div(f"Summary: {summary}", style={'fontSize': 18, 'color': 'white'}),
        html.Div(f"Average P/E Ratio: {pe_mean:.2f}, Latest P/E Ratio: {pe_latest:.2f}", style={'fontSize': 16, 'color': 'white'})
    ], style={'padding': '20px', 'backgroundColor': '#1e2130'})

    # Run the Dash app
    app.run_server(debug=True, use_reloader=False)

# Example usage
#create_pe_ratio_graph('AAPL', '2023-01-01', '2023-12-31')

#Waring use this function to check the P/E Ratio upto a quarter ago as it will take the same 
#EPS for the previous dates and the data wont be accurate.




#Creating a function which takes the ticker , start date , end date and returns the graph for the 	Price-to-Book (P/B) Ratio



def create_pb_ratio_graph(ticker, start_date, end_date):
    # Nested function to fetch and calculate the book value and P/B ratio using yfinance
    def get_book_value(stock):
        try:
            # Fetch quarterly earnings and book value data
            quarterly_data = stock.quarterly_balance_sheet
            book_value = quarterly_data.loc['Total Assets'] - quarterly_data.loc['Total Liabilities Net Minority Interest']
            return book_value
        except KeyError:
            print(f"Unable to fetch book value data for {ticker}. Required data not available.")
            return None

    # Fetch stock data using yfinance
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)

    # Remove timezone info from the stock_data index
    stock_data.index = stock_data.index.tz_localize(None)

    # Use the nested get_book_value to fetch book value and calculate the P/B ratio for each date in the range
    book_value = get_book_value(stock)
    if book_value is None or book_value.empty:
        print(f"Unable to fetch book value for {ticker}.")
        return

    # Remove timezone info from book_value index
    book_value.index = book_value.index.tz_localize(None)

    # Convert the book value Series to a DataFrame to align with stock data index
    book_value = book_value.reindex(stock_data.index, method='ffill')  # Forward fill to align dates
    stock_data['P/B Ratio'] = stock_data['Close'] / book_value

    # Create a dark-themed graph with the area below the line shaded
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['P/B Ratio'],
        mode='lines',
        name=f'{ticker} P/B Ratio',
        line=dict(color='deepskyblue', width=2),  # Neon blue line
        fill='tozeroy',  # Shade the area under the line
        fillcolor='rgba(0, 191, 255, 0.2)',  # Transparent neon blue shade
    ))

    # Add title and axis labels with dark theme
    fig.update_layout(
        title=f'{ticker} P/B Ratio from {start_date} to {end_date}',
        xaxis_title='Date',
        yaxis_title='P/B Ratio',
        template='plotly_dark',  # Dark background theme
        plot_bgcolor='#1e2130',  # Custom background color (dark)
        paper_bgcolor='#1e2130',  # Custom paper color (dark)
        font=dict(color='white'),  # White text for labels
        xaxis=dict(showgrid=False),  # Turn off grid for a cleaner look
        yaxis=dict(showgrid=False)
    )

    # Create a brief summary of the P/B ratio
    pb_mean = stock_data['P/B Ratio'].mean()
    pb_latest = stock_data['P/B Ratio'][-1]

    if pb_latest > pb_mean:
        summary = f"The P/B ratio is higher than the historical average, indicating the stock might be overvalued compared to its past performance."
    else:
        summary = f"The P/B ratio is lower than the historical average, indicating the stock might be undervalued compared to its past performance."

    # Create the Dash layout
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div([
        dcc.Graph(figure=fig),
        html.Hr(),
        html.Div(f"Summary: {summary}", style={'fontSize': 18, 'color': 'white'}),
        html.Div(f"Average P/B Ratio: {pb_mean:.2f}, Latest P/B Ratio: {pb_latest:.2f}", style={'fontSize': 16, 'color': 'white'})
    ], style={'padding': '20px', 'backgroundColor': '#1e2130'})

    # Run the Dash app
    app.run_server(debug=True, use_reloader=False)

# Example usage
#create_pb_ratio_graph('AAPL', '2023-01-01', '2023-12-31')



#Create a function which takes the ticker , start date , end date as input and gives out the graph  for the 	Price-to-Sales (P/S) Ratio for the output.



# Function to calculate and plot the Price-to-Sales (P/S) Ratio
def plot_ps_ratio(ticker, start_date, end_date):
    # Get stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    
    # Fetch historical stock price data
    stock_data = stock.history(start=start_date, end=end_date)
    
    # Get the number of shares outstanding (we assume it to be constant, or use the latest value)
    shares_outstanding = stock.get_info().get('sharesOutstanding')
    
    # Get revenue (you can expand this to get quarterly or annual data)
    financials = stock.financials
    revenue = financials.loc['Total Revenue']
    
    # Calculate Market Cap for each day (Close Price * Shares Outstanding)
    stock_data['Market Cap'] = stock_data['Close'] * shares_outstanding
    
    # Convert revenue from a single point (total yearly revenue) to a series (we use the latest revenue)
    # Ideally, you would pull quarterly revenue and interpolate between periods
    latest_revenue = revenue[0]  # Use the latest available revenue
    
    # Calculate the P/S Ratio for each day
    stock_data['P/S Ratio'] = stock_data['Market Cap'] / latest_revenue
    
    # Create a line graph with Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['P/S Ratio'],
        mode='lines',
        name=f'{ticker} P/S Ratio'
    ))
    
    # Dark theme for the graph
    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} Price-to-Sales (P/S) Ratio",
        xaxis_title="Date",
        yaxis_title="P/S Ratio",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
    )
    
    # Dash App
    app = Dash(__name__)
    
    # Layout of the App
    app.layout = html.Div([
        html.H1(f"Price-to-Sales (P/S) Ratio for {ticker}"),
        dcc.Graph(figure=fig)
    ])
    
    # Run the Dash app
    app.run_server(debug=True, use_reloader=False)

# Example usage of the function
#plot_ps_ratio('AAPL', '2022-01-01', '2024-01-01')



#Creating a function which takes the ticker as an input and returns the table of the valuation metrics using dash 

# Function to fetch valuation metrics for a given stock ticker
def valuation_metrics_mk(ticker):
    stock = yf.Ticker(ticker)
    
    # Get the stock financials, key stats, and balance sheet data
    pe_ratio = stock.info.get('trailingPE')
    pb_ratio = stock.info.get('priceToBook')
    ps_ratio = stock.info.get('priceToSalesTrailing12Months')
    ev = stock.info.get('enterpriseValue')
    ev_ebitda = stock.info.get('enterpriseToEbitda')

    # Table data for Dash
    data = [{
        "Metric": "P/E Ratio",
        "Value": pe_ratio
    }, {
        "Metric": "P/B Ratio",
        "Value": pb_ratio
    }, {
        "Metric": "P/S Ratio",
        "Value": ps_ratio
    }, {
        "Metric": "Enterprise Value (EV)",
        "Value": ev
    }, {
        "Metric": "EV/EBITDA",
        "Value": ev_ebitda
    }]

    return data


# Dash App setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Valuation Metrics"),
    
    dcc.Input(id='ticker-input', type='text', value='AAPL', style={'marginRight': '10px'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    
    dash_table.DataTable(
        id='valuation-table',
        columns=[
            {'name': 'Metric', 'id': 'Metric'},
            {'name': 'Value', 'id': 'Value'}
        ],
        data=[],
        style_table={'width': '50%'}
    )
])

@app.callback(
    Output('valuation-table', 'data'),
    [Input('submit-val', 'n_clicks')],
    [Input('ticker-input', 'value')]
)
def update_table(n_clicks, ticker):
    if n_clicks > 0:
        # Fetch and return the valuation metrics for the given stock ticker
        return valuation_metrics_mk(ticker)
    return []


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
  
  
#Testing the feature   
    
#valuation_metrics_mk('TSLA')

#valuation_metrics_mk('AAPL')
    

    

    
    
#[Profitability Metrics]


#Creating a function which takes the ticker as an input and returns the 	Gross Margin.

def get_gross_margin(ticker):
    try:
        # Fetch the stock data
        stock = yf.Ticker(ticker)
        
        # Get the financial data
        financials = stock.financials
        
        # Calculate Gross Margin
        revenue = financials.loc['Total Revenue'].iloc[0]
        cogs = financials.loc['Cost Of Revenue'].iloc[0]
        gross_profit = revenue - cogs
        gross_margin = (gross_profit / revenue) * 100
        
        return round(gross_margin, 2)
    except Exception as e:
        print(f"Error calculating Gross Margin for {ticker}: {str(e)}")
        return None

# Example usage:
# gross_margin = get_gross_margin('AAPL')
# print(f"Gross Margin: {gross_margin}%")

#get_gross_margin('AAPL')


#Creating a function which takes the ticker as an input and returns the  Operating Margin

def get_operating_margin(ticker):
    try:
        # Fetch the stock data
        stock = yf.Ticker(ticker)
        
        # Get the financial data
        financials = stock.financials
        
        # Calculate Operating Margin
        revenue = financials.loc['Total Revenue'].iloc[0]
        operating_income = financials.loc['Operating Income'].iloc[0]
        operating_margin = (operating_income / revenue) * 100
        
        return round(operating_margin, 2)
    except Exception as e:
        print(f"Error calculating Operating Margin for {ticker}: {str(e)}")
        return None

# Example usage:
# operating_margin = get_operating_margin('AAPL')
# print(f"Operating Margin: {operating_margin}%")

#get_operating_margin('AAPL')




# Creating a function which takes the ticker as input and returns the Net Profit Margin

def get_net_profit_margin(ticker):
    try:
        # Fetch the stock data
        stock = yf.Ticker(ticker)
        
        # Get the financial data
        financials = stock.financials
        
        # Calculate Net Profit Margin
        revenue = financials.loc['Total Revenue'].iloc[0]
        net_income = financials.loc['Net Income'].iloc[0]
        net_profit_margin = (net_income / revenue) * 100
        
        return round(net_profit_margin, 2)
    except Exception as e:
        print(f"Error calculating Net Profit Margin for {ticker}: {str(e)}")
        return None

# Example usage:
# net_profit_margin = get_net_profit_margin('AAPL')
# print(f"Net Profit Margin: {net_profit_margin}%")

#get_net_profit_margin('AAPL')



# Creating a function which takes the ticker as input and returns the 	Return on Equity (ROE)

def get_return_on_equity(ticker):
    try:
        # Fetch the stock data
        stock = yf.Ticker(ticker)
        
        # Get the financial data and balance sheet
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        
        # Calculate Return on Equity (ROE)
        net_income = financials.loc['Net Income'].iloc[0]
        stockholders_equity = balance_sheet.loc['Stockholders Equity'].iloc[0]
        roe = (net_income / stockholders_equity) * 100
        
        return round(roe, 2)
    except Exception as e:
        print(f"Error calculating Return on Equity (ROE) for {ticker}: {str(e)}")
        return None

# Example usage:
# roe = get_return_on_equity('AAPL')
# print(f"Return on Equity (ROE): {roe}%")

#get_return_on_equity('AAPL')





#Creating a function which takes the ticker as an input and returns the profitability metrics as an output.

def profitability_metrics_finance(ticker):
    stock = yf.Ticker(ticker)

    # Get the stock financials and balance sheet data
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    
    # Calculate metrics
    try:
        # Retrieve necessary values
        gross_profit = financials.loc['Gross Profit'].iloc[0]
        total_revenue = financials.loc['Total Revenue'].iloc[0]
        operating_income = financials.loc['Operating Income'].iloc[0]
        net_income = financials.loc['Net Income'].iloc[0]
        total_assets = balance_sheet.loc['Total Assets'].iloc[0]
        stockholders_equity = balance_sheet.loc['Stockholders Equity'].iloc[0]
        
        # Calculate margins and ratios
        gross_margin = (gross_profit / total_revenue) * 100 if total_revenue != 0 else 0
        operating_margin = (operating_income / total_revenue) * 100 if total_revenue != 0 else 0
        net_profit_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 0
        roe = (net_income / stockholders_equity) * 100 if stockholders_equity != 0 else 0
        roa = (net_income / total_assets) * 100 if total_assets != 0 else 0

        # Prepare the data to return
        data = [
            {"Metric": "Gross Margin", "Value": f"{gross_margin:.2f}%"},
            {"Metric": "Operating Margin", "Value": f"{operating_margin:.2f}%"},
            {"Metric": "Net Profit Margin", "Value": f"{net_profit_margin:.2f}%"},
            {"Metric": "Return on Equity (ROE)", "Value": f"{roe:.2f}%"},
            {"Metric": "Return on Assets (ROA)", "Value": f"{roa:.2f}%"}
        ]

        return data
    
    except Exception as e:
        return f"Error calculating profitability metrics for {ticker}: {str(e)}"

# Example usage:
# metrics = profitability_metrics_finance('AAPL')
# for metric in metrics:
#     print(f"{metric['Metric']}: {metric['Value']}")

#Testing the feature 

#profitability_metrics_finance('TSLA')



#A function which takes the ticker as input and gives out the Earnings Per Share EPS growth as output 

def get_eps_growth(ticker):
    # Download stock data
    stock = yf.Ticker(ticker)
    try:
        # Fetch net income and shares outstanding data
        financials = stock.financials  # Annual financial statements
        net_income = financials.loc['Net Income'] if 'Net Income' in financials.index else None
        shares_outstanding = stock.info.get("sharesOutstanding")

        # Ensure both values are available for EPS calculation
        if net_income is not None and shares_outstanding:
            # Calculate EPS for the last two years if available
            eps_last_year = net_income.iloc[1] / shares_outstanding
            eps_two_years_ago = net_income.iloc[2] / shares_outstanding
            # Calculate EPS growth
            eps_growth = ((eps_last_year - eps_two_years_ago) / eps_two_years_ago) * 100
            return f"{eps_growth:.2f}% EPS Growth"
        else:
            return "Not enough data to calculate EPS growth."

    except Exception as e:
        return f"Error: Could not retrieve EPS growth data for {ticker}. Details: {e}"

#get_eps_growth('TSLA')



#Creating a function to show the Revenue Growth Rate and takes the ticker as an input. 


def get_revenue_growth_rate(ticker):
    # Download stock data
    stock = yf.Ticker(ticker)
    try:
        # Fetch revenue data from the financials statement
        financials = stock.financials  # Annual financial statements
        revenue = financials.loc['Total Revenue'] if 'Total Revenue' in financials.index else None

        # Ensure revenue data is available and has at least two years of data
        if revenue is not None and len(revenue) >= 2:
            # Calculate revenue growth rate based on the latest two years
            revenue_growth = ((revenue.iloc[0] - revenue.iloc[1]) / revenue.iloc[1]) * 100
            return f"{revenue_growth:.2f}% Revenue Growth Rate"
        else:
            return "Not enough revenue data available to calculate growth rate."

    except Exception as e:
        return f"Error: Could not retrieve revenue growth data for {ticker}. Details: {e}"

# Example usage

#get_revenue_growth_rate('AAPL')
#get_revenue_growth_rate('TATAMOTORS.NS')




#Creating a function which takes the ticker as input and gives out the Debt-to-Equity Ratio.

def get_debt_to_equity_ratio(ticker):
    # Fetch the stock's balance sheet data
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet

    # Print available row labels to identify the exact label names
    print("Available labels in balance sheet:", balance_sheet.index)

    # Set the labels based on available data
    total_liabilities_label = 'Total Liabilities Net Minority Interest'
    total_equity_label = 'Stockholders Equity'

    # Extract Total Liabilities and Shareholders' Equity
    try:
        total_liabilities = balance_sheet.loc[total_liabilities_label][0]
        total_shareholder_equity = balance_sheet.loc[total_equity_label][0]

        # Calculate Debt-to-Equity Ratio
        debt_to_equity_ratio = total_liabilities / total_shareholder_equity
        return debt_to_equity_ratio

    except KeyError as e:
        return f"Key error: {e}. Check if the label names have changed."
    except Exception as e:
        return f"An error occurred: {e}"
    
    
# Example usage:

#get_debt_to_equity_ratio("AAPL")



#Creating a function which takes the ticker as an input and returns the	Interest Coverage Ratio


def get_interest_coverage_ratio(ticker):
    # Fetch the stock's financial data
    stock = yf.Ticker(ticker)

    # Get the income statement data
    income_statement = stock.financials

    # Print available row labels in the income statement
    print("Available labels in income statement:", income_statement.index)

    try:
        # Extract EBIT (Operating Income) and Interest Expense
        ebit = income_statement.loc['Operating Income'][0]  # This is often used as EBIT
        interest_expense = income_statement.loc['Interest Expense'][0]

        # Calculate Interest Coverage Ratio
        interest_coverage_ratio = ebit / interest_expense
        return interest_coverage_ratio

    except KeyError as e:
        return f"Key error: {e}. Check if the label names have changed."
    except Exception as e:
        return f"An error occurred: {e}"
    

# Example usage

#get_interest_coverage_ratio("AAPL")




#Creating a function which takes the ticker as an input and returns the	Total Debt/Total Assets

def get_total_debt_to_total_assets_ratio(ticker):
    # Fetch the stock's balance sheet data
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet

    # Print available row labels to identify the exact label names
    print("Available labels in balance sheet:", balance_sheet.index)

    try:
        # Extract Total Debt and Total Assets
        total_debt = balance_sheet.loc['Total Debt'][0]  # This often represents the total liabilities
        total_assets = balance_sheet.loc['Total Assets'][0]

        # Calculate Total Debt to Total Assets Ratio
        total_debt_to_total_assets_ratio = total_debt / total_assets
        return total_debt_to_total_assets_ratio

    except KeyError as e:
        return f"Key error: {e}. Check if the label names have changed."
    except Exception as e:
        return f"An error occurred: {e}"
    
    
#get_total_debt_to_total_assets_ratio("AAPL")

#x = get_total_debt_to_total_assets_ratio("AAPL")



#Creating a function which takes the ticker as an input and returns the Asset Turnover Ratio

def asset_turnover_ratio(ticker: str) -> float:
    # Fetch financial data
    stock = yf.Ticker(ticker)
    
    # Get the total revenue (net sales) for the last fiscal year
    financials = stock.financials
    revenue = financials.loc['Total Revenue'][0] if 'Total Revenue' in financials.index else None

    # Get the total assets for the last two fiscal years to compute average assets
    balance_sheet = stock.balance_sheet
    if 'Total Assets' in balance_sheet.index:
        total_assets_end = balance_sheet.loc['Total Assets'][0]
        total_assets_start = balance_sheet.loc['Total Assets'][1] if balance_sheet.shape[1] > 1 else None
    else:
        return None  # Return None if 'Total Assets' not available

    # Calculate the average total assets
    if total_assets_start is not None:
        avg_total_assets = (total_assets_end + total_assets_start) / 2
    else:
        avg_total_assets = total_assets_end

    # Calculate Asset Turnover Ratio
    if revenue and avg_total_assets:
        asset_turnover_ratio = revenue / avg_total_assets
        return asset_turnover_ratio
    else:
        return None  # Return None if data is missing
    


# Example usage:
#asset_turnover_ratio('AAPL')


#Creating a function which takes the ticker as an input and returns the Inventory Turnover Ratio

def inventory_turnover_ratio(ticker: str) -> float:
    # Fetch financial data
    stock = yf.Ticker(ticker)
    
    # Get the Cost of Goods Sold (COGS) for the last fiscal year
    financials = stock.financials
    cogs = financials.loc['Cost Of Revenue'][0] if 'Cost Of Revenue' in financials.index else None

    # Get the inventory values for the last two fiscal years to compute average inventory
    balance_sheet = stock.balance_sheet
    if 'Inventory' in balance_sheet.index:
        inventory_end = balance_sheet.loc['Inventory'][0]
        inventory_start = balance_sheet.loc['Inventory'][1] if balance_sheet.shape[1] > 1 else None
    else:
        return None  # Return None if 'Inventory' is not available

    # Calculate the average inventory
    if inventory_start is not None:
        avg_inventory = (inventory_end + inventory_start) / 2
    else:
        avg_inventory = inventory_end

    # Calculate Inventory Turnover Ratio
    if cogs and avg_inventory:
        inventory_turnover_ratio = cogs / avg_inventory
        return inventory_turnover_ratio
    else:
        return None  # Return None if data is missing

# Example usage:
# inventory_turnover_ratio('AAPL')



#Creating a function which takes the ticker as an input and returns the Day Sales Outstanding 

def days_sales_outstanding(ticker: str, days: int = 365) -> float:
    # Fetch financial data
    stock = yf.Ticker(ticker)
    
    # Get the total revenue (net sales) for the last fiscal year
    financials = stock.financials
    print("Financials Data:\n", financials)  # Print financials data to debug
    
    # Check for alternative names for total revenue
    revenue = None
    if 'Total Revenue' in financials.index:
        revenue = financials.loc['Total Revenue'].iloc[0]
    elif 'Revenues' in financials.index:
        revenue = financials.loc['Revenues'].iloc[0]
    elif 'Net Sales' in financials.index:
        revenue = financials.loc['Net Sales'].iloc[0]
    else:
        print(f"Total Revenue or equivalent not found for {ticker}")
    
    # Get the accounts receivable for the last fiscal year from the balance sheet
    balance_sheet = stock.balance_sheet
    print("Balance Sheet Data:\n", balance_sheet)  # Print balance sheet data to debug
    
    # Check for alternative names for accounts receivable
    accounts_receivable = None
    if 'Net Receivables' in balance_sheet.index:
        accounts_receivable = balance_sheet.loc['Net Receivables'].iloc[0]
    elif 'Receivables' in balance_sheet.index:
        accounts_receivable = balance_sheet.loc['Receivables'].iloc[0]
    elif 'Trade Receivables' in balance_sheet.index:
        accounts_receivable = balance_sheet.loc['Trade Receivables'].iloc[0]
    else:
        print(f"Net Receivables or equivalent not found for {ticker}")
    
    # Calculate DSO if data is available
    if revenue and accounts_receivable:
        dso = (accounts_receivable / revenue) * days
        return dso
    else:
        return None  # Return None if data is missing

# Example usage:
# days_sales_outstanding('AAPL', days=365)



#Creating a function which returns the financials data of the stock from yahoo finance 

def get_detailed_financials(ticker: str):
    # Fetch the stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    
    # Get the financials data
    financials = stock.financials
    
    # Return the financials data
    return financials

# Example usage:
#get_detailed_financials('AAPL')



#Creating a functio which takes the ticker as input and returns the Dividend Yield

def get_dividend_yield(ticker_symbol):
    """
    Fetches the dividend yield of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        float: The dividend yield as a percentage, or None if no dividend yield is available.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        dividend_yield = stock.info.get('dividendYield')
        
        if dividend_yield is not None:
            return round(dividend_yield * 100, 2)  # Convert to percentage
        else:
            print(f"No dividend yield data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None
    
    
#Usage example:

# get_dividend_yield('AAPL')


#Creating a function which takes the ticker as input and returns the Dividend Payout Ratio

def get_dividend_payout_ratio(ticker_symbol):
    """
    Fetches the dividend payout ratio of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        float: The dividend payout ratio as a percentage, or None if no data is available.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        payout_ratio = stock.info.get('payoutRatio')
        
        if payout_ratio is not None:
            return round(payout_ratio * 100, 2)  # Convert to percentage
        else:
            print(f"No dividend payout ratio data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None
    

#Usage Example 

# get_dividend_payout_ratio('AAPL')



#Creating a function which takes the ticker as input and returns the Dividend Growth Rate

def get_dividend_growth_rate(ticker_symbol, years=5):
    """
    Calculates the dividend growth rate of a stock over a given number of years using yfinance.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        years (int): The number of years over which to calculate the growth rate.

    Returns:
        float: The dividend growth rate as a percentage, or None if data is unavailable.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        # Fetch historical dividend data
        dividends = stock.dividends
        
        if dividends.empty:
            print(f"No dividend data available for {ticker_symbol}.")
            return None

        # Filter dividends for the last 'years' years
        recent_dividends = dividends.last(f'{years}Y')

        if len(recent_dividends) < 2:
            print(f"Not enough dividend data for {ticker_symbol} to calculate growth rate.")
            return None

        # Calculate CAGR for dividends
        first_dividend = recent_dividends[0]
        last_dividend = recent_dividends[-1]
        num_years = (recent_dividends.index[-1] - recent_dividends.index[0]).days / 365.25

        if first_dividend > 0 and last_dividend > 0:
            cagr = ((last_dividend / first_dividend) ** (1 / num_years) - 1) * 100
            return round(cagr, 2)
        else:
            print(f"Dividend values are invalid for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None


# get_dividend_growth_rate('AAPL', years=5)




#Creating a function which takes the ticker as input and returns the Market Capitalization

def get_market_cap(ticker_symbol):
    """
    Fetches the market capitalization of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        str: The market capitalization formatted as a human-readable string, 
             or None if no data is available.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        market_cap = stock.info.get('marketCap')
        
        if market_cap is not None:
            # Format the market cap into billions/trillions for readability
            if market_cap >= 1e12:
                formatted_cap = f"${market_cap / 1e12:.2f} Trillion"
            elif market_cap >= 1e9:
                formatted_cap = f"${market_cap / 1e9:.2f} Billion"
            elif market_cap >= 1e6:
                formatted_cap = f"${market_cap / 1e6:.2f} Million"
            else:
                formatted_cap = f"${market_cap:.2f}"
            
            return formatted_cap
        else:
            print(f"No market capitalization data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None
    


#Example Usecase 
# get_market_cap('AAPL')




#Create a function which takes the ticker as input and returns the Beta

def get_beta(ticker_symbol):
    """
    Fetches the Beta (volatility measure) of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        float: The Beta value, or None if no data is available.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        beta = stock.info.get('beta')
        
        if beta is not None:
            return round(beta, 2)
        else:
            print(f"No Beta data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None
    
    
#Example Usecase 
# get_beta('AAPL')




#Create a function which takes the ticker as input and returns the 52-week High and Low
def get_52_week_high_low(ticker_symbol):
    """
    Fetches the 52-week high and low prices of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        tuple: A tuple containing the 52-week high and low prices as floats, or None if data is unavailable.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        high_52_week = stock.info.get('fiftyTwoWeekHigh')
        low_52_week = stock.info.get('fiftyTwoWeekLow')
        
        if high_52_week is not None and low_52_week is not None:
            return round(high_52_week, 2), round(low_52_week, 2)
        else:
            print(f"No 52-week high/low data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None
    
    
#Example Usecase
# get_52_week_high_low('AAPL')


#Create a function which takes the ticker as input and returns the average trading volume
def get_average_volume(ticker_symbol):
    """
    Fetches the average trading volume of a stock using the yfinance library.

    Parameters:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
        int: The average volume, or None if no data is available.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        avg_volume = stock.info.get('averageVolume')

        if avg_volume is not None:
            return avg_volume
        else:
            print(f"No average volume data available for {ticker_symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None


#Example Usecase
# get_average_volume('AAPL')




#Creating a function which takes the ticker as input and returns the moving averages 


def calculate_moving_averages(ticker):
    """
    Fetches historical stock data for the given ticker and calculates Simple and Exponential Moving Averages.

    Parameters:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        dict: A dictionary containing SMAs and EMAs for different periods.
    """
    try:
        # Download historical data for the past year
        stock_data = yf.download(ticker, period="1y")
        
        if stock_data.empty:
            raise ValueError("No data found for the ticker.")

        # Calculate moving averages for specified periods
        periods = [5, 10, 20, 50, 100, 200]
        moving_averages = {}

        for period in periods:
            sma_column = f'SMA_{period}'
            ema_column = f'EMA_{period}'

            # Simple Moving Average (SMA)
            stock_data[sma_column] = stock_data['Close'].rolling(window=period).mean()

            # Exponential Moving Average (EMA)
            stock_data[ema_column] = stock_data['Close'].ewm(span=period, adjust=False).mean()

            moving_averages[sma_column] = stock_data[sma_column].iloc[-1]
            moving_averages[ema_column] = stock_data[ema_column].iloc[-1]

        return moving_averages

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    
#Example Usecase
#calculate_moving_averages('AAPL')




#Creating a function which takes the ticker as an input and returns the Relative Strength Index

def calculate_rsi(ticker, period=14):
    """
    Fetches historical stock data for the given ticker and calculates the Relative Strength Index (RSI).

    Parameters:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        period (int): The lookback period for RSI calculation. Default is 14.

    Returns:
        float: The RSI value.
    """
    try:
        # Download historical data for the past year
        stock_data = yf.download(ticker, period="1y")
        
        if stock_data.empty:
            raise ValueError("No data found for the ticker.")

        # Calculate price changes
        delta = stock_data['Close'].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate average gain and loss
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        # Calculate the Relative Strength (RS)
        rs = avg_gain / avg_loss

        # Calculate the Relative Strength Index (RSI)
        rsi = 100 - (100 / (1 + rs))

        # Return the most recent RSI value
        return rsi.iloc[-1]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    
#Example Usecase
#calculate_rsi('AAPL', period=14)



#Creating a function which takes the ticker as an input and returns the MACD 

def calculate_macd(ticker, short_period=12, long_period=26, signal_period=9):
    """
    Fetches historical stock data for the given ticker and calculates the MACD and Signal line values.

    Parameters:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        short_period (int): The short EMA period. Default is 12.
        long_period (int): The long EMA period. Default is 26.
        signal_period (int): The signal line EMA period. Default is 9.

    Returns:
        dict: A dictionary containing the latest MACD line and Signal line values.
    """
    try:
        # Download historical data for the past year
        stock_data = yf.download(ticker, period="1y")
        
        if stock_data.empty:
            raise ValueError("No data found for the ticker.")

        # Calculate the short-term EMA (12-day by default)
        stock_data['Short_EMA'] = stock_data['Close'].ewm(span=short_period, adjust=False).mean()

        # Calculate the long-term EMA (26-day by default)
        stock_data['Long_EMA'] = stock_data['Close'].ewm(span=long_period, adjust=False).mean()

        # Calculate the MACD line
        stock_data['MACD'] = stock_data['Short_EMA'] - stock_data['Long_EMA']

        # Calculate the Signal line (9-day EMA of MACD by default)
        stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=signal_period, adjust=False).mean()

        # Get the latest values
        macd_line = stock_data['MACD'].iloc[-1]
        signal_line = stock_data['Signal_Line'].iloc[-1]

        return {'MACD_Line': macd_line, 'Signal_Line': signal_line}

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
#example usecase
#calculate_macd('AAPL', short_period=12, long_period=26, signal_period=9)




#Creating a function whch takes the ticker as a input and returns the Current Ratio


def calculate_current_ratio(ticker):
    """
    Fetches balance sheet data for the given ticker and calculates the Current Ratio.
    
    Current Ratio = Current Assets / Current Liabilities

    Parameters:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        float: The Current Ratio, or None if the data is unavailable.
    """
    try:
        # Download financial information
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet

        # Debugging: Print the balance sheet data to check the structure
        print(balance_sheet)

        # Try to fetch "Total Current Assets" and "Total Current Liabilities"
        if balance_sheet.empty:
            raise ValueError("Balance sheet data is not available for this ticker.")
        
        # Adjust labels based on actual structure
        current_assets_label = 'Current Assets' if 'Current Assets' in balance_sheet.index else 'Total Current Assets'
        current_liabilities_label = 'Current Liabilities' if 'Current Liabilities' in balance_sheet.index else 'Total Current Liabilities'

        # Extract values
        current_assets = balance_sheet.loc[current_assets_label].iloc[0]
        current_liabilities = balance_sheet.loc[current_liabilities_label].iloc[0]

        # Calculate Current Ratio
        if current_liabilities == 0:
            raise ValueError("Current liabilities are zero, division by zero is not allowed.")

        current_ratio = current_assets / current_liabilities
        return current_ratio

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



#Example Usecase 
#calculate_current_ratio('AAPL')



#Creating a function which takes the ticker as input and returns the Quick Ratio

def calculate_quick_ratio(ticker):
    """
    Fetches balance sheet data for the given ticker and calculates the Quick Ratio.
    
    Quick Ratio = (Current Assets - Inventory) / Current Liabilities

    Parameters:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        float: The Quick Ratio, or None if the data is unavailable.
    """
    try:
        # Download financial information
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet

        # Debugging: Print the balance sheet data to check its structure
        print(balance_sheet)

        # Ensure balance sheet data is available
        if balance_sheet.empty:
            raise ValueError("Balance sheet data is not available for this ticker.")

        # Adjust labels based on actual structure
        current_assets_label = 'Current Assets' if 'Current Assets' in balance_sheet.index else 'Total Current Assets'
        current_liabilities_label = 'Current Liabilities' if 'Current Liabilities' in balance_sheet.index else 'Total Current Liabilities'
        inventory_label = 'Inventory' if 'Inventory' in balance_sheet.index else None

        # Extract values
        current_assets = balance_sheet.loc[current_assets_label].iloc[0]
        current_liabilities = balance_sheet.loc[current_liabilities_label].iloc[0]
        inventory = balance_sheet.loc[inventory_label].iloc[0] if inventory_label else 0

        # Check for division by zero
        if current_liabilities == 0:
            raise ValueError("Current liabilities are zero, division by zero is not allowed.")

        # Calculate Quick Ratio
        quick_ratio = (current_assets - inventory) / current_liabilities
        return quick_ratio

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

#Example Usecase
#calculate_quick_ratio('AAPL')




#Creating a function which takes the ticker as input and retuns a dark themed graph for Price Chart (Candlestick or Line) using dash , yfinance and plotily 

# Single function to create Dash app with stock price chart
def create_price_chart():
    app = dash.Dash(__name__)
    
    # Function to fetch stock data using yfinance
    def fetch_stock_data(ticker, period='1y'):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data

    # Function to generate stock price chart using plotly
    def create_stock_chart(data, chart_type='candlestick'):
        fig = go.Figure()

        if chart_type == 'candlestick':
            fig.add_trace(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         name='Candlestick'))
        else:  # Line chart
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Line'))

        # Dark theme settings
        fig.update_layout(
            template="plotly_dark",
            title=f"Stock Price Chart ({chart_type.capitalize()})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            font=dict(color="white"),
            plot_bgcolor="black",
            paper_bgcolor="black",
            hovermode="x",
        )
        return fig

    # Layout for the Dash app
    app.layout = html.Div(
        style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'},
        children=[
            html.H1("Stock Price Dashboard", style={'textAlign': 'center'}),
            
            # Input for ticker symbol
            html.Label("Enter Stock Ticker:", style={'font-size': '20px'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': 'orange'}), 
            
            # Dropdown for duration
            html.Label("Select Duration:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': 'orange'}
            ),
            
            # Dropdown for chart type
            html.Label("Select Chart Type:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Candlestick', 'value': 'candlestick'},
                    {'label': 'Line', 'value': 'line'},
                ],
                value='candlestick',
                style={'font-size': '20px', 'color': 'orange'}
            ),
            
            # Graph to display stock price chart
            dcc.Graph(id='price-chart', style={'height': '600px'}),
        ]
    )

    # Callback to update the chart based on user inputs
    @app.callback(
        Output('price-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value'),
        Input('chart-type-dropdown', 'value')
    )
    def update_chart(ticker, period, chart_type):
        # Fetch the stock data
        data = fetch_stock_data(ticker, period)
        
        # Generate the chart
        fig = create_stock_chart(data, chart_type)
        return fig

    # Run the Dash app
    app.run_server(debug=True)

# Call the function to launch the app
#create_price_chart()



#Creating a function to return the volume chart and has the options for duration and input stock 


# Function to create Dash app with stock volume chart
def create_volume_chart():
    app = dash.Dash(__name__)

    # Function to fetch stock data using yfinance
    def fetch_stock_data(ticker, period='1y'):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data

    # Function to generate stock volume chart using plotly
    def create_volume_chart(data):
        fig = go.Figure()

        # Adding volume trace
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))

        # Dark theme settings
        fig.update_layout(
            template="plotly_dark",
            title="Stock Volume Chart",
            xaxis_title="Date",
            yaxis_title="Volume",
            font=dict(color="white"),
            plot_bgcolor="black",
            paper_bgcolor="black",
            hovermode="x",
        )
        return fig

    # Layout for the Dash app
    app.layout = html.Div(
        style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'},
        children=[
            html.H1("Stock Volume Dashboard", style={'textAlign': 'center'}),

            # Input for ticker symbol
            html.Label("Enter Stock Ticker:", style={'font-size': '20px'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': 'orange'}),
            
            # Dropdown for duration
            html.Label("Select Duration:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': 'orange'}
            ),
            
            # Graph to display stock volume chart
            dcc.Graph(id='volume-chart', style={'height': '600px'}),
        ]
    )

    # Callback to update the chart based on user inputs
    @app.callback(
        Output('volume-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = fetch_stock_data(ticker, period)
        
        # Generate the volume chart
        fig = create_volume_chart(data)
        return fig

    # Run the Dash app
    app.run_server(debug=True)

# Call the function to launch the app
#create_volume_chart()



#Creating a function which returns the MACD chart and has the options for duration and input stock

# Function to create Dash app with MACD chart
def macd_dashboard():
    app = dash.Dash(__name__)

    # Function to fetch stock data using yfinance
    def fetch_stock_data(ticker, period='1y'):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data

    # Function to calculate MACD
    def calculate_macd(data):
        short_ema = data['Close'].ewm(span=12, adjust=False).mean()  # 12-period EMA
        long_ema = data['Close'].ewm(span=26, adjust=False).mean()   # 26-period EMA
        macd = short_ema - long_ema  # MACD line
        signal = macd.ewm(span=9, adjust=False).mean()  # Signal line
        return macd, signal

    # Function to generate MACD chart using plotly
    def create_macd_chart(data):
        macd, signal = calculate_macd(data)
        fig = go.Figure()

        # MACD line trace
        fig.add_trace(go.Scatter(x=data.index, y=macd, mode='lines', name='MACD Line'))

        # Signal line trace
        fig.add_trace(go.Scatter(x=data.index, y=signal, mode='lines', name='Signal Line'))

        # Bar plot for MACD histogram
        fig.add_trace(go.Bar(x=data.index, y=macd - signal, name='MACD Histogram'))

        # Dark theme settings
        fig.update_layout(
            template="plotly_dark",
            title="MACD (Moving Average Convergence Divergence)",
            xaxis_title="Date",
            yaxis_title="MACD",
            font=dict(color="white"),
            plot_bgcolor="black",
            paper_bgcolor="black",
            hovermode="x",
        )
        return fig

    # Layout for the Dash app
    app.layout = html.Div(
        style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'},
        children=[
            html.H1("MACD Dashboard", style={'textAlign': 'center'}),

            # Input for ticker symbol
            html.Label("Enter Stock Ticker:", style={'font-size': '20px'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': 'orange'}),

            # Dropdown for duration
            html.Label("Select Duration:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': 'orange'}
            ),

            # Graph to display MACD chart
            dcc.Graph(id='macd-chart', style={'height': '600px'}),
        ]
    )

    # Callback to update the chart based on user inputs
    @app.callback(
        Output('macd-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = fetch_stock_data(ticker, period)

        # Generate the MACD chart
        fig = create_macd_chart(data)
        return fig

    # Run the Dash app
    app.run_server(debug=True)

# Call the function to launch the app
#macd_dashboard()


#Creating a function which gives out the dashboard for the Relative Strength Index (RSI) and has the options for duration and input stock

def rsi_graph():
    app = dash.Dash(__name__)

    # Function to fetch stock data using yfinance
    def fetch_stock_data(ticker, period='1y'):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data

    # Function to calculate RSI
    def calculate_rsi(data, period=14):
        delta = data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Function to generate RSI chart using plotly
    def create_rsi_chart(data):
        rsi = calculate_rsi(data)
        fig = go.Figure()

        # RSI line trace
        fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name='RSI'))

        # Dark theme settings
        fig.update_layout(
            template="plotly_dark",
            title="Relative Strength Index (RSI)",
            xaxis_title="Date",
            yaxis_title="RSI",
            font=dict(color="white"),
            plot_bgcolor="black",
            paper_bgcolor="black",
            hovermode="x",
        )

        # Add upper and lower bound lines
        fig.add_shape(
            type="line", x0=data.index[0], x1=data.index[-1], y0=70, y1=70,
            line=dict(color="red", dash="dash"), name='Overbought'
        )
        fig.add_shape(
            type="line", x0=data.index[0], x1=data.index[-1], y0=30, y1=30,
            line=dict(color="green", dash="dash"), name='Oversold'
        )
        return fig

    # Layout for the Dash app
    app.layout = html.Div(
        style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'},
        children=[
            html.H1("RSI Dashboard", style={'textAlign': 'center'}),

            # Input for ticker symbol
            html.Label("Enter Stock Ticker:", style={'font-size': '20px'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': 'orange'}),

            # Dropdown for duration
            html.Label("Select Duration:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': 'orange'}
            ),

            # Graph to display RSI chart
            dcc.Graph(id='rsi-chart', style={'height': '600px'}),
        ]
    )

    # Callback to update the chart based on user inputs
    @app.callback(
        Output('rsi-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = fetch_stock_data(ticker, period)

        # Generate the RSI chart
        fig = create_rsi_chart(data)
        return fig

    # Run the Dash app
    app.run_server(debug=True)

# Call the function to launch the app
#rsi_graph()



#Creating a function to create Bolinger Bands as per the stock and time range entered 

def bolinger_bands():
    app = dash.Dash(__name__)

    # Function to fetch stock data using yfinance
    def fetch_stock_data(ticker, period='1y'):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data

    # Function to calculate Bollinger Bands
    def calculate_bollinger_bands(data, window=20, num_std=2):
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return rolling_mean, upper_band, lower_band

    # Function to generate Bollinger Bands chart using plotly
    def create_bollinger_chart(data):
        rolling_mean, upper_band, lower_band = calculate_bollinger_bands(data)
        fig = go.Figure()

        # Closing price trace
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='orange')))

        # Middle band (Moving Average) trace
        fig.add_trace(go.Scatter(x=data.index, y=rolling_mean, mode='lines', name='Middle Band (SMA)', line=dict(color='blue')))

        # Upper band trace
        fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band', line=dict(color='green')))

        # Lower band trace
        fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band', line=dict(color='red')))

        # Dark theme settings
        fig.update_layout(
            template="plotly_dark",
            title="Bollinger Bands",
            xaxis_title="Date",
            yaxis_title="Price",
            font=dict(color="white"),
            plot_bgcolor="black",
            paper_bgcolor="black",
            hovermode="x",
        )
        return fig

    # Layout for the Dash app
    app.layout = html.Div(
        style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'},
        children=[
            html.H1("Bollinger Bands Dashboard", style={'textAlign': 'center'}),

            # Input for ticker symbol
            html.Label("Enter Stock Ticker:", style={'font-size': '20px'}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': 'orange'}),

            # Dropdown for duration
            html.Label("Select Duration:", style={'font-size': '20px', 'color': 'orange'}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': 'orange'}
            ),

            # Graph to display Bollinger Bands chart
            dcc.Graph(id='bollinger-chart', style={'height': '600px'}),
        ]
    )

    # Callback to update the chart based on user inputs
    @app.callback(
        Output('bollinger-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = fetch_stock_data(ticker, period)

        # Generate the Bollinger Bands chart
        fig = create_bollinger_chart(data)
        return fig

    # Run the Dash app
    app.run_server(debug=True)

# Call the function to launch the app
#bolinger_bands()




#Creating a function which will show the Simple Moving Averages (SMA) for multiple periods using dash and yfinance


def create_sma_dashboard():
    # Initialize the Dash app with a dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    # Define colors inspired by Bloomberg Terminal
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'sma_50': '#1f77b4',   # blue
        'sma_100': '#ff7f0e',  # orange
        'sma_200': '#2ca02c'   # green
    }
    
    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Simple Moving Averages (SMA) Dashboard", style={'textAlign': 'center', 'color': colors['text']}),
            
            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='sma-chart', style={'height': '600px'}),
        ]
    )

    # Define callback to update the chart
    @app.callback(
        Output('sma-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)
        
        # Calculate SMAs
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_100'] = data['Close'].rolling(window=100).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        
        # Create the figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], mode='lines', name='50-Day SMA', line=dict(color=colors['sma_50'])))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_100'], mode='lines', name='100-Day SMA', line=dict(color=colors['sma_100'])))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], mode='lines', name='200-Day SMA', line=dict(color=colors['sma_200'])))
        
        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Simple Moving Averages",
            xaxis_title="Date",
            yaxis_title="Price",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x",
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#create_sma_dashboard()




#Creating a function which takes displays the dashboard for the exponential moving averages (EMA) for multiple periods using dash and yfinance


def create_ema_dashboard():
    # Initialize the Dash app with a dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    # Define colors inspired by Bloomberg Terminal
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'ema_20': '#1f77b4',   # blue
        'ema_50': '#ff7f0e',   # orange
        'ema_100': '#2ca02c'   # green
    }
    
    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Exponential Moving Averages (EMA) Dashboard", style={'textAlign': 'center', 'color': colors['text']}),
            
            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='ema-chart', style={'height': '600px'}),
        ]
    )

    # Define callback to update the chart
    @app.callback(
        Output('ema-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)
        
        # Calculate EMAs
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
        data['EMA_100'] = data['Close'].ewm(span=100, adjust=False).mean()
        
        # Create the figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], mode='lines', name='20-Day EMA', line=dict(color=colors['ema_20'])))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_50'], mode='lines', name='50-Day EMA', line=dict(color=colors['ema_50'])))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_100'], mode='lines', name='100-Day EMA', line=dict(color=colors['ema_100'])))
        
        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Exponential Moving Averages",
            xaxis_title="Date",
            yaxis_title="Price",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x",
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#create_ema_dashboard()



#Creating a function which displays a dashboard for Stochastic Oscillator using dash and yfinance


def create_stochastic_dashboard():
    # Initialize the Dash app with a dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    # Define colors inspired by Bloomberg Terminal
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'k_line': '#1f77b4',   # blue
        'd_line': '#ff7f0e',   # orange
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Stochastic Oscillator Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='stochastic-chart', style={'height': '600px'}),
        ]
    )

    # Define callback to update the chart
    @app.callback(
        Output('stochastic-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Calculate the Stochastic Oscillator
        high_14 = data['High'].rolling(window=14).max()
        low_14 = data['Low'].rolling(window=14).min()
        data['%K'] = 100 * ((data['Close'] - low_14) / (high_14 - low_14))
        data['%D'] = data['%K'].rolling(window=3).mean()

        # Create the figure
        fig = go.Figure()
        
        # Plot %K line
        fig.add_trace(go.Scatter(x=data.index, y=data['%K'], mode='lines', name='%K Line (14-day)', line=dict(color=colors['k_line'])))
        
        # Plot %D line (3-day moving average of %K)
        fig.add_trace(go.Scatter(x=data.index, y=data['%D'], mode='lines', name='%D Line (3-day MA)', line=dict(color=colors['d_line'])))
        
        # Add 20 and 80 reference lines for overbought/oversold levels
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="top right")
        fig.add_hline(y=20, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom right")

        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Stochastic Oscillator",
            xaxis_title="Date",
            yaxis_title="Stochastic Oscillator (%)",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x",
            yaxis=dict(range=[0, 100])
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#create_stochastic_dashboard()




#Creating a function which displays a dashboard for the On Balance Volume (OBV) using dash and yfinance


def create_obv_dashboard():
    # Initialize the Dash app with a dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    # Define colors inspired by Bloomberg Terminal
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'obv_line': '#1f77b4',   # blue
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("On-Balance Volume (OBV) Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='obv-chart', style={'height': '600px'}),
        ]
    )

    # Define callback to update the chart
    @app.callback(
        Output('obv-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Calculate On-Balance Volume (OBV)
        obv = [0]  # Start with the first OBV value at 0
        for i in range(1, len(data)):
            if data['Close'][i] > data['Close'][i - 1]:
                obv.append(obv[-1] + data['Volume'][i])
            elif data['Close'][i] < data['Close'][i - 1]:
                obv.append(obv[-1] - data['Volume'][i])
            else:
                obv.append(obv[-1])
        data['OBV'] = obv

        # Create the figure
        fig = go.Figure()

        # Plot OBV line
        fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], mode='lines', name='OBV', line=dict(color=colors['obv_line'])))
        
        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - On-Balance Volume (OBV)",
            xaxis_title="Date",
            yaxis_title="On-Balance Volume",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#create_obv_dashboard()







#Creating  a function for Average True Value (ATR) using dash and yfinance


def calculate_atr(data, period=14):
    """Calculate the Average True Range (ATR)"""
    high = data['High']
    low = data['Low']
    close = data['Close']

    # Calculate the True Range (TR)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1)
    tr = tr.max(axis=1)  # Maximum of the three True Range calculations

    # Calculate ATR
    atr = tr.rolling(window=period).mean()
    return atr

def create_atr_dashboard():
    # Initialize the Dash app with a dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors inspired by Bloomberg Terminal
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'atr_line': '#FF6347',  # Tomato color for ATR line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Average True Range (ATR) Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='atr-chart', style={'height': '600px'}),
        ]
    )

    # Define callback to update the chart
    @app.callback(
        Output('atr-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Calculate ATR
        atr = calculate_atr(data)

        # Create the figure
        fig = go.Figure()

        # Plot ATR line
        fig.add_trace(go.Scatter(x=data.index, y=atr, mode='lines', name='ATR', line=dict(color=colors['atr_line'])))
        
        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Average True Range (ATR)",
            xaxis_title="Date",
            yaxis_title="ATR",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#create_atr_dashboard()



#Creating a function which returns the Fibonnaci Retracements on the selected stock and time range 


def fibonacci_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'fib_lines': '#FF6347',  # Tomato color for Fibonacci lines
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Fibonacci Retracement Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='fibonacci-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('fibonacci-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Calculate Fibonacci retracement levels
        high_price = data['High'].max()
        low_price = data['Low'].min()
        diff = high_price - low_price
        levels = {
            '0%': high_price,
            '23.6%': high_price - 0.236 * diff,
            '38.2%': high_price - 0.382 * diff,
            '50%': high_price - 0.5 * diff,
            '61.8%': high_price - 0.618 * diff,
            '100%': low_price,
        }

        # Create the figure
        fig = go.Figure()

        # Add the stock's closing price line
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='cyan')))

        # Plot Fibonacci retracement levels as horizontal lines
        for level_name, level_value in levels.items():
            fig.add_hline(y=level_value, line_dash="dash", line_color=colors['fib_lines'], annotation_text=level_name, annotation_position="top right")

        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Fibonacci Retracement Levels",
            xaxis_title="Date",
            yaxis_title="Price",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#fibonacci_dashboard()





#Creating a function which takes the ticker as input and returns the Price to Earnings Ration Over time 


def pe_ratio_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'pe_line': '#FF6347',  # Tomato color for P/E ratio line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Price-to-Earnings (P/E) Ratio Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='pe-ratio-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('pe-ratio-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Get the trailing twelve-month (TTM) EPS for P/E calculation
        stock = yf.Ticker(ticker)
        ttm_eps = stock.info.get('trailingEps')

        if ttm_eps:
            # Calculate the P/E ratio by dividing close price by TTM EPS
            data['P/E Ratio'] = data['Close'] / ttm_eps
        else:
            # If no EPS data, P/E ratio cannot be calculated
            data['P/E Ratio'] = None

        # Create the figure
        fig = go.Figure()

        # Add the P/E ratio line
        fig.add_trace(go.Scatter(x=data.index, y=data['P/E Ratio'], mode='lines', name='P/E Ratio', line=dict(color=colors['pe_line'])))

        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Price-to-Earnings (P/E) Ratio Over Time",
            xaxis_title="Date",
            yaxis_title="P/E Ratio",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#pe_ratio_dashboard()




#Creating a function which takes the ticker as input and returns the Price to Book Ration Over Time.


def pb_ratio_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'pb_line': '#1E90FF',  # DodgerBlue color for P/B ratio line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Price-to-Book (P/B) Ratio Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='pb-ratio-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('pb-ratio-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Get the book value per share (BVPS) for P/B calculation
        stock = yf.Ticker(ticker)
        bvps = stock.info.get('bookValue')

        if bvps:
            # Calculate the P/B ratio by dividing close price by BVPS
            data['P/B Ratio'] = data['Close'] / bvps
        else:
            # If no BVPS data, P/B ratio cannot be calculated
            data['P/B Ratio'] = None

        # Create the figure
        fig = go.Figure()

        # Add the P/B ratio line
        fig.add_trace(go.Scatter(x=data.index, y=data['P/B Ratio'], mode='lines', name='P/B Ratio', line=dict(color=colors['pb_line'])))

        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Price-to-Book (P/B) Ratio Over Time",
            xaxis_title="Date",
            yaxis_title="P/B Ratio",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#pb_ratio_dashboard()



#Creating a function which takes the ticker and gives out the Dividend Yield Over Time.

def dividend_yield_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'dividend_line': '#FFD700',  # Gold color for dividend yield line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Dividend Yield Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='dividend-yield-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('dividend-yield-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch the stock data
        data = yf.download(ticker, period=period)

        # Fetch dividend yield data
        stock = yf.Ticker(ticker)
        annual_dividend = stock.info.get('dividendRate', 0)

        if annual_dividend and not data.empty:
            # Calculate dividend yield as a percentage
            data['Dividend Yield (%)'] = (annual_dividend / data['Close']) * 100
        else:
            data['Dividend Yield (%)'] = None

        # Create the figure
        fig = go.Figure()

        # Add the Dividend Yield line
        fig.add_trace(go.Scatter(x=data.index, y=data['Dividend Yield (%)'], mode='lines', name='Dividend Yield', line=dict(color=colors['dividend_line'])))

        # Update layout with dark theme
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Dividend Yield Over Time",
            xaxis_title="Date",
            yaxis_title="Dividend Yield (%)",
            font=dict(color="white"),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            hovermode="x"
        )
        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#dividend_yield_dashboard()


#Creating a fucntion which shows the graph for the revenue growth of the stock.

def revenue_growth_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'revenue_line': '#FFA500',  # Orange color for Revenue Growth line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Revenue Growth Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='revenue-growth-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('revenue-growth-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch financial data
        stock = yf.Ticker(ticker)
        financials = stock.financials

        if financials is not None:
            # Calculate revenue growth (year-over-year)
            financials = financials.transpose()
            financials['Revenue Growth'] = financials['Total Revenue'].pct_change() * 100  # Convert to percentage

            # Filter data for the selected duration
            financials = financials.tail(int(period.replace('y', '')))

            # Create the figure
            fig = go.Figure()

            # Add the Revenue Growth line
            fig.add_trace(go.Scatter(x=financials.index, y=financials['Revenue Growth'], mode='lines+markers',
                                     name='Revenue Growth (%)', line=dict(color=colors['revenue_line'])))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Revenue Growth Over Time",
                xaxis_title="Date",
                yaxis_title="Revenue Growth (%)",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if financial data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Revenue data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#revenue_growth_dashboard()



#Creating a function which takes ticker and displays the Profit Margin Trend.

def profit_margin_trend_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'margin_line': '#32CD32',  # LimeGreen color for Profit Margin line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Profit Margin Trend Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='profit-margin-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('profit-margin-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch financial data
        stock = yf.Ticker(ticker)
        financials = stock.financials

        if financials is not None:
            # Calculate profit margin (Net Income / Total Revenue) * 100 for percentage
            financials = financials.transpose()
            financials['Profit Margin'] = (financials['Net Income'] / financials['Total Revenue']) * 100

            # Filter data for the selected duration
            financials = financials.tail(int(period.replace('y', '')))

            # Create the figure
            fig = go.Figure()

            # Add the Profit Margin line
            fig.add_trace(go.Scatter(x=financials.index, y=financials['Profit Margin'], mode='lines+markers',
                                     name='Profit Margin (%)', line=dict(color=colors['margin_line'])))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Profit Margin Trend Over Time",
                xaxis_title="Date",
                yaxis_title="Profit Margin (%)",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if financial data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Profit margin data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#profit_margin_trend_dashboard()



#Creating a function which displays the Free Cash Flow trend for the typed ticker.

def free_cash_flow_trend_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'fcf_line': '#1E90FF',  # DodgerBlue color for Free Cash Flow line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Free Cash Flow Trend Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='fcf-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('fcf-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch cash flow data
        stock = yf.Ticker(ticker)
        cash_flow = stock.cashflow

        if cash_flow is not None:
            # Transpose to have dates as rows
            cash_flow = cash_flow.transpose()

            # Check if 'Free Cash Flow' column is available
            if 'Free Cash Flow' in cash_flow.columns:
                # Filter data for the selected duration
                cash_flow = cash_flow.tail(int(period.replace('y', '')))

                # Create the figure
                fig = go.Figure()

                # Add the Free Cash Flow line
                fig.add_trace(go.Scatter(x=cash_flow.index, y=cash_flow['Free Cash Flow'], mode='lines+markers',
                                         name='Free Cash Flow', line=dict(color=colors['fcf_line'])))

                # Update layout with dark theme
                fig.update_layout(
                    template="plotly_dark",
                    title=f"{ticker} - Free Cash Flow Trend Over Time",
                    xaxis_title="Date",
                    yaxis_title="Free Cash Flow (USD)",
                    font=dict(color="white"),
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    hovermode="x"
                )
            else:
                # Display a message if the column is unavailable
                fig = go.Figure()
                fig.add_annotation(
                    text="Free Cash Flow data not available for this stock",
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=20, color=colors['text'])
                )
                fig.update_layout(
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background']
                )
        else:
            # Display a message if cash flow data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Cash flow data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#free_cash_flow_trend_dashboard()




#Creating a function which displays the Beta coefficient over time


def beta_trend_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'beta_line': '#FF4500',  # OrangeRed color for Beta line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Beta Coefficient Trend Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                    {'label': '10 Years', 'value': '10y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='beta-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('beta-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        if not ticker:
            fig = go.Figure()
            fig.add_annotation(
                text="Please enter a valid stock ticker symbol",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )
            return fig

        # Fetch stock data
        try:
            stock = yf.Ticker(ticker)
            beta = stock.info.get('beta')
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text="Failed to retrieve data. Please check the stock ticker symbol.",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )
            return fig

        if beta is not None:
            # Simulate Beta trend as a constant line
            date_range = pd.date_range(end=pd.Timestamp.today(), periods=int(period.replace('y', '')) * 12, freq='ME')

            # Create the figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=date_range, y=[beta] * len(date_range), mode='lines',
                                     name='Beta Coefficient', line=dict(color=colors['beta_line'])))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Beta Coefficient Trend Over Time",
                xaxis_title="Date",
                yaxis_title="Beta Coefficient",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if Beta data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Beta coefficient data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#beta_trend_dashboard()



#Creating a function for displaying Correlation with market index

def correlation_with_market_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'correlation_line': '#FF6347',  # Tomato color for correlation line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Stock and Market Index Correlation Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='correlation-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('correlation-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Define the market index ticker (S&P 500 in this example)
        market_index_ticker = '^GSPC'  # S&P 500

        # Fetch historical data for the stock and the market index
        stock_data = yf.download(ticker, period=period, interval='1mo')
        market_index_data = yf.download(market_index_ticker, period=period, interval='1mo')

        # Ensure we have data for both the stock and the index
        if not stock_data.empty and not market_index_data.empty:
            # Calculate the monthly returns
            stock_returns = stock_data['Adj Close'].pct_change().dropna()
            market_index_returns = market_index_data['Adj Close'].pct_change().dropna()

            # Align data by index (date)
            returns_df = pd.DataFrame({
                'Stock': stock_returns,
                'Market Index': market_index_returns
            }).dropna()

            # Calculate the rolling correlation (using a 6-month window)
            returns_df['Correlation'] = returns_df['Stock'].rolling(window=6).corr(returns_df['Market Index'])

            # Create the figure
            fig = go.Figure()

            # Add the Correlation line
            fig.add_trace(go.Scatter(x=returns_df.index, y=returns_df['Correlation'], mode='lines+markers',
                                     name='Rolling Correlation', line=dict(color=colors['correlation_line'])))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Rolling Correlation with {market_index_ticker} Over Time",
                xaxis_title="Date",
                yaxis_title="Correlation",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#correlation_with_market_dashboard()



#Creating a function which returns the - Volatility standard deviation of the stock.


def volatility_trend_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'volatility_line': '#FFA500',  # Orange color for volatility line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Stock Volatility Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='volatility-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('volatility-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch historical data for the stock
        stock_data = yf.download(ticker, period=period, interval='1d')

        if not stock_data.empty:
            # Calculate daily returns
            stock_returns = stock_data['Adj Close'].pct_change().dropna()

            # Calculate rolling volatility (standard deviation) with a 20-day window (approximately 1 month)
            rolling_volatility = stock_returns.rolling(window=20).std() * (252**0.5)  # Annualize the volatility

            # Create the figure
            fig = go.Figure()

            # Add the Volatility line
            fig.add_trace(go.Scatter(x=rolling_volatility.index, y=rolling_volatility, mode='lines',
                                     name='Rolling Volatility (Annualized)', line=dict(color=colors['volatility_line'])))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Rolling Volatility Over Time",
                xaxis_title="Date",
                yaxis_title="Volatility (Standard Deviation)",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#volatility_trend_dashboard()




#Creating a function which will show the sharpe_ratio_trend_dashboard


def sharpe_ratio_trend_dashboard():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'sharpe_ratio_line': '#00FF00',  # Green color for Sharpe Ratio line
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Stock Sharpe Ratio Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '2 Years', 'value': '2y'},
                    {'label': '5 Years', 'value': '5y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='sharpe-ratio-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('sharpe-ratio-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        # Fetch historical data for the stock
        stock_data = yf.download(ticker, period=period, interval='1d')

        if not stock_data.empty:
            # Calculate daily returns
            stock_returns = stock_data['Adj Close'].pct_change().dropna()

            # Assume a risk-free rate of 0% for simplicity
            risk_free_rate = 0

            # Calculate rolling average return and rolling volatility (standard deviation) with a 20-day window
            rolling_avg_return = stock_returns.rolling(window=20).mean()
            rolling_volatility = stock_returns.rolling(window=20).std()

            # Calculate rolling Sharpe Ratio
            rolling_sharpe_ratio = (rolling_avg_return - risk_free_rate) / rolling_volatility

            # Create the figure
            fig = go.Figure()

            # Add the Sharpe Ratio line
            fig.add_trace(go.Scatter(
                x=rolling_sharpe_ratio.index,
                y=rolling_sharpe_ratio,
                mode='lines',
                name='Rolling Sharpe Ratio',
                line=dict(color=colors['sharpe_ratio_line'])
            ))

            # Update layout with dark theme
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker} - Rolling Sharpe Ratio Over Time",
                xaxis_title="Date",
                yaxis_title="Sharpe Ratio",
                font=dict(color="white"),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                hovermode="x"
            )
        else:
            # Display a message if data is unavailable
            fig = go.Figure()
            fig.add_annotation(
                text="Data not available",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

# Call the function to launch the app
#sharpe_ratio_trend_dashboard()



def trading_volume_price_dashboard():
  
   
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'price_line': '#00FF00',  # Green for Price line
        'volume_bar': '#007BFF',  # Blue for Volume bars
    }

    # Define the layout of the dashboard
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Trading Volume vs. Price Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Label("Enter Stock Ticker:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Input(id='ticker-input', type='text', value='AAPL', style={'font-size': '20px', 'color': colors['text']}),

            html.Label("Select Duration:", style={'font-size': '20px', 'color': colors['text']}),
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '5 Years', 'value': '5y'},
                ],
                value='1y',
                style={'font-size': '20px', 'color': colors['text']}
            ),

            dcc.Graph(id='volume-price-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('volume-price-chart', 'figure'),
        Input('ticker-input', 'value'),
        Input('duration-dropdown', 'value')
    )
    def update_chart(ticker, period):
        try:
            # Fetch historical data for the stock
            stock_data = yf.download(ticker, period=period, interval='1d')

            if not stock_data.empty:
                # Create the figure
                fig = go.Figure()

                # Add the price line (Adjusted Close)
                fig.add_trace(go.Scatter(
                    x=stock_data.index,
                    y=stock_data['Adj Close'],
                    mode='lines',
                    name='Price',
                    line=dict(color=colors['price_line'], width=2),
                    yaxis='y1'  # Use the left y-axis
                ))

                # Add the volume bar chart
                fig.add_trace(go.Bar(
                    x=stock_data.index,
                    y=stock_data['Volume'],
                    name='Volume',
                    marker=dict(color=colors['volume_bar']),
                    yaxis='y2'  # Use the right y-axis
                ))

                # Update layout
                fig.update_layout(
                    template="plotly_dark",
                    title=f"{ticker} - Trading Volume vs. Price",
                    xaxis_title="Date",
                    yaxis=dict(
                        title="Price",
                        titlefont=dict(color=colors['price_line']),
                        tickfont=dict(color=colors['price_line'])
                    ),
                    yaxis2=dict(
                        title="Volume",
                        titlefont=dict(color=colors['volume_bar']),
                        tickfont=dict(color=colors['volume_bar']),
                        overlaying='y',
                        side='right'
                    ),
                    font=dict(color="white"),
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    legend=dict(x=0, y=1, xanchor='left', yanchor='top')
                )
            else:
                # Handle empty data case
                fig = go.Figure()
                fig.add_annotation(
                    text="Data not available",
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=20, color=colors['text'])
                )
                fig.update_layout(
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background']
                )

        except Exception as e:
            # Handle errors (e.g., invalid ticker, API issues)
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
    
#Example Use Case 
#trading_volume_price_dashboard()




#[Creating the function for the comparative graphs]

#Creating a function to create comparative graphs 


def multi_ticker_dashboard():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'line1': '#FF4500',  # Line for Ticker 1
        'line2': '#1E90FF',  # Line for Ticker 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Multi-Ticker Value Comparison Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Value Type:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='value-type-dropdown',
                    options=[
                        {'label': 'Open', 'value': 'Open'},
                        {'label': 'Close', 'value': 'Close'},
                        {'label': 'High', 'value': 'High'},
                        {'label': 'Low', 'value': 'Low'},
                        {'label': 'Average', 'value': 'Average'},
                    ],
                    value='Close',
                    style={'margin-bottom': '20px'}
                ),
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                )
            ]),

            dcc.Graph(id='comparison-chart', style={'height': '600px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('value-type-dropdown', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, value_type, period):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate average if selected
            if value_type == 'Average':
                data1['Average'] = (data1['High'] + data1['Low']) / 2
                data2['Average'] = (data2['High'] + data2['Low']) / 2

            # Create the figure
            fig = go.Figure()

            # Add line for Ticker 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1[value_type],
                    mode='lines',
                    name=f'{ticker1} {value_type}',
                    line=dict(color=colors['line1'], width=2),
                ))
            else:
                fig.add_annotation(
                    text=f"Data not available for {ticker1}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.8, showarrow=False,
                    font=dict(size=18, color=colors['text'])
                )

            # Add line for Ticker 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2[value_type],
                    mode='lines',
                    name=f'{ticker2} {value_type}',
                    line=dict(color=colors['line2'], width=2),
                ))
            else:
                fig.add_annotation(
                    text=f"Data not available for {ticker2}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.6, showarrow=False,
                    font=dict(size=18, color=colors['text'])
                )

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - {value_type} Comparison",
                xaxis_title="Date",
                yaxis_title=value_type,
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
    
#Example Usecase 
#multi_ticker_dashboard()



#Creating a function for showing comparative graphs for price moving averages 

def price_moving_average_dashboard():
    

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'price1': '#FF4500',  # Price line for Ticker 1
        'price2': '#1E90FF',  # Price line for Ticker 2
        'sma_ema1': '#FFD700',  # SMA/EMA line for Ticker 1
        'sma_ema2': '#32CD32',  # SMA/EMA line for Ticker 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Price vs. Moving Average (SMA/EMA) Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Moving Average Type:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='ma-type-dropdown',
                    options=[
                        {'label': 'Simple Moving Average (SMA)', 'value': 'SMA'},
                        {'label': 'Exponential Moving Average (EMA)', 'value': 'EMA'},
                    ],
                    value='SMA',
                    style={'margin-bottom': '20px'}
                ),
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                ),
                html.Label("Moving Average Window (Days):", style={'color': colors['text']}),
                dcc.Input(id='ma-window-input', type='number', value=20, style={'margin-top': '10px'}),
            ]),

            dcc.Graph(id='ma-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('ma-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('ma-type-dropdown', 'value'),
            Input('duration-dropdown', 'value'),
            Input('ma-window-input', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, ma_type, period, window):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate moving averages
            if not data1.empty:
                if ma_type == 'SMA':
                    data1['MA'] = data1['Adj Close'].rolling(window=window).mean()
                elif ma_type == 'EMA':
                    data1['MA'] = data1['Adj Close'].ewm(span=window, adjust=False).mean()

            if not data2.empty:
                if ma_type == 'SMA':
                    data2['MA'] = data2['Adj Close'].rolling(window=window).mean()
                elif ma_type == 'EMA':
                    data2['MA'] = data2['Adj Close'].ewm(span=window, adjust=False).mean()

            # Create the figure
            fig = go.Figure()

            # Add price and moving average for Ticker 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Adj Close'],
                    mode='lines',
                    name=f'{ticker1} Price',
                    line=dict(color=colors['price1'], width=2),
                ))
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['MA'],
                    mode='lines',
                    name=f'{ticker1} {ma_type}',
                    line=dict(color=colors['sma_ema1'], dash='dash', width=2),
                ))

            # Add price and moving average for Ticker 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Adj Close'],
                    mode='lines',
                    name=f'{ticker2} Price',
                    line=dict(color=colors['price2'], width=2),
                ))
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['MA'],
                    mode='lines',
                    name=f'{ticker2} {ma_type}',
                    line=dict(color=colors['sma_ema2'], dash='dash', width=2),
                ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - Price and {ma_type} Comparison",
                xaxis_title="Date",
                yaxis_title="Price",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)


#Example Usecase 
#price_moving_average_dashboard()




#Function to create RSI comparison dashboard

def rsi_comparison_dashboard():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'line1': '#FF4500',  # RSI for Ticker 1
        'line2': '#1E90FF',  # RSI for Ticker 2
        'overbought': '#FF6347',  # Overbought threshold line
        'oversold': '#32CD32',  # Oversold threshold line
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Relative Strength Index (RSI) Comparison Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
                html.Label("RSI Window (Days):", style={'color': colors['text']}),
                dcc.Input(id='rsi-window-input', type='number', value=14, style={'margin-top': '10px'}),
            ]),

            dcc.Graph(id='rsi-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the RSI calculation function
    def calculate_rsi(data, window):
        """Calculate the Relative Strength Index (RSI)."""
        delta = data['Adj Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Define the callback to update the chart
    @app.callback(
        Output('rsi-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('duration-dropdown', 'value'),
            Input('rsi-window-input', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, period, window):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate RSI
            data1['RSI'] = calculate_rsi(data1, window) if not data1.empty else pd.Series(dtype='float64')
            data2['RSI'] = calculate_rsi(data2, window) if not data2.empty else pd.Series(dtype='float64')

            # Create the figure with subplots for side-by-side RSI comparison
            fig = go.Figure()

            # Add RSI chart for Ticker 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['RSI'],
                    mode='lines',
                    name=f'{ticker1} RSI',
                    line=dict(color=colors['line1'], width=2),
                ))

            # Add RSI chart for Ticker 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['RSI'],
                    mode='lines',
                    name=f'{ticker2} RSI',
                    line=dict(color=colors['line2'], width=2),
                ))

            # Add overbought and oversold threshold lines
            fig.add_hline(y=70, line=dict(color=colors['overbought'], dash='dash'), annotation_text="Overbought", annotation_position="bottom right")
            fig.add_hline(y=30, line=dict(color=colors['oversold'], dash='dash'), annotation_text="Oversold", annotation_position="top right")

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - RSI Comparison",
                xaxis_title="Date",
                yaxis_title="RSI",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
    

#Example Usecase 
#rsi_comparison_dashboard()



#Creating a function to create Bollinger Bands comparison dashboard

def bollinger_bands_comparison_dashboard():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'stock1': '#FF4500',  # Stock 1 Bollinger Bands
        'stock2': '#1E90FF',  # Stock 2 Bollinger Bands
        'band_fill': 'rgba(255, 69, 0, 0.2)',  # Semi-transparent fill for Stock 1 bands
        'band_fill2': 'rgba(30, 144, 255, 0.2)'  # Semi-transparent fill for Stock 2 bands
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Bollinger Bands Comparison Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
                html.Label("Bollinger Bands Window (Days):", style={'color': colors['text']}),
                dcc.Input(id='bollinger-window-input', type='number', value=20, style={'margin-top': '10px'}),
            ]),

            dcc.Graph(id='bollinger-bands-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the Bollinger Bands calculation function
    def calculate_bollinger_bands(data, window):
        """Calculate Bollinger Bands."""
        sma = data['Adj Close'].rolling(window=window).mean()  # Simple Moving Average
        std = data['Adj Close'].rolling(window=window).std()   # Standard Deviation
        upper_band = sma + (2 * std)  # Upper Band
        lower_band = sma - (2 * std)  # Lower Band
        return sma, upper_band, lower_band

    # Define the callback to update the chart
    @app.callback(
        Output('bollinger-bands-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('duration-dropdown', 'value'),
            Input('bollinger-window-input', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, period, window):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate Bollinger Bands
            if not data1.empty:
                data1['SMA'], data1['Upper Band'], data1['Lower Band'] = calculate_bollinger_bands(data1, window)
            if not data2.empty:
                data2['SMA'], data2['Upper Band'], data2['Lower Band'] = calculate_bollinger_bands(data2, window)

            # Create the figure with subplots for side-by-side comparison
            fig = go.Figure()

            # Add Bollinger Bands for Ticker 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Upper Band'],
                    mode='lines',
                    name=f'{ticker1} Upper Band',
                    line=dict(color=colors['stock1'], dash='dot')
                ))
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Lower Band'],
                    mode='lines',
                    name=f'{ticker1} Lower Band',
                    line=dict(color=colors['stock1'], dash='dot')
                ))
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Adj Close'],
                    mode='lines',
                    name=f'{ticker1} Price',
                    line=dict(color=colors['stock1'])
                ))

            # Add Bollinger Bands for Ticker 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Upper Band'],
                    mode='lines',
                    name=f'{ticker2} Upper Band',
                    line=dict(color=colors['stock2'], dash='dot')
                ))
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Lower Band'],
                    mode='lines',
                    name=f'{ticker2} Lower Band',
                    line=dict(color=colors['stock2'], dash='dot')
                ))
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Adj Close'],
                    mode='lines',
                    name=f'{ticker2} Price',
                    line=dict(color=colors['stock2'])
                ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - Bollinger Bands Comparison",
                xaxis_title="Date",
                yaxis_title="Price",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)


#Example Usecase 
#bollinger_bands_comparison_dashboard()




#Creating a function for macd_comparison dashboard using 2 ticker values 
def macd_comparison_dashboard():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'macd1': '#FF4500',  # Stock 1 MACD line
        'signal1': '#FFA07A',  # Stock 1 Signal line
        'hist1': '#FF6347',  # Stock 1 Histogram
        'macd2': '#1E90FF',  # Stock 2 MACD line
        'signal2': '#87CEEB',  # Stock 2 Signal line
        'hist2': '#4682B4',  # Stock 2 Histogram
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("MACD Comparison Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
                html.Label("MACD Short Window (Fast):", style={'color': colors['text']}),
                dcc.Input(id='macd-fast-window', type='number', value=12, style={'margin-right': '20px'}),
                html.Label("MACD Long Window (Slow):", style={'color': colors['text']}),
                dcc.Input(id='macd-slow-window', type='number', value=26, style={'margin-right': '20px'}),
                html.Label("Signal Line Window:", style={'color': colors['text']}),
                dcc.Input(id='signal-line-window', type='number', value=9),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='macd-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the MACD calculation function
    def calculate_macd(data, fast, slow, signal):
        """Calculate MACD, Signal Line, and Histogram."""
        ema_fast = data['Adj Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = data['Adj Close'].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    # Define the callback to update the chart
    @app.callback(
        Output('macd-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('duration-dropdown', 'value'),
            Input('macd-fast-window', 'value'),
            Input('macd-slow-window', 'value'),
            Input('signal-line-window', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, period, fast, slow, signal):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate MACD for both stocks
            if not data1.empty:
                data1['MACD'], data1['Signal'], data1['Histogram'] = calculate_macd(data1, fast, slow, signal)
            if not data2.empty:
                data2['MACD'], data2['Signal'], data2['Histogram'] = calculate_macd(data2, fast, slow, signal)

            # Create the figure
            fig = go.Figure()

            # Add MACD for Ticker 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['MACD'],
                    mode='lines',
                    name=f'{ticker1} MACD Line',
                    line=dict(color=colors['macd1'])
                ))
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Signal'],
                    mode='lines',
                    name=f'{ticker1} Signal Line',
                    line=dict(color=colors['signal1'])
                ))
                fig.add_trace(go.Bar(
                    x=data1.index,
                    y=data1['Histogram'],
                    name=f'{ticker1} Histogram',
                    marker=dict(color=colors['hist1']),
                    opacity=0.5
                ))

            # Add MACD for Ticker 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['MACD'],
                    mode='lines',
                    name=f'{ticker2} MACD Line',
                    line=dict(color=colors['macd2'])
                ))
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Signal'],
                    mode='lines',
                    name=f'{ticker2} Signal Line',
                    line=dict(color=colors['signal2'])
                ))
                fig.add_trace(go.Bar(
                    x=data2.index,
                    y=data2['Histogram'],
                    name=f'{ticker2} Histogram',
                    marker=dict(color=colors['hist2']),
                    opacity=0.5
                ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - MACD Comparison",
                xaxis_title="Date",
                yaxis_title="Value",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
    
#Example Usecase 
#macd_comparison_dashboard()



#Creating a function which generates the comparative return chart

def comparative_return_chart():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'stock1': '#FF6347',  # Stock 1
        'stock2': '#1E90FF',  # Stock 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Comparative Return Chart", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '1 Month', 'value': '1mo'},
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='return-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('return-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, period):
        try:
            # Fetch historical data for both tickers
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate cumulative returns
            data1['Daily Return'] = data1['Adj Close'].pct_change()
            data2['Daily Return'] = data2['Adj Close'].pct_change()

            data1['Cumulative Return'] = (1 + data1['Daily Return']).cumprod() - 1
            data2['Cumulative Return'] = (1 + data2['Daily Return']).cumprod() - 1

            # Create the figure
            fig = go.Figure()

            # Add cumulative returns for Stock 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Cumulative Return'] * 100,
                    mode='lines',
                    name=f'{ticker1} Cumulative Return',
                    line=dict(color=colors['stock1'])
                ))

            # Add cumulative returns for Stock 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Cumulative Return'] * 100,
                    mode='lines',
                    name=f'{ticker2} Cumulative Return',
                    line=dict(color=colors['stock2'])
                ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - Cumulative Return Comparison",
                xaxis_title="Date",
                yaxis_title="Cumulative Return (%)",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)


#Example Usecase
#comparative_return_chart()


#Creating a function which takes 2 ticker as input and displays the volatility comparison chart.

def volatility_comparison_chart():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'stock1': '#FF6347',  # Stock 1
        'stock2': '#1E90FF',  # Stock 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Volatility Comparison Chart", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Volatility Metric:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='volatility-metric-dropdown',
                    options=[
                        {'label': 'Standard Deviation', 'value': 'std_dev'},
                        {'label': 'Average True Range (ATR)', 'value': 'atr'},
                    ],
                    value='std_dev',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '1 Month', 'value': '1mo'},
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='volatility-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('volatility-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('volatility-metric-dropdown', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, metric, period):
        try:
            # Fetch historical data for both stocks
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate volatility metrics
            if metric == 'std_dev':  # Standard Deviation
                data1['Volatility'] = data1['Adj Close'].rolling(window=20).std()
                data2['Volatility'] = data2['Adj Close'].rolling(window=20).std()
                metric_label = "Standard Deviation"
            elif metric == 'atr':  # Average True Range (ATR)
                data1['High-Low'] = data1['High'] - data1['Low']
                data1['High-Close'] = abs(data1['High'] - data1['Close'].shift())
                data1['Low-Close'] = abs(data1['Low'] - data1['Close'].shift())
                data1['True Range'] = data1[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
                data1['Volatility'] = data1['True Range'].rolling(window=14).mean()

                data2['High-Low'] = data2['High'] - data2['Low']
                data2['High-Close'] = abs(data2['High'] - data2['Close'].shift())
                data2['Low-Close'] = abs(data2['Low'] - data2['Close'].shift())
                data2['True Range'] = data2[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
                data2['Volatility'] = data2['True Range'].rolling(window=14).mean()
                metric_label = "Average True Range (ATR)"

            # Create the figure
            fig = go.Figure()

            # Add volatility for Stock 1
            if not data1.empty:
                fig.add_trace(go.Scatter(
                    x=data1.index,
                    y=data1['Volatility'],
                    mode='lines',
                    name=f'{ticker1} {metric_label}',
                    line=dict(color=colors['stock1'])
                ))

            # Add volatility for Stock 2
            if not data2.empty:
                fig.add_trace(go.Scatter(
                    x=data2.index,
                    y=data2['Volatility'],
                    mode='lines',
                    name=f'{ticker2} {metric_label}',
                    line=dict(color=colors['stock2'])
                ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"{ticker1} vs {ticker2} - {metric_label} Comparison",
                xaxis_title="Date",
                yaxis_title=metric_label,
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top')
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
#Example Usecase 
#volatility_comparison_chart()





#Creating a function for the Corellation Comparison Chart 

def correlation_comparison_chart():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'ticker1': '#FF6347',  # Tomato for Ticker 1
        'ticker2': '#1E90FF',  # Dodger Blue for Ticker 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Correlation Comparison Chart", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='ticker2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '1 Month', 'value': '1mo'},
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='correlation-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('correlation-comparison-chart', 'figure'),
        [
            Input('ticker1-input', 'value'),
            Input('ticker2-input', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(ticker1, ticker2, period):
        try:
            # Fetch historical data for both stocks
            data1 = yf.download(ticker1, period=period, interval='1d')
            data2 = yf.download(ticker2, period=period, interval='1d')

            # Calculate daily returns
            data1['Return'] = data1['Adj Close'].pct_change()
            data2['Return'] = data2['Adj Close'].pct_change()

            # Align data by date and drop NaN values
            merged_data = pd.concat([data1['Return'], data2['Return']], axis=1, keys=[ticker1, ticker2]).dropna()

            # Calculate correlation
            correlation = merged_data.corr().iloc[0, 1]

            # Create the figure
            fig = go.Figure()

            # Add scatter plot for Ticker 1
            fig.add_trace(go.Scatter(
                x=merged_data[ticker1],
                y=merged_data[ticker2],
                mode='markers',
                name=f"Correlation: {ticker1} vs {ticker2}",
                marker=dict(color=colors['ticker1'], size=8, opacity=0.7),
                hovertemplate=f"<b>{ticker1} Return:</b> {{x:.2%}}<br>" +
                              f"<b>{ticker2} Return:</b> {{y:.2%}}<extra></extra>"
            ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"Correlation of Returns: {ticker1} vs {ticker2}<br>Correlation Coefficient: {correlation:.2f}",
                xaxis_title=f"Daily Returns ({ticker1})",
                yaxis_title=f"Daily Returns ({ticker2})",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)



#Example Usecase 
#correlation_comparison_chart()



#Creating a function which shows the sector industry performance of the stock 



def sector_industry_comparison():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import dash_bootstrap_components as dbc

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'stock1': '#FF6347',  # Tomato for Stock 1
        'stock2': '#1E90FF',  # Dodger Blue for Stock 2
        'sector1': '#32CD32',  # Lime Green for Sector 1
        'sector2': '#FFD700',  # Gold for Sector 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Sector/Industry Comparison", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='stock1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='stock2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Enter Proxy Sector Index for First Stock:", style={'color': colors['text']}),
                dcc.Input(id='sector1-input', type='text', value='XLK', style={'margin-right': '20px'}),
                html.Label("Enter Proxy Sector Index for Second Stock:", style={'color': colors['text']}),
                dcc.Input(id='sector2-input', type='text', value='XLC'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '1 Month', 'value': '1mo'},
                        {'label': '6 Months', 'value': '6mo'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='sector-industry-comparison-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('sector-industry-comparison-chart', 'figure'),
        [
            Input('stock1-input', 'value'),
            Input('stock2-input', 'value'),
            Input('sector1-input', 'value'),
            Input('sector2-input', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(stock1, stock2, sector1, sector2, period):
        try:
            # Fetch historical data for stocks and sectors
            stock1_data = yf.download(stock1, period=period, interval='1d')
            stock2_data = yf.download(stock2, period=period, interval='1d')
            sector1_data = yf.download(sector1, period=period, interval='1d')
            sector2_data = yf.download(sector2, period=period, interval='1d')

            # Calculate cumulative returns
            stock1_data['Cumulative Return'] = (1 + stock1_data['Adj Close'].pct_change()).cumprod()
            stock2_data['Cumulative Return'] = (1 + stock2_data['Adj Close'].pct_change()).cumprod()
            sector1_data['Cumulative Return'] = (1 + sector1_data['Adj Close'].pct_change()).cumprod()
            sector2_data['Cumulative Return'] = (1 + sector2_data['Adj Close'].pct_change()).cumprod()

            # Create the figure
            fig = go.Figure()

            # Add traces for stocks
            fig.add_trace(go.Scatter(
                x=stock1_data.index,
                y=stock1_data['Cumulative Return'],
                mode='lines',
                name=f"{stock1} (Stock)",
                line=dict(color=colors['stock1'], width=2),
            ))
            fig.add_trace(go.Scatter(
                x=stock2_data.index,
                y=stock2_data['Cumulative Return'],
                mode='lines',
                name=f"{stock2} (Stock)",
                line=dict(color=colors['stock2'], width=2),
            ))

            # Add traces for sectors
            fig.add_trace(go.Scatter(
                x=sector1_data.index,
                y=sector1_data['Cumulative Return'],
                mode='lines',
                name=f"{sector1} (Sector)",
                line=dict(color=colors['sector1'], width=2, dash='dash'),
            ))
            fig.add_trace(go.Scatter(
                x=sector2_data.index,
                y=sector2_data['Cumulative Return'],
                mode='lines',
                name=f"{sector2} (Sector)",
                line=dict(color=colors['sector2'], width=2, dash='dash'),
            ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"Sector/Industry Comparison: {stock1} vs {stock2}",
                xaxis_title="Date",
                yaxis_title="Cumulative Return",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)
    
    
#Usecase Example 
#sector_industry_comparison()





#Creating a function to create a graph for dividend yield comparison
def dividend_yield_comparison():
    # Import necessary libraries
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.graph_objects as go
    import yfinance as yf
    import dash_bootstrap_components as dbc
    import pandas as pd

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define colors
    colors = {
        'background': '#0E1117',
        'text': '#E0E0E0',
        'stock1': '#FF6347',  # Tomato for Stock 1
        'stock2': '#1E90FF',  # Dodger Blue for Stock 2
    }

    # Define the layout
    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '20px'},
        children=[
            html.H1("Dividend Yield Comparison", style={'textAlign': 'center', 'color': colors['text']}),

            html.Div([
                html.Label("Enter First Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='stock1-input', type='text', value='AAPL', style={'margin-right': '20px'}),
                html.Label("Enter Second Stock Ticker:", style={'color': colors['text']}),
                dcc.Input(id='stock2-input', type='text', value='MSFT'),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Time Duration:", style={'color': colors['text']}),
                dcc.Dropdown(
                    id='duration-dropdown',
                    options=[
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '2 Years', 'value': '2y'},
                        {'label': '5 Years', 'value': '5y'},
                    ],
                    value='1y',
                    style={'margin-bottom': '20px'}
                ),
            ], style={'margin-bottom': '20px'}),

            dcc.Graph(id='dividend-yield-chart', style={'height': '700px'}),
        ]
    )

    # Define the callback to update the chart
    @app.callback(
        Output('dividend-yield-chart', 'figure'),
        [
            Input('stock1-input', 'value'),
            Input('stock2-input', 'value'),
            Input('duration-dropdown', 'value')
        ]
    )
    def update_chart(stock1, stock2, period):
        try:
            # Fetch historical data for stocks
            stock1_data = yf.Ticker(stock1)
            stock2_data = yf.Ticker(stock2)

            stock1_dividends = stock1_data.dividends
            stock2_dividends = stock2_data.dividends

            # Fetch historical close prices
            stock1_prices = yf.download(stock1, period=period, interval='1mo')['Adj Close']
            stock2_prices = yf.download(stock2, period=period, interval='1mo')['Adj Close']

            # Standardize datetime index to be timezone naive
            stock1_dividends.index = stock1_dividends.index.tz_localize(None)
            stock2_dividends.index = stock2_dividends.index.tz_localize(None)
            stock1_prices.index = stock1_prices.index.tz_localize(None)
            stock2_prices.index = stock2_prices.index.tz_localize(None)

            # Align the data to the same index
            stock1_dividends = stock1_dividends.reindex(stock1_prices.index, method='pad')
            stock2_dividends = stock2_dividends.reindex(stock2_prices.index, method='pad')

            # Calculate dividend yield
            stock1_yield = (stock1_dividends / stock1_prices) * 100
            stock2_yield = (stock2_dividends / stock2_prices) * 100

            # Create the figure
            fig = go.Figure()

            # Add traces for stocks
            fig.add_trace(go.Scatter(
                x=stock1_yield.index,
                y=stock1_yield,
                mode='lines+markers',
                name=f"{stock1} Dividend Yield",
                line=dict(color=colors['stock1'], width=2),
            ))
            fig.add_trace(go.Scatter(
                x=stock2_yield.index,
                y=stock2_yield,
                mode='lines+markers',
                name=f"{stock2} Dividend Yield",
                line=dict(color=colors['stock2'], width=2),
            ))

            # Update layout
            fig.update_layout(
                template="plotly_dark",
                title=f"Dividend Yield Comparison: {stock1} vs {stock2}",
                xaxis_title="Date",
                yaxis_title="Dividend Yield (%)",
                font=dict(color=colors['text']),
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
            )

        except Exception as e:
            # Handle errors
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=colors['text'])
            )
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background']
            )

        return fig

    # Run the app
    app.run_server(debug=True)

    
#Example Usecase 
#dividend_yield_comparison()


















































































































