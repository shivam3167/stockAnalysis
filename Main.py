import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt
import datetime


st.title("Stock Market Analysis & Prediction ")
stock = st.sidebar.text_input("Stock Name",value='GOOG')

default_date = datetime.date(2023 , 1 ,1)

start_date = st.sidebar.date_input("Start_date", value = default_date)
end_date = st.sidebar.date_input("End_date")

data = yf.download(stock , start = start_date , end = end_date)

#LINE GRAPH

fig = px.line(data, x = data.index , y = data['Adj Close'] , title = stock)
st.plotly_chart(fig)

#CURRENT PRICE

if not data.empty:
    current_price = data['Adj Close'][-1]
    st.subheader("Price of stock ")
    st.markdown(f"""
        <div style="
            font-size: 24px; 
            color : green; 
            padding:0 0 0 3px;">
            <strong> {current_price:.2f}</strong>
        </div>
    """,unsafe_allow_html=True)

#TAB

over_view , fundamental_data , technical_analysis , top_news= st.tabs(["OverView" , "Fundamental Data" , "Technical Analysis","Top News"])

with over_view :

    #PERCANTEGE CHANGE

    st.header("Price Movements of Stock")
    data2=data
    data2["% Change"] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    st.write(data2)

    #STOCK SECTOR

    stock1 = yf.Ticker(stock)
    info = stock1.info
    sector = info.get('sector')
    st.subheader("Sector")
    st.markdown(f"""
        <div style="
            font-size: 18px; 
            border : 2px solid gray; 
            padding:0 0 0 3px;">
            <strong> {sector}</strong>
        </div>
    """,unsafe_allow_html=True)

    #STOCK MARKET CAP VALUE

    info = stock1.info
    market_cap = info.get('marketCap')
    st.subheader("MarketCap Value")
    st.markdown(f"""
        <div style="
            font-size: 18px; 
            border : 2px solid gray; 
            padding:0 0 0 3px;">
            <strong> {market_cap/1e7:.2f} crore</strong>
        </div>
    """,unsafe_allow_html=True)

    #STOCK MARKET CAP

    if 'sector' in info and 'marketCap' in info:
        sector = info['sector']
        market_cap = info['marketCap']

        st.subheader('Market Cap Type')

        # Market cap classification
        if market_cap > 75000 * 1e7:
            st.markdown(f"""
            <div style="
                font-size: 18px; 
                border : 2px solid gray; 
                padding:0 0 0 3px;">
                <strong>Large Cap</strong>
            </div>""",unsafe_allow_html=True)
        elif 15000 * 1e7 <= market_cap <= 75000 * 1e7:
            st.markdown(f"""
            <div style="
                font-size: 18px; 
                border : 2px solid gray; 
                padding:0 0 0 3px;">
                <strong>Mid Cap</strong>
            </div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                font-size: 18px; 
                border : 2px solid gray; 
                padding:0 0 0 3px;">
                <strong>Small Cap</strong>
            </div>""",unsafe_allow_html=True)
    else:
        st.write("Unable to fetch stock data. Please check the ticker symbol.")

    #ANNUAL RETURN

    annual_return = data2['% Change'].mean()*252*100
    st.subheader("Annual Return ")
    st.markdown(f"""
        <div style="
            font-size: 18px;
            border : 2px solid gray; 
            padding:0 0 0 3px;">
            <strong> {annual_return:.2f}%</strong>
        </div>
    """,unsafe_allow_html=True)

    #VOLATILITY

    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.subheader("Volatility ")
    st.markdown(f"""
        <div style="
            font-size: 18px; 
            border : 2px solid gray; 
            padding:0 0 0 3px;">
            <strong> {stdev*100:.2f}%</strong>
        </div>
    """,unsafe_allow_html=True)

    #RISK STANDARD DEVIATION

    st.subheader("Risk Standard Deviation ")
    st.markdown(f"""
        <div style="
            font-size: 18px; 
            border : 2px solid gray; 
            padding:0 0 0 3px;
            font : Times New Roman;">
            <strong> {annual_return/(stdev*100):.2f}</strong>
        </div>
    """,unsafe_allow_html=True)


from alpha_vantage.fundamentaldata import FundamentalData

with fundamental_data : 

    key = 'SO9XJDF710RLGACR'

    #ANNUAL BALANCE SHEET

    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(stock)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)

    #ANNUAL INCOME STATEMENT

    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(stock)[0]
    insc = income_statement.T[2:]
    insc.columns = list(income_statement.T.iloc[0])
    st.write(insc)

    #CASH FLOW STATEMENT

    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(stock)[0]
    cashF = cash_flow.T[2:]
    cashF.columns = list(cash_flow.T.iloc[0])
    st.write(cashF)


with technical_analysis :

    #SIMPLE GRAPH OF STOCK

    st.subheader("STOCK GRAPH")
    st.line_chart(data[['Close']])

    #DAILY RETURN

    data['Daily Return'] = data['Close'].pct_change()*100
    st.subheader("Daily Returns")
    fig1 = px.line(data, x = data.index , y = data['Daily Return'])
    st.plotly_chart(fig1)

    #MOVING AVERAGES

    data['100-day SMA'] = data['Close'].rolling(window=100).mean()
    data['200-day SMA'] = data['Close'].rolling(window=200).mean()

    #100 DAYS MOVING AVERAGE
    
    st.subheader("Moving Averages (100-days)")
    st.line_chart(data[['Close','100-day SMA']])

    #200 DAYS MOVING AVERAGE

    st.subheader("Moving Averages (200-days)")
    st.line_chart(data[['Close','200-day SMA']])

    #(100 DAYS - 200 DAYS) MOVING AVERAGE

    st.subheader("Moving Averages (100Days - 200Days)")
    st.line_chart(data[['Close','100-day SMA','200-day SMA']])

    #VOLUMN

    st.subheader("Volumn of stock")
    vol = stock1.history(period="1mo")

    st.bar_chart(data['Volume'])



from stocknews import StockNews

with top_news :
    st.header(f'News of {stock}')
    sn = StockNews(stock , save_news = False)
    df_news = sn.read_rss()
    
    for i in range(10):

        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

