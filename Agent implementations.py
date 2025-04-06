# agents/farmer_agent.py

import sqlite3
from db.queries import save_farm_data, get_farm_data as db_get_farm_data

class FarmerAgent:
    def __init__(self):
        self.conn = sqlite3.connect('agrisync.db')
        
    def save_farm_data(self, farmer_id, soil_data, budget, crop_history):
        """Stores farmer data in the database"""
        try:
            save_farm_data(self.conn, farmer_id, soil_data, budget, crop_history)
            return True
        except Exception as e:
            print(f"Error saving farm data: {e}")
            return False
            
    def get_farm_data(self, farmer_id):
        """Retrieves farmer data from database"""
        return db_get_farm_data(self.conn, farmer_id)
        
    def get_soil_data(self, farmer_id):
        """Gets the latest soil data for a farmer"""
        data = db_get_farm_data(self.conn, farmer_id)
        return data.get('soil_data', {})
