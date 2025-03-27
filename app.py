import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
from config import GROQ_API_KEY, GROQ_MODEL
from budget_analysis import analyze_budget
from stock_insights import get_stock_price, plot_stock_trends
from sentiment_analysis import get_financial_news, analyze_sentiment
from risk_alerts import check_risk

# Set Streamlit Page Config
st.set_page_config(page_title="💰 AI Finance Advisor", layout="wide")

# Initialize session state for selection if not already initialized
if "selection" not in st.session_state:
    st.session_state.selection = "Budget Analysis"  # Default section

# ✅ Function to Get AI Investment Advice (Groq LLM)
def get_investment_advice(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Ensure this is the correct endpoint
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": GROQ_MODEL,  # Ensure this is the correct model name, e.g., "deepseek-chat"
        "messages": [
            {"role": "system", "content": "You are a Indian financial advisor. Provide smart investment strategies based on the user's budget.Also try to answer in points and not forget to give suggestions"},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Error fetching investment advice: {response.json().get('error', {}).get('message', 'Unknown issue')}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ API Request Error: {str(e)}"

# 🟢 Horizontal Navigation Bar (Using Columns)
st.title("💼 AI Finance Advisor")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Budget Analysis"):
        st.session_state.selection = "Budget Analysis"
        
with col2:
    if st.button("Stock Insights"):
        st.session_state.selection = "Stock Insights"

with col3:
    if st.button("Financial News & Sentiment"):
        st.session_state.selection = "Financial News & Sentiment"

with col4:
    if st.button("AI Investment Recommendations"):
        st.session_state.selection = "AI Investment Recommendations"

# 🟢 Budget Analysis Section
if st.session_state.selection == "Budget Analysis":
    st.header("📊 Budget Analysis")
    income = st.number_input("💵 Monthly Income", min_value=0, step=1000)
    num_income_sources = st.number_input("📈 Number of Income Sources", min_value=1, step=1)
    income_sources = {}
    for i in range(num_income_sources):
        source = st.text_input(f"Income Source {i+1} Name", key=f"source_{i}")
        amount = st.number_input(f"Income from {source}", min_value=0, step=100, key=f"amount_{i}")
        income_sources[source] = amount

    living_expenses = st.number_input("📉 Total Living Expenses", min_value=0, step=100)
    investment_area = st.text_input("Investment Area (e.g., stocks, real estate)")
    investment_amount = st.number_input(f"Amount Invested in {investment_area}", min_value=0, step=100)
    goal = st.text_input("Future Goal (Optional)", placeholder="e.g., Buy a house, retirement")
    total_savings = income - living_expenses - investment_amount

    # Display calculated savings
    st.write(f"✅ Total Savings: {total_savings}")

    if st.button("Submit Budget"):
        # Validate that all values are valid
        sizes = [sum(income_sources.values()), living_expenses, investment_amount, total_savings]
        
        # Check for NaN or negative values
        invalid_values = [np.isnan(size) or size is None or size < 0 for size in sizes]
        
        if any(invalid_values):
            st.error(f"Error: Some financial values are invalid (NaN or negative). Please check your inputs. Invalid fields: {', '.join([label for label, invalid in zip(['Income', 'Expenses', 'Investments', 'Savings'], invalid_values) if invalid])}")
        else:
            # If all values are valid, generate the pie chart with appropriate size
            labels = ['Income', 'Expenses', 'Investments', 'Savings']
            colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
            
            fig1, ax1 = plt.subplots(figsize=(3,2 ))  # Adjust the size of the chart
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})  # Adjust text size
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)
            

            # 🟢 Generate and display the budget analysis
            advice = analyze_budget(income, income_sources, living_expenses, investment_area, investment_amount, goal)
            st.write("💡 Budget Advice: ", advice)

# 🟢 Stock Insights Section
elif st.session_state.selection == "Stock Insights":
    st.header("📈 Stock Insights")
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, BTC-USD)")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Get Stock Price"):
            price = get_stock_price(symbol)
            st.write(f"📊 Current Price of {symbol}: ${price}")
    
    with col2:
        if st.button("Check Risk"):
            risk_alert = check_risk(symbol)
            st.write(risk_alert)

    # Show Stock Trends
    if st.button("Show Stock Trends"):
        fig = plot_stock_trends(symbol)
        if fig:
            st.plotly_chart(fig)
        else:
            st.warning("Stock data not available.")

# 🟢 Financial News & Sentiment Section
elif st.session_state.selection == "Financial News & Sentiment":
    st.header("📰 Financial News & Sentiment")
    ticker = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, BTC-USD)", key="ticker_input")
    
    if st.button("Get Financial News"):
        if ticker:
            news_list = get_financial_news(ticker)
            for news in news_list:
                sentiment = analyze_sentiment(news)
                st.write(f"📰 {news} - **{sentiment}**")
        else:
            st.warning("Please enter a stock symbol.")

# 🟢 AI Investment Advice Section
elif st.session_state.selection == "AI Investment Recommendations":
    st.header("💡 AI Investment Recommendations")
    query = st.text_area("Ask AI about investment strategies", key="investment_query")
    
    if st.button("Get Advice"):
        if query.strip():
            advice = get_investment_advice(query)
            st.write("💡 AI Suggests:", advice)
        else:
            st.warning("Please enter a valid investment strategy query.")
