# bybit_auth.py

import time
import hmac
import hashlib
import logging
from urllib.parse import urlencode
from config import config_instance

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BybitAuth:
    def __init__(self):
        self.api_key = config_instance.get_bybit_api_key()
        self.api_secret = config_instance.get_bybit_secret_key()
        self.base_url = 'https://api.bybit.com'
        
    def _generate_signature(self, params: dict) -> tuple:
        """
        Generate signature for Bybit API request
        
        Args:
            params: Request parameters
            
        Returns:
            tuple: (timestamp, signature)
        """
        timestamp = str(int(time.time() * 1000))
        params['api_key'] = self.api_key
        params['timestamp'] = timestamp
        
        # Sort parameters by key
        sorted_params = dict(sorted(params.items()))
        
        # Create signature payload
        param_str = urlencode(sorted_params)
        signature = hmac.new(
            bytes(self.api_secret, 'utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return timestamp, signature
        
    def get_headers_and_params(self, params: dict = None) -> tuple:
        """
        Get headers and signed parameters for Bybit API request
        
        Args:
            params: Additional parameters for the request
            
        Returns:
            tuple: (headers, params)
        """
        if params is None:
            params = {}
            
        timestamp, signature = self._generate_signature(params)
        
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-SIGN-TYPE': '2',  # HMAC SHA256
        }
        
        return headers, params