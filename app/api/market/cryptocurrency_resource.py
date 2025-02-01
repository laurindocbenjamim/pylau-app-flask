

import yfinance as yf
from app.dependencies import request, current_app, jsonify, Resource
from app.api.upload_factory.file_upload import save_uploaded_file  # Import the file upload module
from app import csrf_global
from app.api.market.repository import get_historical_data

#@csrf_global.exempt # This Exclude views from protection
#@jwt_required()
class CryptoCurrencyResource(Resource):
    def post(self):

        symbols = ['AAPL', 'MSFT', 'NVDA']
        period = request.args.get('period', '1mo')
        
        stocks = {}
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            stocks[symbol] = {
                'current': stock.info['currentPrice'],
                'history': [{'date': date.strftime('%Y-%m-%d'), 'price': price} 
                        for date, price in zip(hist.index, hist['Close'])]
            }
        return jsonify(stocks)
    
    def get(self):
        """
        Get cryptocurrency data for specified coins and period
        ---
        parameters:
        - name: coins
            in: query
            type: string
            required: true
            description: Comma-separated crypto symbols (e.g., BTC-USD,ETH-USD)
        - name: period
            in: query
            type: string
            enum: [1d, 5d, 1mo, 3mo, 6mo, 1y, ytd, max]
            default: 1mo
        """
        coins = request.args.get('coins', '').upper().split(',')
        period = request.args.get('period', '1mo')
        
        valid_periods = {'1d', '5d', '1mo', '3mo', '6mo', '1y', 'ytd', 'max'}
        if period not in valid_periods:
            return jsonify(error="Invalid period specified"), 400
        
        response_data = {}
        
        for coin in coins:
            if not coin:
                continue
                
            crypto_data = get_historical_data(coin, period)
            if not crypto_data:
                continue
                
            # Add crypto-specific metrics
            ticker = yf.Ticker(coin)
            info = ticker.info
            crypto_data.update({
                'market_rank': info.get('marketCapRank', 'N/A'),
                'circulating_supply': info.get('circulatingSupply', 'N/A'),
                'total_supply': info.get('totalSupply', 'N/A'),
                'ath': info.get('regularMarketDayHigh', 'N/A'),
                'atl': info.get('fiftyTwoWeekLow', 'N/A')
            })
            
            response_data[coin] = crypto_data
        
        if not response_data:
            return jsonify(error="No valid crypto data found"), 404
            
        return jsonify(response_data)