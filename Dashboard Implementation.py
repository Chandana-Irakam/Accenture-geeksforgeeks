# dashboard/app.py

from flask import Flask, render_template, request, jsonify
from agrisync.agents.farmer_agent import FarmerAgent
from agrisync.agents.weather_agent import WeatherAgent
from agrisync.agents.market_agent import MarketAgent
from agrisync.ai.decision_engine import DecisionEngine

app = Flask(__name__)

# Initialize components
farmer_agent = FarmerAgent()
weather_agent = WeatherAgent()
market_agent = MarketAgent()
decision_engine = DecisionEngine()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/farm-data', methods=['POST'])
def update_farm_data():
    data = request.json
    farmer_id = data.get('farmer_id')
    
    try:
        farmer_agent.save_farm_data(
            farmer_id,
            data.get('soil_data', {}),
            data.get('water_budget', 0),
            data.get('crop_history', [])
        )
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/recommendations/<int:farmer_id>')
def get_recommendations(farmer_id):
    try:
        farm_data = farmer_agent.get_farm_data(farmer_id)
        if not farm_data:
            return jsonify({'status': 'error', 'message': 'Farm not found'}), 404
            
        weather_data = weather_agent.get_weather_forecast(farm_data['location'])
        market_data = market_agent.get_market_trends(
            farm_data.get('crop_history', []) or ['Wheat', 'Soybean', 'Millet']
        )
        
        recommendations = decision_engine.generate_recommendations(
            farm_data,
            weather_data,
            farm_data.get('soil_data', {}),
            market_data
        )
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
