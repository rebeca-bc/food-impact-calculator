from flask import Flask, jsonify, request, render_template
import sqlite3
import json
from calculations import calc_total_footprint

app = Flask(__name__, static_folder='static', template_folder='templates')

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
        contributions.append({'name': est['food_name'], 'contribution': contribution})

    # sort contributions by emissions
    contributions.sort(key=lambda x: x['contribution'], reverse=True)

    # send data for the charts 
    labels = [c['name'] for c in contributions]  
    emissions = [est['week_emissions'] for est in estimates[:-1]]
    percents = [c['contribution'] for c in contributions]  

    # rendes new page with results + charts 
    return render_template("estimates.html",  
                           total=total, 
                           contributions=contributions, 
                           labels=labels, 
                           percents=percents, 
                           emissions=emissions)

# do an endpoint on icon click for info and recs or replacements...

if __name__ == '__main__':
    app.run(debug=True)