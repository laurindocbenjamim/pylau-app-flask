
import yfinance as yf
from app.dependencies import request, jsonify, Resource
from app.api.market.repository import get_historical_data

#@csrf_global.exempt # This Exclude views from protection
#@jwt_required()
class StockResource(Resource):
    
    def get(self):
        """def post(self):

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
        return jsonify(stocks)"""
        """
        Get stock data for specified symbols and period
        ---
        parameters:
        - name: symbols
            in: query
            type: string
            required: true
            description: Comma-separated stock symbols (e.g., AAPL,MSFT)
        - name: period
            in: query
            type: string
            enum: [1d, 5d, 1mo, 3mo, 6mo, 1y, ytd, max]
            default: 1mo
        """
        symbols = request.args.get('symbols', '').upper().split(',')
        period = request.args.get('period', '1mo')
        
        valid_periods = {'1d', '5d', '1mo', '3mo', '6mo', '1y', 'ytd', 'max'}
        if period not in valid_periods:
            return jsonify(error="Invalid period specified"), 400
        
        response_data = {}
        
        for symbol in symbols:
            if not symbol:
                continue
                
            stock_data = get_historical_data(symbol, period)
            if not stock_data:
                continue
                
            response_data[symbol] = stock_data
        
        if not response_data:
            return jsonify(error="No valid stock data found"), 404
            
        return jsonify(response_data)