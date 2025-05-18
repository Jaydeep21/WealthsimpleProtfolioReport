import json, openai, settings
from logger import Logger
from datetime import datetime
import yfinance as yf
class ResearchAnalysis:
    def __init__(self):
        self.logger = Logger("ResearchAnalysis")
        
    
    def research_analysis(self, symbol):
        """Get research-based analysis for a symbol using OpenAI"""
        self.logger.info(f"Performing research analysis for {symbol}")
        
        api_key = settings.API_KEY
        model = settings.MODEL  # Use the model from config, default to gpt-4
        
        if api_key == 'your_openai_api_key':
            self.logger.warning("OpenAI API key not configured. Skipping research analysis.")
            return {"error": "OpenAI API key not configured"}
            
        try:
            # Configure OpenAI client
            openai.api_key = api_key
            
            # Get recent news about the stock
            news = self.get_stock_news(symbol)
            news_summary = "\n".join([f"- {item['headline']}" for item in news[:5]]) if news else "No recent news found."
            
            # Prepare prompt for OpenAI
            prompt = f"""
            Please analyze the stock {symbol} based on the following recent news:
            
            {news_summary}
            
            Provide a concise analysis covering:
            1. Overall sentiment (bullish/bearish/neutral)
            2. Key drivers or catalysts
            3. Potential risks
            4. Future outlook
            
            Format your response as JSON with these fields.
            """
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=model,  # Use model from config
                messages=[{"role": "system", "content": "You are a financial analyst providing concise stock analysis."},
                         {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            analysis = json.loads(analysis_text)
            
            # Add news sources to the response
            analysis['recent_news'] = news[:5] if news else []
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Research analysis failed for {symbol}: {str(e)}")
            return {"error": str(e)}
    def get_stock_news(self, symbol, max_items=10):
        """Get recent news for a stock symbol"""
        try:
            # Using Yahoo Finance for news
            stock = yf.Ticker(symbol)
            news = stock.news
            
            # Format news items
            formatted_news = []
            for item in news[:max_items]:
                formatted_news.append({
                    'headline': item.get('title', 'No title'),
                    'source': item.get('publisher', 'Unknown source'),
                    'url': item.get('link', ''),
                    'published': datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S')
                })
                
            return formatted_news
        except Exception as e:
            self.logger.error(f"Failed to get news for {symbol}: {str(e)}")
            return []