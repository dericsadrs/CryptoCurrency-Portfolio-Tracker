# bybit_trade_history.py

import time
import requests
import logging
from services.bybit.bybit_auth import BybitAuth
import json

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BybitTradeHistory:
    def __init__(self):
        self.auth = BybitAuth()
        
    def get_trade_history(self, symbol: str = None, limit: int = 50) -> list:
        """
        Fetch trade execution history from Bybit API
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            limit: Number of records to fetch (default: 50, max: 100)
            
        Returns:
            list: List of trade executions
        """
        try:
            logger.info(f"Fetching Bybit trade history for {symbol}")
            endpoint = '/v5/execution/list'
            
            # Prepare parameters
            params = {
                'category': 'spot',
                'limit': min(limit, 100)  # Ensure limit doesn't exceed max
            }
            
            if symbol:
                params['symbol'] = symbol
                
            # Get authentication headers and signed params
            headers, signed_params = self.auth.get_headers_and_params(params)
            
            # Make request
            response = requests.get(
                f"{self.auth.base_url}{endpoint}",
                headers=headers,
                params=signed_params
            )
            
            if response.status_code != 200:
                logger.error(f"Error getting trade history. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return []
                
            data = response.json()
            
            # Check if response is successful
            if data['retCode'] != 0:
                logger.error(f"API error: {data['retMsg']}")
                return []
                
            # Pretty print response for debugging
            logger.debug(f"Response: {json.dumps(data, indent=4)}")
            
            return data.get('result', {}).get('list', [])
            
        except Exception as e:
            logger.error(f"An error occurred while fetching trade history: {str(e)}")
            return []
            
    def get_all_trades(self, symbols: list = None) -> list:
        """
        Fetch trade history for multiple symbols
        
        Args:
            symbols: List of trading pair symbols
            
        Returns:
            list: Combined list of trades
        """
        all_trades = []
        
        # If no symbols provided, get all trades
        if not symbols:
            return self.get_trade_history()
            
        for symbol in symbols:
            trades = self.get_trade_history(symbol)
            all_trades.extend(trades)
            time.sleep(0.1)  # Rate limiting
            
        return all_trades