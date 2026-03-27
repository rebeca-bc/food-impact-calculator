from flask import Flask, jsonify, request, render_template
import sqlite3
import json
from calculations import calc_total_footprint
# Import ML functions for predictions and recommendations
from ml_models import predict_custom_food, recommend_alternatives

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_impact_comparison(annual_tons):
    """
    Converts annual CO2 emissions to relatable real-world comparisons.
    Helps users understand what their food choices mean in practical terms.
    
    Examples:
    - Car miles driven
    - Tree equivalents needed to offset
    - Smartphone charges
    """
    # Reference values (approximate)
    # 1 ton CO2 ≈ 2,500 miles driven in average car
    # 1 ton CO2 ≈ 40 trees needed to absorb per year
    # 1 ton CO2 ≈ 121,000 smartphone charges
    # 1 ton CO2 ≈ 4,000 km flown
    
    car_miles = int(annual_tons * 2500)
    trees_needed = int(annual_tons * 40)
    phone_charges = int(annual_tons * 121000)
    flight_km = int(annual_tons * 4000)
    
    comparisons = []
    
    if car_miles > 0:
        comparisons.append({
            'icon': 'car-front',
            'value': f'{car_miles:,}',
            'unit': 'miles',
            'description': 'driven in an average car'
        })
    
    if trees_needed > 0:
        comparisons.append({
            'icon': 'tree',
            'value': f'{trees_needed}',
            'unit': 'trees',
            'description': 'needed to offset this annually'
        })
    
    if annual_tons >= 0.1:  # Only show for meaningful amounts
        comparisons.append({
            'icon': 'airplane',
            'value': f'{flight_km:,}',
            'unit': 'km',
            'description': 'of air travel'
        })
    
    if phone_charges > 1000:
        comparisons.append({
            'icon': 'phone',
            'value': f'{phone_charges:,}',
            'unit': 'charges',
            'description': 'of a smartphone'
        })
    
    return comparisons

def db_connections():
    connection = sqlite3.connect('food_impact.db')
    cur = connection.cursor()
    return cur

@app.route('/')
def index():
    cur = db_connections()
    cur.execute('SELECT id, food FROM food')
    items = cur.fetchall()
    # send all the items for the dropdown...
    return render_template('index.html', items=items)


@app.route('/ml-predict')
def ml_predict_page():
    """
    Page for ML-powered custom food emission prediction.
    
    Users can input supply chain breakdown for foods not in the database,
    and the ML model will predict total emissions.
    """
    # Get count of foods in database for display
    cur = db_connections()
    cur.execute('SELECT COUNT(*) FROM food')
    food_count = cur.fetchone()[0]
    
    return render_template('ml_predict.html', food_count=food_count)

@app.route('/api/add', methods=["POST"])
def add_item():
    data = request.get_json()

    # sends none if the id wasnt sent correctly, good option
    id = data.get("foodId")
    food = data.get("foodName")
    qty = data.get("quantity")
    
    # return jason with the data
    return jsonify({
        "id": id, 
        "food": food,
        "qty": qty
    })

@app.route("/estimates", methods=["POST"])
def total_estimate():
    foods_json = request.form.get("foods")
    if not foods_json:
        return "No food data received", 400
    # changes the json to python dict that calculations.py recieves 
    foods = json.loads(foods_json)

    estimates = calc_total_footprint(foods)

    # get the contribution % per food and save in contributions
    total = estimates[-1]
    contributions = []

    # dont get to the last element, because is the total
    for est in estimates[:-1]:
        item_emissions = est['week_emissions']
        contribution = item_emissions * 100 / total
        contributions.append({
            'name': est['food_name'], 
            'contribution': contribution,
            'emissions': item_emissions  # ADD EMISSIONS HERE!
        })

    # sort contributions by emissions (highest first)
    contributions.sort(key=lambda x: x['contribution'], reverse=True)

    # send data for the charts - NOW ALL IN SYNC!
    labels = [c['name'] for c in contributions]  
    emissions = [c['emissions'] for c in contributions]  # NOW SORTED!
    percents = [c['contribution'] for c in contributions]  

    # Get ML recommendations for each food in the list
    # This finds lower-emission alternatives for foods the user selected
    all_recommendations = {}
    for est in estimates[:-1]:  # Exclude the total
        food_id = est['food_id']
        try:
            # Get recommendations for this specific food
            recs = recommend_alternatives(food_id, top_n=3, max_emission_ratio=0.8)
            all_recommendations[food_id] = recs['alternatives']
        except Exception as e:
            # If recommendations fail for this food, just skip it
            print(f"Could not get recommendations for food {food_id}: {e}")
            all_recommendations[food_id] = []
    
    # Calculate annual emissions and get real-world comparisons
    annual_tons = (total * 52) / 1000  # Weekly to annual, kg to tons
    impact_comparisons = get_impact_comparison(annual_tons)
    
    # rendes new page with results + charts + ML recommendations + impact comparisons
    return render_template("estimates.html",  
                           total=total, 
                           contributions=contributions, 
                           labels=labels, 
                           percents=percents, 
                           emissions=emissions,
                           recommendations=all_recommendations,
                           estimates=estimates[:-1],  # Send food details for recommendations
                           annual_tons=annual_tons,
                           impact_comparisons=impact_comparisons)


# ML API ENDPOINTS
@app.route('/api/predict', methods=["POST"])
def predict_emissions():
    """
    ML Endpoint: Predict emissions for a custom food (not in db)
    
    This uses the trained regression model to estimate total emissions
    based on supply chain breakdown.
    
    Returns:
    {
        "predicted_emissions": 6.2,
        "unit": "kg CO2e"
    }
    """
    data = request.get_json()
    
    # Validate that all required fields are present
    required_fields = ['land_use', 'animal_feed', 'farm', 'processing', 
                      'transport', 'packaging', 'retail']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Make prediction using the ML model
        prediction = predict_custom_food(
            land_use=float(data['land_use']),
            animal_feed=float(data['animal_feed']),
            farm=float(data['farm']),
            processing=float(data['processing']),
            transport=float(data['transport']),
            packaging=float(data['packaging']),
            retail=float(data['retail'])
        )
        
        return jsonify({
            'predicted_emissions': prediction,
            'unit': 'kg CO2e per kg of product',
            'note': 'This is an ML prediction based on similar foods in our database'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommend/<int:food_id>', methods=["GET"])
def get_recommendations(food_id):
    """
    ML Endpoint to get lower-emission alternatives for a specific food.
    
    This uses cosine similarity to find foods with similar emission patterns
    but lower total emissions.
    
    URL ex: /api/recommend/5
    Optional query params:
        - top_n: Number of recommendations (default: 5)
        - max_ratio: Maximum emission ratio (default: 0.8 = 80%)
    
    Returns:
    {
        "original_food": "Beef (beef herd)",
        "original_emissions": 99.48,
        "alternatives": [
            {
                "id": 12,
                "name": "Poultry Meat",
                "similarity_score": 0.856,
                "emissions": 9.87,
                "reduction_percent": 90.1,
                "savings_kg": 89.61
            },
            ...
        ]
    }
    """
    # Get optional query parameters
    top_n = request.args.get('top_n', 5, type=int)
    max_ratio = request.args.get('max_ratio', 0.8, type=float)
    
    try:
        # Get recommendations using the ML similarity engine
        recommendations = recommend_alternatives(
            food_id=food_id,
            top_n=top_n,
            max_emission_ratio=max_ratio
        )
        
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)