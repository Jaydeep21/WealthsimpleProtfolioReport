class TechnicalIndicators:
    def __init__(self, data):
        self.data = data

    def calculate_rsi(prices, window=14):
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