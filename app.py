import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
from datetime import datetime
import yfinance as yf
import plotly.graph_objects as go
from pycaret.regression import *

# streamlit run app.py --server.address=127.0.0.1

st.set_page_config(layout="wide")
# st.title("Stock Analysis On NIFTY50")
# st.header("Stock Analysis On NIFTY50")
st.markdown(
    "<h2 style='text-align: center; color: white;'>Stock Analysis On NIFTY50</h2>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: white;'>Detailed Analysis and Visualization for Top 50 NIFTY Stocks</p>",
    unsafe_allow_html=True)
# st.subheader("Detailed Analysis and Visualization for Top 50 NIFTY Stocks")

############ Variables ##########################
stocks_list = [
    'ONGC.NS', 'UPL.NS', 'ITC.NS', 'SUNPHARMA.NS', 'IOC.NS', 'JSWSTEEL.NS',
    'SBIN.NS', 'SHREECEM.NS', 'HINDUNILVR.NS', 'NTPC.NS', 'HINDALCO.NS',
    'LT.NS', 'BAJFINANCE.NS', 'DIVISLAB.NS', 'TATACONSUM.NS', 'HDFCLIFE.NS',
    'M&M.NS', 'INFY.NS', 'GRASIM.NS', 'WIPRO.NS', 'COALINDIA.NS',
    'BRITANNIA.NS', 'INDUSINDBK.NS', 'BHARTIARTL.NS', 'SBILIFE.NS',
    'ICICIBANK.NS', 'TATASTEEL.NS', 'RELIANCE.NS', 'HCLTECH.NS',
    'BAJAJ-AUTO.NS', 'BPCL.NS', 'TCS.NS', 'NESTLEIND.NS', 'ADANIPORTS.NS',
    'AXISBANK.NS', 'ULTRACEMCO.NS', 'CIPLA.NS', 'TITAN.NS', 'HEROMOTOCO.NS',
    'KOTAKBANK.NS', 'BAJAJFINSV.NS', 'POWERGRID.NS', 'ASIANPAINT.NS',
    'EICHERMOT.NS', 'TATAMOTORS.NS', 'DRREDDY.NS', 'HDFCBANK.NS', 'HDFC.NS',
    'MARUTI'
]

#################################################################
options = st.selectbox("Select a Stock", stocks_list)

end = datetime.today().date()
start = end - timedelta(days=1456)
@st.cache(allow_output_mutation=True)
def stock_fn(options, start, end):
    df = yf.download(options, end=end, start = start)
    df = df.reset_index()
    df["MarktCap"] = df["Open"] * df["Volume"]
    df["MA50"] = df["Open"].rolling(50).mean()
    df["MA200"] = df["Open"].rolling(200).mean()
    df["returns"] = ((df["Close"] / df["Close"].shift(1)) - 1) * 100
    return df

stock = stock_fn(options,start, end)

closing_price = round(stock['Close'].iloc[-1], 2)
return_percent = round(stock['returns'].iloc[-1], 2)
return_value = round((stock["Close"].iloc[-1] - stock["Close"].iloc[-2]), 2)

if return_value >= 0:
    rotation = 0
    clr = "#42FF00"
    height = "50px"
else:
    rotation = 180
    clr = "#FF0000"
    height = "65px"
tab = f"""
<html>

<head>
    <link href="https://fonts.googleapis.com/css?family=Montserrat&display=swap" rel="stylesheet" />
    <style></style>
</head>

<body>
    <div style="        
    width: 400px;
    height: 96px;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    opacity: 1;
    position: relative;
    top: 0px;
    left: 0px;
    overflow: hidden;">
        <div style="        
        width: 250px;
        height: 96px;
        background: rgba(38, 39, 48, 1);
        opacity: 1;
        position: relative;
        top: 0px;
        left: 0px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        overflow: hidden;">
        </div>
        <div style="        
        position: absolute;
        top:{height};
        left: 15px;
        width: 0;
        height: 0;
        transform: rotate({rotation}deg);
        border: solid 15px;
        border-color: transparent transparent {clr} transparent;"></div>
        <span style="        
            width: 190px;
            color: white;
            position: absolute;
            top: 2px;
            left: 15px;
            font-family: Montserrat;
            font-weight: SemiBold;
            font-size: 38px;
            opacity: 1;
            text-align: center;">{closing_price}</span>
        <span style="        
            width: 130px;
            color:{clr};
            position: absolute;
            top: 51px;
            left: 55px;
            font-family: Montserrat;
            font-weight: Medium;
            font-size: 26px;
            opacity: 1;
            text-align: left;"> {return_value}</span>
        <span style="        
            width: 130px;
            color:{clr};
            position: absolute;
            top: 51px;
            left:130px;
            font-family: Montserrat;
            font-weight: Medium;
            font-size: 24px;
            opacity: 1;
            text-align: left;">({return_percent}%)</span>
    </div>
</body>

</html><br>"""

with open("tabcss.html", "r") as f:
    tabcss = f.read()
tab_bar = tab.replace("<style></style>", tabcss)
st.markdown(tab_bar, unsafe_allow_html=True)
#################### Plot ##############3

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=stock["Date"],
        open=stock["Open"],
        high=stock["High"],
        low=stock["Low"],
        close=stock["Close"],
    ))

fig.update_layout(
    hovermode="x unified",
    autosize=False,
    xaxis_rangeslider_visible=False,
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span><span style='font-size: 24px;color:#9FE6A0'> HIGH</span><span style='font-size: 24px;color:white'> vs</span><span style='font-size: 24px;color:#F55C47'> LOW</span>",
        "x": 0.5,
        "xanchor": "center",
        'yanchor': 'top'
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

#################################
fig = go.Figure()

# Add traces
fig.add_trace(go.Line(x=stock["Date"], y=stock["Open"], name=f"{options}"))

fig.update_layout(
    hovermode="x unified",
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'> Opening Price</span>",
        "x": 0.5,
        "xanchor": "center",
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure()

# Add traces
fig.add_trace(go.Line(x=stock["Date"], y=stock["Volume"], name="TCS"))

fig.update_layout(
    hovermode="x unified",
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'> Volume Traded</span>",
        "x": 0.5,
        "xanchor": "center",
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

########################################33333
fig = go.Figure()
# Add traces
fig.add_trace(go.Line(x=stock["Date"], y=stock["MarktCap"], name=f"{options}"))

fig.update_layout(
    hovermode="x unified",
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'> Market Cap</span>",
        "x": 0.5,
        "xanchor": "center",
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

###########################################################

fig = go.Figure()
# Add traces
fig.add_trace(go.Line(x=stock["Date"], y=stock["Open"], name=f"{options}"))
fig.add_trace(go.Line(x=stock["Date"], y=stock["MA50"], name="Moving Avg 50"))
fig.add_trace(go.Line(x=stock["Date"], y=stock["MA200"],
                      name="Moving Avg 200"))

fig.update_layout(
    hovermode="x unified",
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'> Opening Trend with Moving Avg</span>",
        "x": 0.5,
        "xanchor": "center",
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

######################################3333
fig = go.Figure()

# Add traces
fig.add_trace(go.Histogram(
    x=stock["returns"],
    name=f"{options} Returns",
))

fig.update_layout(
    xaxis_title="Share % Return",
    hovermode="x unified",
    barmode="overlay",
    template="plotly_dark",
    title={
        "text":
        f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'> Volatility</span>",
        "x": 0.5,
        "xanchor": "center",
    },
    margin=dict(
        l=10,  # left
        r=10,  # right
        t=60,  # top
        b=10,  # bottom
    ),
    paper_bgcolor="rgb(38,39,48)",
    plot_bgcolor="rgb(38,39,48)",
)
st.plotly_chart(fig, use_container_width=True)

#################### Forecasting ########################


st_date = datetime.today().date()
seven_days_after = st_date + timedelta(days=7)
all_dates = pd.date_range(start=st_date, end=seven_days_after, freq='D')
# create empty dataframe
score_df = pd.DataFrame()
# add columns to dataset
score_df['Date'] = all_dates
score_df['month'] = [i.month for i in score_df['Date']]
score_df['year'] = [i.year for i in score_df['Date']]
score_df['day_of_week'] = [i.dayofweek for i in score_df['Date']]
score_df['day_of_year'] = [i.dayofyear for i in score_df['Date']]

final_forecast = score_df.copy()
final_forecast.drop(columns=['month', 'year', 'day_of_week', 'day_of_year'], inplace=True)



l = load_model('models/' + f"{options}", verbose=False)
p = predict_model(l, data=score_df)
p.drop(columns=['month','year','day_of_week','day_of_year'],inplace=True)
final_forecast = pd.merge(final_forecast, p, how = 'left', left_on='Date', right_on ='Date')

###########################################################

key = st.radio("Choose the Time", ('1M', '5M', '1Y'))

if key == '1M':
    fig = go.Figure()
    # Add traces
    fig.add_trace(
        go.Line(x=stock["Date"].iloc[-30:],
                y=stock["Close"].iloc[-30:],
                name=f"{options}"))
    fig.add_trace(
        go.Line(x=final_forecast["Date"],
                y=final_forecast["Label"],
                name="Forecasted"))

    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        title={
            "text":
            f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'>Closing Price Forecasting for 7 days</span>",
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(
            l=10,  # left
            r=10,  # right
            t=60,  # top
            b=10,  # bottom
        ),
        paper_bgcolor="rgb(38,39,48)",
        plot_bgcolor="rgb(38,39,48)",
    )
    st.plotly_chart(fig, use_container_width=True)
elif key == "5M":
    fig = go.Figure()
    # Add traces
    fig.add_trace(
        go.Line(x=stock["Date"].iloc[-150:],
                y=stock["Close"].iloc[-150:],
                name=f"{options}"))
    fig.add_trace(
        go.Line(x=final_forecast["Date"],
                y=final_forecast["Label"],
                name="Forecasted"))

    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        title={
            "text":
            f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'>Closing Price Forecasting for 7 days</span>",
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(
            l=10,  # left
            r=10,  # right
            t=60,  # top
            b=10,  # bottom
        ),
        paper_bgcolor="rgb(38,39,48)",
        plot_bgcolor="rgb(38,39,48)",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = go.Figure()
    # Add traces
    fig.add_trace(
        go.Line(x=stock["Date"].iloc[-365:],
                y=stock["Close"].iloc[-365:],
                name=f"{options}"))
    fig.add_trace(
        go.Line(x=final_forecast["Date"],
                y=final_forecast["Label"],
                name="Forecasted"))

    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        title={
            "text":
            f"<span style='font-size: 20px;'>{options}</span> <span style='font-size: 24px;'>Closing Price Forecasting for 7 days</span>",
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(
            l=10,  # left
            r=10,  # right
            t=60,  # top
            b=10,  # bottom
        ),
        paper_bgcolor="rgb(38,39,48)",
        plot_bgcolor="rgb(38,39,48)",
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("Gain Calculator & Predictor")
col1, col2 = st.columns(2)
with col1:
    quantity = st.number_input(f'Invested Quantity of {options} Share',
                               min_value=0)

with col2:
    stock_price = st.number_input(f'Invested Stock Price of {options}/Share ')

investment = round((quantity * stock_price), 2)
current_price = round((closing_price * quantity), 2)
current_gain = current_price - investment
current_gain_percent = round((current_gain / investment * 100), 2)

price_after_week = round((quantity * final_forecast["Label"].iloc[-1]), 2)
gain_after_week = round((price_after_week - investment), 2)
gain_after_week_percent = round((gain_after_week / investment * 100), 2)

col3, col4, col5 = st.columns(3)
col3.metric("Total Investment", investment)
col4.metric("Current gain", current_gain, f"{current_gain_percent}%")
col5.metric("Gain After a week", gain_after_week,
            f"{gain_after_week_percent}%")
