"""
ML Models for Food Impact Calculator

    1. Training a regression model to predict food emissions
    2. Building a recommendation system using similarity scores
    3. Saving/loading trained models for reuse
"""

import pandas as pd
import numpy as np
import sqlite3
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt


# DATABASE CONNECTION
def load_data_from_db():
    """
    Load food data from SQLite database into a pandas DataFrame.
    
    Returns:
        DataFrame: All food records with emission breakdowns
    """
    connection = sqlite3.connect('food_impact.db')
    
    # SQL query to get all data
    query = "SELECT * FROM food"
    df = pd.read_sql_query(query, connection)
    connection.close()
    
    return df


# REGRESSION MODEL: PREDICT EMISSIONS
def train_regression_model(save_path='models/emission_predictor.pkl'):
    """
    Train a machine learning model to predict total_emissions from supply chain data.
    
    1. Load data from database
    2. Split into features (X) and target (y)
    3. Train a Random Forest Regressor
    4. Evaluate performance
    5. Save the trained model
    
    Args:
        save_path (str): Where to save the trained model
    
    Returns:
        dict: Contains the model, metrics, and feature importance
    """
    print("Starting model training...")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load data
    df = load_data_from_db()
    print(f"Loaded {len(df)} food items from database")
    
    # Define features these are the supply chain components
    feature_columns = [
        'land_use',      
        'animal_feed',   
        'farm',          
        'processing',    
        'transport',     
        'packaging',     
        'retail'         
    ]
    
    # Prepare X (features) and y (target)
    X = df[feature_columns]
    y = df['total_emissions']
    
    # Handle missing values by filling with 0
    # Some foods might not have all supply chain components
    X = X.fillna(0)
    y = y.fillna(0)
    
    # Split data: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # - n_estimators: Number of trees 
    # - max_depth: Maximum depth of each tree 
    # - random_state: For reproducibility
    model = RandomForestRegressor(
        n_estimators=100,    
        max_depth=10,        
        random_state=42      
    )
    
    print("Training Random Forest model...")
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics to evaluate model performance
    
    # R² Score (R-squared) measures how well the model fits the data
    # 0 to 1 (1 = perfect fit, 0 = no better than guessing the mean)
    # "What % of variance in emissions does the model explain?"
    r2 = r2_score(y_test, y_pred)
    
    # MAE Average absolute difference between predicted and actual
    # Units kg CO2e
    mae = mean_absolute_error(y_test, y_pred)
    
    # RMSE Square root of average squared errors
    # Units are Same as target (kg CO2e)
    # Penalizes large errors more than MAE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("\nMODEL PERFORMANCE METRICS")
    print("="*60)
    print(f"R² Score:  {r2:.4f}  (closer to 1 is better)")
    print(f"MAE:       {mae:.4f} kg CO2e  (lower is better)")
    print(f"RMSE:      {rmse:.4f} kg CO2e  (lower is better)")
    

    # Random Forest tells us which features are most important for predictions
    # This helps us understand which supply chain stages matter most
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("Feature Importance:")
    for _, row in feature_importance.iterrows():
        print(f"  {row['feature']:15s}: {row['importance']:.4f}")
    print()
    
    # joblib saves the trained model so we don't need to retrain it
    # Later, we can load it instantly and make predictions
    joblib.dump(model, save_path)
    print(f"Model saved to: {save_path}")
    
    # Return everything for further use
    return {
        'model': model,
        'r2': r2,
        'mae': mae,
        'rmse': rmse,
        'feature_importance': feature_importance,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred
    }


def predict_custom_food(land_use, animal_feed, farm, processing, 
                       transport, packaging, retail, 
                       model_path='models/emission_predictor.pkl'):
    """
    Predict total emissions for a custom food based on supply chain breakdown.
        
    Args:
        land_use (float): Emissions from land use change
        animal_feed (float): Emissions from animal feed
        farm (float): Emissions from farming
        processing (float): Emissions from processing
        transport (float): Emissions from transport
        packaging (float): Emissions from packaging
        retail (float): Emissions from retail
        model_path (str): Path to saved model
    
    Returns:
        float: Predicted total emissions in kg CO2e
    """
    # Load the pre-trained model
    model = joblib.load(model_path)
    
    # Create a feature array in the same order as training
    features = np.array([[land_use, animal_feed, farm, processing, 
                         transport, packaging, retail]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    return round(prediction, 2)


# RECOMMENDATION SYSTEM: SIMILARITY-BASED ALTERNATIVES
def build_food_similarity_matrix():
    """
    Build a similarity matrix showing how similar each food is to every other food. 
    Uses Cosine Similarity to compare emission profiles
    
    Returns:
        tuple: (similarity_matrix, food_dataframe)
    """
    # Load all foods from database
    df = load_data_from_db()
    
    # Features for similarity comparison
    # We use the same supply chain components
    feature_columns = [
        'land_use', 'animal_feed', 'farm', 'processing',
        'transport', 'packaging', 'retail'
    ]
    
    # Get emission profiles
    X = df[feature_columns].fillna(0)
    
    # Calculate cosine similarity between all pairs of foods
    # Result is a matrix where similarity_matrix[i][j] = similarity between food i and food j
    similarity_matrix = cosine_similarity(X)
    
    return similarity_matrix, df


def recommend_alternatives(food_id, top_n=5, max_emission_ratio=0.8):
    """
    Recommend lower-emission alternatives to a given food.
    
    1. Find foods with similar emission profiles (high cosine similarity)
    2. Filter to only show foods with LOWER emissions
    3. Sort by similarity score
    4. Return top N recommendations
    
    Args:
        food_id (int): ID of the food to find alternatives for
        top_n (int): Number of recommendations to return
        max_emission_ratio (float): Only show alternatives with emissions <= 0.8 (80% or less of original emissions)
    
    Returns:
        list: Recommended foods with similarity scores and emission reductions
    """
    # Build similarity matrix
    similarity_matrix, df = build_food_similarity_matrix()
    
    # Find the food in our database
    food_idx = df[df['id'] == food_id].index[0]
    food_name = df.iloc[food_idx]['food']
    food_emissions = df.iloc[food_idx]['total_emissions']
    
    # Get similarity scores for this food compared to all others
    similarity_scores = similarity_matrix[food_idx]
    
    # Create a DataFrame with all foods and their similarity to our target food
    recommendations = []
    
    for idx, score in enumerate(similarity_scores):
        # Skip the food itself (is 1.0)
        if idx == food_idx:
            continue
        
        alt_food = df.iloc[idx]
        alt_emissions = alt_food['total_emissions']
        
        # Only recommend foods with lower emissions
        if alt_emissions <= food_emissions * max_emission_ratio:
            emission_reduction = ((food_emissions - alt_emissions) / food_emissions) * 100
            
            recommendations.append({
                'id': int(alt_food['id']),
                'name': alt_food['food'],
                'similarity_score': round(score, 3),
                'emissions': round(alt_emissions, 2),
                'original_emissions': round(food_emissions, 2),
                'reduction_percent': round(emission_reduction, 1),
                'savings_kg': round(food_emissions - alt_emissions, 2)
            })
    
    # Sort by similarity score (highest first)
    recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    # Return top N recommendations
    return {
        'original_food': food_name,
        'original_emissions': round(food_emissions, 2),
        'alternatives': recommendations[:top_n]
    }


# VISUALIZATION HELPERS
def plot_predictions_vs_actual(results, save_path='models/prediction_plot.png'):
    """
    Create a scatter plot comparing predicted vs actual emissions.
    
    A perfect model would have all points on the diagonal line (predicted = actual).
    
    Args:
        results (dict): Output from train_regression_model()
        save_path (str): Where to save the plot
    """
    y_test = results['y_test']
    y_pred = results['y_pred']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    
    # Add diagonal line (perfect predictions)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    plt.xlabel('Actual Emissions (kg CO2e)', fontsize=12)
    plt.ylabel('Predicted Emissions (kg CO2e)', fontsize=12)
    plt.title(f'Model Predictions vs Actual Values\nR² = {results["r2"]:.3f}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"📈 Visualization saved to: {save_path}")
    plt.close()


# MAIN: RUN THIS TO TRAIN THE MODEL
if __name__ == '__main__':
    """
    Run this directly to train the model:
        python ml_models.py

    """
    print("MACHINE LEARNING MODEL TRAINING\n")
    
    # Train the regression model
    results = train_regression_model()
    
    # Create visualization
    plot_predictions_vs_actual(results)
    
    print("\nTESTING RECOMMENDATION SYSTEM\n")
    
    # Test recommendation system with a high-emission food for ID=1
    try:
        recs = recommend_alternatives(food_id=1, top_n=5)
        print(f"Original food: {recs['original_food']}")
        print(f"Emissions: {recs['original_emissions']} kg CO2e\n")
        print("Recommended lower-emission alternatives:")
        print("-" * 60)
        
        for i, alt in enumerate(recs['alternatives'], 1):
            print(f"{i}. {alt['name']}")
            print(f"   Similarity: {alt['similarity_score']:.3f} | "
                  f"Emissions: {alt['emissions']} kg CO2e | "
                  f"Saves: {alt['reduction_percent']}% ({alt['savings_kg']} kg)")
            print()
    except Exception as e:
        print(f"Note: Could not test recommendations yet: {e}")
        print("This is normal if database is empty. Run seed_db.py first!")
    
    print("Training complete! Model ready to use\n")