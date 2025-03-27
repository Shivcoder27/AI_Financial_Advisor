import requests
from config import GROQ_API_KEY, GROQ_MODEL
import json

# ✅ Function to Get LLM-Based Budget Analysis and Suggestions
def analyze_budget(income, income_sources, living_expenses, investment_area, investment_amount, goal):
    # Prepare the input data for the model query
    income_sources_str = ', '.join([f"{source}: {amount}" for source, amount in income_sources.items()])
    
    query = (f"User has a monthly income of {income}, with sources: {income_sources_str}. "
             f"Total living expenses are {living_expenses}. "
             f"User invests {investment_amount} in {investment_area}. "
             f"Savings after all expenses and investments is {income - living_expenses - investment_amount}. "
             f"User's goal is to {goal}.\n"
             "Provide personalized financial advice on budget optimization, investment improvement, "
             "savings growth, and achieving the user's goal.")

    # Call the Groq LLM to get investment advice
    url = "https://api.groq.com/openai/v1/chat/completions"  # Ensure the correct endpoint is used
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,  # Ensure this is the correct model name
        "messages": [
            {"role": "system", "content": "You are a Indian financial advisor. Provide personalized budgeting and investment advice according to indian market and in ruppee. it should include summary or conclusion don't over explain only give valuable suggestions in points"},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        # Send request to Groq API
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and "choices" in response_data:
            # Extract the response text from the model
            advice = response_data["choices"][0]["message"]["content"]
            return advice
        else:
            return "❌ Error fetching budget advice: " + response_data.get('error', {}).get('message', 'Unknown issue')

    except requests.exceptions.RequestException as e:
        return f"❌ API Request Error: {str(e)}"
