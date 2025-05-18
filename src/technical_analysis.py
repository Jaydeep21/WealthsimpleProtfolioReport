from logger import Logger
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from technical_indicators import TechnicalIndicators
import settings
from research_analysis import ResearchAnalysis
class TechnicalAnalysis:
    def __init__(self):
        self.logger = Logger("TechnicalAnalysis")
    def get_symbol_with_exchange(self, symbol):
        """Add exchange suffix for non-US stocks if needed"""        
            
        # Simple heuristic: Canadian stocks often need .TO suffix
        # This is a simplified approach - in production, you'd want a more robust mapping
        if symbol.endswith('.TO') or symbol.endswith('.V') or symbol.endswith('.NE'):
            return symbol  # Already has exchange suffix
        
        # Add exchange mappings as needed
        exchange_mappings = {
            'TSX': '.TO',   # Toronto Stock Exchange
            'TSXV': '.V',   # TSX Venture Exchange
            'NEO': '.NE',   # Aequitas NEO Exchange
            # Add more exchanges as needed
        }
        
        # For simplicity, we're not checking which exchange the stock is from
        # In a real app, you would query this info from Wealthsimple API
        # For now, we'll assume TSX if it's a Canadian stock without suffix
        
        # Check if this might be a Canadian stock
        # Simple heuristic: many (but not all) Canadian stocks have a 3-letter symbol
        if len(symbol) <= 3 and symbol.isalpha():
            return f"{symbol}.TO"  # Try TSX
            
        return symbol  # Default: assume US stock
    def analyze_performance(self, positions_by_account):
        """Analyze performance of all holdings"""
        if not positions_by_account:
            self.logger.warning("No positions found. Run get_holdings() first.")
            return
        analysis_results = {}
        research = ResearchAnalysis()
        for account_type, positions in positions_by_account.items():
            self.logger.info(f"Analyzing performance for account: {account_type}")
            
            for position in positions:
                symbol = position.get('stock', {}).get('symbol')
                if not symbol:
                    continue
                    
                try:
                    # Add exchange suffix if needed
                    yf_symbol = self.get_symbol_with_exchange(symbol)
                    self.logger.info(f"Using symbol {yf_symbol} for Yahoo Finance")
                    
                    # Combine technical and research analysis
                    technical_analysis = self.technical_analysis(yf_symbol)
                    research_analysis = research.research_analysis(yf_symbol) #:TODO
                    # research_analysis = {"error": str(e)}
                    
                    # Store the combined analysis
                    if account_type not in analysis_results:
                        analysis_results[account_type] = {}
                        
                    analysis_results[account_type][symbol] = {
                        'position_data': position,
                        'technical_analysis': technical_analysis,
                        'research_analysis': research_analysis,
                        'summary': {"overall_recommendation": "BUY", "key_points": "TODO"} # TODO generateSummary()
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing {symbol}: {str(e)}")
            return analysis_results
    def technical_analysis(self, symbol):
        """Perform technical analysis on a symbol"""
        self.logger.info(f"Performing technical analysis for {symbol}")
        
        try:
            # Get historical data
            lookback_days = int(settings.LOOKBACK_PERIOD_DAYS)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)
            
            # Get data from Yahoo Finance
            stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if stock_data.empty:
                return {"error": "No historical data available"}
                
            # Calculate technical indicators
            results = {}
            
            # Simple Moving Averages (20, 50, 200 day)
            stock_data['SMA20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
            stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()
            
            # Fix for truth value of DataFrame is ambiguous error
            if len(stock_data) >= 20:  # Make sure we have enough data points for the SMA
                sma20_val = stock_data['SMA20'].iloc[-1]
                # Check if it's NaN
                if pd.isna(sma20_val):
                    sma20_val = None
            else:
                sma20_val = None
            if len(stock_data) >= 50:  # Make sure we have enough data points for the SMA
                sma50_val = stock_data['SMA50'].iloc[-1]
                # Check if it's NaN
                if pd.isna(sma50_val):
                    sma50_val = None
            else:
                sma50_val = None
            if len(stock_data) >= 200:  # Make sure we have enough data points for the SMA
                sma200_val = stock_data['SMA200'].iloc[-1]
                # Check if it's NaN
                if pd.isna(sma200_val):
                    sma200_val = None
            else:
                sma200_val = None
            current_price = stock_data['Close'].iloc[-1].values[0] if not stock_data['Close'].empty else None
            
            sma_trend = 'neutral'
            if sma20_val is not None and sma50_val is not None and current_price is not None:
                if sma20_val > sma50_val and current_price > sma20_val:
                    sma_trend = 'bullish'
                elif sma20_val < sma50_val and current_price < sma20_val:
                    sma_trend = 'bearish'
            
            results['sma'] = {
                'sma20': sma20_val,
                'sma50': sma50_val,
                'sma200': sma200_val,
                'price': current_price,
                'sma_trend': sma_trend
            }
            technical_indicators = TechnicalIndicators()
            # RSI (Relative Strength Index)
            rsi_value = technical_indicators.calculate_rsi(stock_data['Close'], window=14)
            if rsi_value is not None:
                rsi_value = rsi_value[0]
            rsi_signal = 'neutral'
            if rsi_value is not None:
                if rsi_value < 30:
                    rsi_signal = 'oversold'
                elif rsi_value > 70:
                    rsi_signal = 'overbought'
                    
            results['rsi'] = {
                'value': rsi_value,
                'signal': rsi_signal
            }
            
            # MACD (Moving Average Convergence Divergence)
            macd = technical_indicators.calculate_macd(stock_data)
            macd_line = macd['MACD'].iloc[-1] if not macd['MACD'].empty else None
            signal_line = macd['Signal'].iloc[-1] if not macd['Signal'].empty else None
            histogram = macd['Histogram'].iloc[-1] if not macd['Histogram'].empty else None
            
            macd_signal = 'neutral'
            if macd_line is not None and signal_line is not None:
                if macd_line > signal_line:
                    macd_signal = 'bullish'
                else:
                    macd_signal = 'bearish'
                    
            results['macd'] = {
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': histogram,
                'signal': macd_signal
            }
            
            # Bollinger Bands
            # Calculate the 20-period Simple Moving Average (SMA)
            stock_data['SMA'] = stock_data['Close'].rolling(window=20).mean()
            # Calculate the 20-period Standard Deviation (SD)
            stock_data['SD'] = stock_data['Close'].rolling(window=20).std()
            # Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
            stock_data['UB'] = stock_data['SMA'] + 2 * stock_data['SD']
            stock_data['LB'] = stock_data['SMA'] - 2 * stock_data['SD']
            bb_upper = stock_data['UB'].iloc[-1] if not stock_data['UB'].empty else None
            bb_middle = stock_data['SMA'].iloc[-1] if not stock_data['SMA'].empty else None
            bb_lower = stock_data['LB'].iloc[-1] if not stock_data['LB'].empty else None
            
            bb_signal = 'neutral'
            if current_price is not None and bb_upper is not None and bb_lower is not None:
                if current_price >= bb_upper:
                    bb_signal = 'upper_touch'
                elif current_price <= bb_lower:
                    bb_signal = 'lower_touch'
                    
            results['bollinger_bands'] = {
                'upper': bb_upper,
                'middle': bb_middle,
                'lower': bb_lower,
                'signal': bb_signal
            }
            
            # Calculate historical performance
            if len(stock_data) > 1:
                start_price = stock_data['Close'].iloc[0][0]
                current_price = stock_data['Close'].iloc[-1][0]
                perf_pct = ((current_price - start_price) / start_price) * 100 if start_price != 0 else 0
                
                results['performance'] = {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'start_price': start_price,
                    'current_price': current_price,
                    'percent_change': perf_pct,
                    'trend': 'up' if perf_pct > 0 else 'down'
                }
            
            # Calculate volatility (standard deviation of daily returns)
            if len(stock_data) > 1:
                daily_returns = stock_data['Close'].pct_change().dropna()
                results['volatility'] = {
                    'daily_std_dev': daily_returns.std() * 100 if not daily_returns.empty else None,  # as percentage
                    'annualized_volatility': daily_returns.std() * np.sqrt(252) * 100 if not daily_returns.empty else None  # annualized
                }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Technical analysis failed for {symbol}: {str(e)}")
            return {"error": str(e)}