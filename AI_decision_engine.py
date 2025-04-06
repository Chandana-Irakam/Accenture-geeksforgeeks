# ai/decision_engine.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class DecisionEngine:
    def __init__(self):
        # Load pre-trained models (in a real system, these would be trained separately)
        self.water_model = self._load_water_model()
        self.yield_model = self._load_yield_model()
        
    def _load_water_model(self):
        """Placeholder for water usage prediction model"""
        # In practice, this would load a pre-trained model
        return RandomForestRegressor()
        
    def _load_yield_model(self):
        """Placeholder for crop yield prediction model"""
        # In practice, this would load a pre-trained model
        return RandomForestRegressor()
        
    def generate_recommendations(self, farm_data, weather_data, soil_data, market_data):
        """Generates recommendations for the farmer"""
        recommendations = {
            'crops': [],
            'irrigation': {},
            'soil_health': {}
        }
        
        # 1. Crop recommendations
        if market_data:
            recommendations['crops'] = self._recommend_crops(
                farm_data, 
                soil_data, 
                weather_data, 
                market_data
            )
            
        # 2. Irrigation recommendations
        if weather_data and 'location' in farm_data:
            recommendations['irrigation'] = self._recommend_irrigation(
                farm_data['location'],
                soil_data.get('moisture', 0),
                weather_data
            )
            
        # 3. Soil health recommendations
        if soil_data:
            recommendations['soil_health'] = self._assess_soil_health(soil_data)
            
        return recommendations
        
    def _recommend_crops(self, farm_data, soil_data, weather_data, market_data):
        """Recommends crops based on multiple factors"""
        # Placeholder implementation - expand with real logic
        crops = [
            {
                'name': 'Wheat',
                'profit_per_hectare': 1200,
                'water_requirement': 500,
                'sustainability_score': 8.5,
                'market_trend': market_data.get('Wheat', {}).get('trend', 'stable')
            },
            {
                'name': 'Soybean',
                'profit_per_hectare': 1500,
                'water_requirement': 600,
                'sustainability_score': 7.8,
                'market_trend': market_data.get('Soybean', {}).get('trend', 'stable')
            },
            {
                'name': 'Millet',
                'profit_per_hectare': 900,
                'water_requirement': 300,
                'sustainability_score': 9.2,
                'market_trend': market_data.get('Millet', {}).get('trend', 'stable')
            }
        ]
        
        # Filter based on water availability
        water_budget = farm_data.get('water_budget', 1000)
        crops = [c for c in crops if c['water_requirement'] <= water_budget]
        
        # Sort by combined score (profit + sustainability)
        crops.sort(key=lambda x: (x['profit_per_hectare'] * 0.7 + x['sustainability_score'] * 30), reverse=True)
        
        return crops[:3]  # Return top 3 recommendations
        
    def _recommend_irrigation(self, location, soil_moisture, weather_data):
        """Recommends irrigation schedule"""
        # Simple logic - expand with more sophisticated rules
        recommendation = {
            'action': 'none',
            'amount': 0,
            'next_check': 'tomorrow'
        }
        
        if soil_moisture < 30:
            if not any('rain' in day.get('weather', [{}])[0].get('main', '').lower() 
                     for day in weather_data.get('daily', [])[:2]):
                recommendation['action'] = 'irrigate'
                recommendation['amount'] = min(50, 100 - soil_moisture)  # mm/m2
                
        return recommendation
        
    def _assess_soil_health(self, soil_data):
        """Assesses soil health and provides recommendations"""
        # Placeholder implementation
        recommendations = []
        
        if soil_data.get('organic_matter', 0) < 3:
            recommendations.append({
                'issue': 'Low organic matter',
                'recommendation': 'Add compost or organic fertilizer',
                'urgency': 'moderate'
            })
            
        if soil_data.get('ph', 7) < 6:
            recommendations.append({
                'issue': 'Acidic soil',
                'recommendation': 'Apply lime to raise pH',
                'urgency': 'high' if soil_data['ph'] < 5.5 else 'moderate'
            })
            
        return {
            'score': max(0, min(10, 
                soil_data.get('organic_matter', 0)/3 * 3 + 
                (1 - abs(soil_data.get('ph', 7) - 7)/2) * 4 +
                soil_data.get('microbial_activity', 5)/10 * 3
            ),
            'recommendations': recommendations
        }
