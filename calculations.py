import sqlite3

# link to database, each on safe 
def db_connections():
    connection = sqlite3.connect('food_impact.db')
    return connection


# calulates the footprint per item in a list of dicts {food_id: n; food_name: name; qty_kg: x kgs}
# based on the food inputed and the quantity of it per week.
def calc_total_footprint(foods):

    # where to save the impact for each of the foods in the dict
    footprints = []
    total = 0

    # call for the safe db connection
    connection = db_connections()
    cur = connection.cursor()
    cur.execute('SELECT * FROM food')
    rows = cur.fetchall()  

    for food in foods:
        id = food['id']
        # amount of qty consumed per week in kgs
        qty = food['qty']
        qty = int(qty)
        qty /= 1000 

        # query database to get total emissions
        cur.execute("SELECT food, total_emissions FROM food WHERE id = ?", (id,))
        row = cur.fetchone()

        if row is None:
            raise ValueError(f"Food ID {id} not found in database")
   
        # devides the touple so it extracts the actual value
        food = row[0]
        total_emissions = row[1]

        # calculate the total emissions a week for this food
        total_per_food = total_emissions * qty
        total_per_food = round(total_per_food, 2)
        footprints.append({'food_id': id, 'food_name': food, 'week_emissions': total_per_food})

        # get the accumulated sum of the whole emissions
        total += total_per_food
    
    # append the total to the end of the footprints []
    total = round(total, 2)
    footprints.append(total)

    # close db connection
    connection.close()

    return footprints
