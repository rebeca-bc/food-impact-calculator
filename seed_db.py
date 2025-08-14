import pandas as pd
import sqlite3

# first read the csv
df = pd.read_csv('data/Food_Production.csv')

df.columns = df.columns.str.strip()

# maintain only relevant columns
columns_to_keep = [
    'Food product',
    'Land use change', 
    'Animal Feed', 
    'Farm', 
    'Processing',   
    'Transport', 
    'Packging', 
    'Retail', 
    'Total_emissions'
]

df2 = df[columns_to_keep].copy()

# Connect to (or create) SQLite DB
conn = sqlite3.connect('food_impact.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   
    food TEXT,                              
    land_use REAL,                          
    animal_feed REAL,
    farm REAL,
    processing REAL,
    transport REAL,
    packaging REAL,                        
    retail REAL,
    total_emissions REAL
)''')

# Insert data from DataFrame into the table
for _, row in df2.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO food (food, land_use, animal_feed, farm, processing, transport, packaging, retail, total_emissions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (row['Food product'], 
                              row['Land use change'], 
                              row['Animal Feed'], 
                              row['Farm'], 
                              row['Processing'], 
                              row['Transport'], 
                              row['Packging'], 
                              row['Retail'], 
                              row['Total_emissions']))

conn.commit()
conn.close()