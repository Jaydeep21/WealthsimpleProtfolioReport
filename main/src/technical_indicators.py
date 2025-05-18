import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self):
        pass

    def calculate_rsi(self, prices, window=14):
        """
        Calculate the Relative Strength Index (RSI) for a given price series
        
        Parameters:
        prices (pandas.Series): Series of closing prices
        window (int): RSI lookback period
        
        Returns:
        float: The RSI value for the last period
        """
        # Get price changes
        delta = prices.diff().dropna()
        
        # Separate gains and losses
        gains = delta.copy()
        losses = delta.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)
        
        # Calculate average gains and losses
        avg_gain = gains.rolling(window=window).mean()
        avg_loss = losses.rolling(window=window).mean()
        
        # Calculate RS
        rs = avg_gain / avg_loss
        
        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))
        
        # Return the last RSI value
        return rsi.iloc[-1] if not rsi.empty else None
    

    # def calculate_ema(self, data, period, smoothing=2):
    #     """Calculate Exponential Moving Average."""
    #     ema = [sum(data[:period]) / period]  # Start with SMA
    #     multiplier = smoothing / (period + 1)
        
    #     for price in data[period:]:
    #         ema.append((price - ema[-1]) * multiplier + ema[-1])
        
    #     # Pad the beginning with NaNs to maintain the original data length
    #     return np.array([np.nan] * (len(data) - len(ema)) + ema)

    def calculate_macd(self, data, fast_period=12, slow_period=26, signal_period=9):
        # """
        # Calculate MACD, Signal Line, and Histogram
        
        # Parameters:
        # close_prices (array-like): Array of closing prices
        # fast_period (int): Period for the fast EMA (default: 12)
        # slow_period (int): Period for the slow EMA (default: 26)
        # signal_period (int): Period for the signal line EMA (default: 9)
        
        # Returns:
        # DataFrame with MACD, Signal, and Histogram columns
        # """
        # # Convert to numpy array if it's not already
        # prices = np.array(close_prices)
        
        # # Calculate EMAs
        # ema_fast = self.calculate_ema(prices, fast_period)
        # ema_slow = self.calculate_ema(prices, slow_period)
        
        # # Calculate MACD line
        # macd_line = ema_fast - ema_slow
        
        # # Calculate the signal line (9-day EMA of MACD line)
        # # We need to handle NaN values in the MACD line
        # valid_macd = macd_line[~np.isnan(macd_line)]
        # if len(valid_macd) >= signal_period:
        #     signal_line_valid = self.calculate_ema(valid_macd, signal_period)
        #     # Pad with NaNs to match the original array length
        #     signal_line = np.array([np.nan] * (len(macd_line) - len(signal_line_valid)) + list(signal_line_valid))
        # else:
        #     signal_line = np.full_like(macd_line, np.nan)
        
        # # Calculate histogram (MACD line - Signal line)
        # histogram = macd_line - signal_line
        
        data['ema12'] = data['Close'].ewm (span=12).mean()
        data['ema26'] = data['Close'].ewm(span=26).mean()
        data['macd'] = data['ema12'] - data['ema26']
        data['macd_signal'] = data['macd'].ewm(span=9).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']

        # Create DataFrame with results
        result = pd.DataFrame({
            'MACD': data['macd'],
            'Signal': data['macd_signal'],
            'Histogram': data['macd_histogram']
        })
        
        return result    