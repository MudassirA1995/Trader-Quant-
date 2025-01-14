# Trader-Quant-
Python Based Library for Stock Analysts , Traders , Researchers and Data Scientists. With these commands the user can convert their VS Code terminals into a Bloomberg like Trader terminal.

## Table of Contents
- [Introduction](#introduction)
- [Intended Use Cases](#intended-usecases)
- [get_pe_ratio()](#get_pe_ratio)
- [get_pb_ratio()](#get_pb_ratio)
- [get_ps_ratio()](#get_ps_ratio)
  





## Introduction 

Trader Quant is a Python library designed to empower traders and quantitative analysts by streamlining the process of data analysis, strategy development, and execution in financial markets. Built with a focus on simplicity and efficiency, the library integrates seamlessly with popular financial data sources and APIs, enabling users to access real-time and historical market data with minimal setup. With its robust set of tools for technical analysis, machine learning, and risk management, Trader Quant provides a comprehensive platform for creating, testing, and optimizing trading strategies. The library’s modular architecture ensures flexibility, making it suitable for both beginner traders exploring algorithmic trading and seasoned quants seeking to refine their strategies.

One of the standout features of Trader Quant is its ability to handle large datasets efficiently, enabling users to backtest strategies on decades of market data with speed and accuracy. It includes pre-built modules for calculating key indicators like moving averages, RSI, and MACD, as well as advanced functionalities such as portfolio optimization, statistical arbitrage, and sentiment analysis. The library supports integration with live trading platforms, making it possible to transition seamlessly from strategy development to execution. With an intuitive API and detailed documentation, Trader Quant aims to reduce the complexity of quantitative trading, empowering users to focus on innovation and strategy performance.

Trader Quant is built on top of python libraries like numpy , pandas , matplotlib , plotliy , dash and y finance. 


##  Intended Usecases 


### Use Cases for Trader Quant Python Library
Trader Quant is a Python library designed to simplify and enhance financial analysis and decision-making for traders, analysts, and investors. With a focus on providing ready-to-use, interactive tools, Trader Quant enables users to analyze complex financial metrics like Sharpe ratios, volatility trends, and risk analysis with minimal coding. The library leverages the power of Dash for creating dynamic dashboards that visualize key insights in real-time, making it easier for users to track and interpret market trends. Whether you're looking to evaluate the risk-adjusted returns of a stock, identify patterns in market volatility, or manage a portfolio, Trader Quant provides tailored functions that handle data retrieval, processing, and visualization seamlessly.

Trader Quant is especially useful for both beginners and seasoned professionals in the financial domain. For novice users, it offers intuitive interfaces and pre-built visualizations, such as rolling volatility and Sharpe ratio dashboards, enabling them to grasp advanced concepts without extensive financial knowledge. For experts, the library's modular and customizable nature allows integration with existing analytics pipelines and further fine-tuning of calculations. The ability to interactively analyze and compare financial metrics makes Trader Quant a valuable tool for informed trading decisions, strategic planning, and academic research. Its focus on accessibility and flexibility ensures that users of all skill levels can harness data-driven insights effectively.


## get_pe_ratio()

This function, get_pe_ratio, is designed to calculate the Price-to-Earnings (P/E) ratio for a specified stock. The P/E ratio is a financial metric widely used by investors and traders to evaluate the relative value of a company's stock. It represents the relationship between a company's current stock price and its earnings per share (EPS).
Definition of get_pe_ratio
•	Function Input: A stock ticker symbol (e.g., "AAPL" for Apple).
•	Process: It retrieves data from the Yahoo Finance API via the yfinance library, fetching the current price (current_price) and trailing earnings per share (trailingEps) of the stock.
•	Calculation: The P/E ratio is calculated by dividing the current_price by eps.
•	Output: The function returns the P/E ratio if available, or None if the required data is missing.
Significance for Traders
For traders, the P/E ratio is essential for comparing the valuation of companies. A high P/E ratio could suggest that the stock is overvalued or that investors expect high growth rates in the future, while a low P/E might indicate undervaluation or slower growth expectations. By analyzing the P/E ratio, traders can make more informed decisions about whether to buy, hold, or sell a stock.
What the Function Covers
•	Fetches Current Price: Retrieves the latest market price of the stock.
•	Fetches EPS: Gathers earnings data, which is essential for calculating the P/E ratio.
•	Handles Data Availability: Includes error handling in case the data for current price or EPS is unavailable for the given ticker, which is common for certain stocks or newly listed companies.
Overall, this function is a practical tool for traders aiming to quickly assess a stock's valuation relative to its earnings, aiding in fundamental analysis and comparison across stocks.

### Use Case 

![image](https://github.com/user-attachments/assets/88fe1fed-f9ef-4980-b923-d3a1c3e08a0b)

### Source Code 

```python

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


```


## get_pb_ratio()

Significance of the Financial Metric: Price-to-Book (P/B) Ratio
The Price-to-Book (P/B) ratio is a financial metric that compares a company's market value to its book value. It is calculated as:
P/B=Market Price per ShareBook Value per ShareP/B = \frac{\text{Market Price per Share}}{\text{Book Value per Share}}P/B=Book Value per ShareMarket Price per Share
•	Market Price per Share: The current trading price of a single share of the company.
•	Book Value per Share: The value of the company’s net assets (total assets minus liabilities) divided by the total number of outstanding shares.
Why is the P/B Ratio Important?
1.	Valuation Indicator:
o	A low P/B ratio (< 1) may indicate that the stock is undervalued relative to its book value.
o	A high P/B ratio may suggest overvaluation or that investors expect high growth.
2.	Industry-Specific Insight: The P/B ratio is more relevant for asset-heavy industries like banking, real estate, or manufacturing.
3.	Risk Assessment: It provides insights into the company’s financial health and investor sentiment.

### Source Code 


```python

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


```

### Code Explanation 


The function get_pb_ratio retrieves the P/B ratio for a specified stock ticker using the yfinance library. Here's a breakdown:
1.	Input:
o	ticker: The stock's ticker symbol (e.g., "AAPL" for Apple Inc.).
2.	Fetching Stock Data:
o	The yfinance library's Ticker object fetches detailed stock information for the specified ticker.
3.	Data Retrieval:
o	The currentPrice and bookValue are extracted from the info dictionary provided by yfinance.
4.	P/B Ratio Calculation:
o	If the required data (currentPrice and bookValue) is available, the P/B ratio is calculated using: P/B Ratio=currentPricebookValue\text{P/B Ratio} = \frac{\text{currentPrice}}{\text{bookValue}}P/B Ratio=bookValuecurrentPrice
5.	Error Handling:
o	If any of the required fields (currentPrice or bookValue) are missing, a KeyError exception is handled gracefully. A message is printed indicating that the data is unavailable, and the function returns None.
6.	Output:
o	Returns the calculated P/B ratio if successful, or None if the data is not available.

### Example Usecase 

![image](https://github.com/user-attachments/assets/6903ced8-9f1c-4947-90ff-b0b0f30b3853)



## get_ps_ratio()

### Significance of the Financial Metric: Price-to-Sales (P/S) Ratio
The Price-to-Sales (P/S) ratio is a financial metric that measures the value investors place on a company's sales relative to its market value. It is calculated as:
P/S=Market Price per ShareRevenue per ShareP/S = \frac{\text{Market Price per Share}}{\text{Revenue per Share}}P/S=Revenue per ShareMarket Price per Share
•	Market Price per Share: The current trading price of a single share of the company.
•	Revenue per Share: The total revenue of the company divided by the number of outstanding shares.
Why is the P/S Ratio Important?
1.	Valuation Benchmark:
o	A low P/S ratio may indicate that a company is undervalued compared to its sales.
o	A high P/S ratio may suggest that investors expect significant future growth.
2.	Comparative Analysis: Useful for comparing companies in the same industry, especially for firms with no profits (e.g., startups or growth companies).
3.	Industry Neutrality: While more relevant for revenue-driven industries, the P/S ratio can be applied across a broad range of sectors.
________________________________________


### Code Explanation 
The function get_ps_ratio retrieves the P/S ratio for a specified stock ticker using the yfinance library. Here's how it works:
1.	Input:
o	ticker: The stock's ticker symbol (e.g., "AAPL" for Apple Inc.).
2.	Fetching Stock Data:
o	The yfinance library's Ticker object fetches comprehensive stock information for the specified ticker.
3.	Data Retrieval:
o	The currentPrice and revenuePerShare fields are extracted from the info dictionary provided by yfinance.
4.	P/S Ratio Calculation:
o	If the required data (currentPrice and revenuePerShare) is available, the P/S ratio is calculated using: P/S Ratio=currentPricerevenuePerShare\text{P/S Ratio} = \frac{\text{currentPrice}}{\text{revenuePerShare}}P/S Ratio=revenuePerSharecurrentPrice
5.	Error Handling:
o	If either currentPrice or revenuePerShare is unavailable, the function handles the KeyError gracefully. It prints a message and returns None.
6.	Output:
o	Returns the calculated P/S ratio if successful, or None if the data is unavailable.


### Example Usecase 

![image](https://github.com/user-attachments/assets/472b2ff3-eabf-4bfa-9642-e30bdc95d792)


### Source Code 

```python


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



```







