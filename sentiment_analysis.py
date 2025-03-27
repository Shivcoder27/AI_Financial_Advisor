from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from yahoo_fin import news
from config import FINBERT_MODEL
import yahoo_fin.stock_info as si

# Load FinBERT model for sentiment analysis
tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL)
sentiment_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)

def get_financial_news(ticker):
    """
    Get the latest financial news for a given stock ticker.
    """
    headlines = news.get_yf_rss(ticker)  # Pass the ticker to fetch news for a specific stock
    return [headline["title"] for headline in headlines[:7]]  # Return top 7 headlines

def analyze_sentiment(news_text):
    """
    Analyze sentiment of the provided news text using FinBERT.
    """
    result = sentiment_pipeline(news_text)
    return result[0]["label"]
