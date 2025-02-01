from datetime import datetime, timedelta
import yfinance as yf
import cachetools
from flask import current_app

# Configure cache
data_cache = cachetools.TTLCache(maxsize=1000, ttl=300)

def get_historical_data(symbol, period):
    """
    Fetch historical market data for a given symbol and period
    Args:
        symbol (str): Stock/crypto symbol
        period (str): Time period (1d, 5d, 1mo, 6mo, 1y, ytd, max)
    Returns:
        dict: Formatted historical data
    """
    cache_key = f"{symbol}-{period}"
    if cache_key in data_cache:
        return data_cache[cache_key]
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
            
        info = ticker.info
        dividends = ticker.dividends.tail(4).to_dict()
        
        data = {
            'symbol': symbol,
            'currency': info.get('currency', 'USD'),
            'current_price': round(info.get('currentPrice', hist['Close'][-1]), 2),
            'previous_close': round(info.get('regularMarketPreviousClose', hist['Close'][-2]), 2),
            'price_change': round(info.get('regularMarketChange', hist['Close'][-1] - hist['Close'][-2]), 2),
            'change_percent': round(info.get('regularMarketChangePercent', 
                ((hist['Close'][-1] - hist['Close'][-2]) / hist['Close'][-2]) * 100), 2),
            'historical': [{
                'date': date.strftime('%Y-%m-%d'),
                'open': round(row['Open'], 2),
                'high': round(row['High'], 2),
                'low': round(row['Low'], 2),
                'close': round(row['Close'], 2),
                'volume': int(row['Volume'])
            } for date, row in hist.iterrows()],
            'meta': {
                'exchange': info.get('exchangeName', 'N/A'),
                'timezone': info.get('exchangeTimezoneName', 'UTC'),
                'market_cap': info.get('marketCap', 'N/A'),
                'dividends': [{'date': d.strftime('%Y-%m-%d'), 'amount': a} for d, a in dividends.items()],
                'last_updated': datetime.utcnow().isoformat()
            }
        }
        
        data_cache[cache_key] = data
        return data
        
    except Exception as e:
        current_app.logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return None