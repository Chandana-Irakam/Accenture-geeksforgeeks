# agents/market_agent.py

import requests
import pandas as pd
from datetime import datetime

class MarketAgent:
    def __init__(self):
        self.usda_api = "https://api.usda.gov/data"
        self.cache = {}
        
    def get_market_trends(self, crop_types, days=30):
        """Gets market trends for specified crop types"""
        trends = {}
        for crop in crop_types:
            if crop in self.cache:
                # Use cached data if not expired
                cached_data, timestamp = self.cache[crop]
                if (datetime.now() - timestamp).days < 1:
                    trends[crop] = cached_data
                    continue
                    
            # Fetch fresh data
            try:
                params = {
                    'commodity_desc': crop,
                    'format': 'json',
                    'api_key': 'your_usda_key'
                }
                response = requests.get(f"{self.usda_api}/psd", params=params)
                response.raise_for_status()
                data = response.json()
                
                # Process with pandas
                df = pd.DataFrame(data['results'])
                df['report_date'] = pd.to_datetime(df['report_date'])
                df = df.sort_values('report_date').tail(days)
                
                trends[crop] = {
                    'current_price': df['price'].iloc[-1],
                    'trend': 'up' if df['price'].iloc[-1] > df['price'].iloc[0] else 'down',
                    'volatility': df['price'].std()
                }
                
                # Update cache
                self.cache[crop] = (trends[crop], datetime.now())
                
            except Exception as e:
                print(f"Error fetching market data for {crop}: {e}")
                trends[crop] = None
                
        return trends
