# app.py - Main entry point for the GreenSynth system

from flask import Flask, jsonify
from agents.farmer_agent import FarmerAgent
from agents.weather_agent import WeatherAgent
from agents.market_agent import MarketAgent
from ai.decision_engine import DecisionEngine
import sqlite3
from db.models import init_db

app = Flask(__name__)

# Initialize database
init_db()

# Initialize agents
farmer_agent = FarmerAgent()
weather_agent = WeatherAgent()
market_agent = MarketAgent()
decision_engine = DecisionEngine()

@app.route('/api/recommendations/<int:farmer_id>', methods=['GET'])
def get_recommendations(farmer_id):
    """Endpoint to get farming recommendations for a specific farmer"""
    try:
        # Get farmer data
        farm_data = farmer_agent.get_farm_data(farmer_id)
        
        # Get environmental data
        weather_data = weather_agent.get_weather_forecast(farm_data['location'])
        soil_data = farmer_agent.get_soil_data(farmer_id)
        
        # Get market data
        market_data = market_agent.get_market_trends(farm_data['crop_types'])
        
        # Generate recommendations
        recommendations = decision_engine.generate_recommendations(
            farm_data, 
            weather_data, 
            soil_data, 
            market_data
        )
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
