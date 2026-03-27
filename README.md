# 🌱 Food Impact Calculator - AI-Powered Edition

A modern, machine learning-powered web application to calculate the environmental impact of your weekly food consumption with intelligent recommendations for lower-emission alternatives.

## 📸 Preview

<img width="1440" height="853" alt="Screen Shot 2026-03-27 at 12 22 38" src="https://github.com/user-attachments/assets/8274e476-8f36-42d9-8d85-965d54b96857" />
<br>
<img width="1439" height="840" alt="Screen Shot 2026-03-27 at 12 23 53" src="https://github.com/user-attachments/assets/d84c6f73-1497-4cfa-9f08-7a695e27966c" />
<br>
<img width="1440" height="851" alt="Screen Shot 2026-03-27 at 12 24 28" src="https://github.com/user-attachments/assets/26270168-be56-4e85-967d-7435a8ebe46a" />


## ✨ Features

### 🧮 **Carbon Footprint Calculator**

- Input your weekly groceries (food type + quantity)
- Get total CO₂ emissions instantly
- See detailed breakdown by food item
- Visual charts and progress bars
- Impact badges (High/Medium/Low)
- Annual emissions projection

### 🤖 **AI-Powered Recommendations**

- Machine learning similarity algorithm (96.5% accuracy)
- Recommends lower-emission alternatives
- Shows similarity scores (how alike foods are)
- Displays emission savings (% and kg)
- Beautiful card-based interface

### 📊 **Life Cycle Analysis**

- LCA from farm to retail
- Insights on:
  - Farm operations (methane, fertilizers)
  - Land use changes (deforestation)
  - Transportation emissions
  - Packaging impact
- Educational content debunking myths

### 🎨 **Modern UI/UX**

- Dark + green theme (sustainability yet professional)
- Responsive design (mobile/tablet/desktop)
- Smooth animations
- Gradient visualizations
- Print support

## 🚀 Quick Start

```bash
# Clone the repository
git clone <https://github.com/rebeca-bc/food-impact-calculator.git>
cd food-impact-calculator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database
python3 seed_db.py

# Train the ML model
python3 ml_models.py

# Run the app
flask run

# Open browser
# http://127.0.0.1:5000/
```

## 🛠 Tech Stack

### Backend

- **Flask** - Web framework
- **Python 3** - Programming language
- **SQLite** - Database
- **Pandas** - Data manipulation
- **scikit-learn** - Machine learning
  - Random Forest Regressor
  - Cosine Similarity

### Frontend

- **HTML5/CSS3** - Structure & styling
- **JavaScript (ES6)** - Interactivity
- **Chart.js** - Data visualization
- **Bootstrap Icons** - Icons

### Machine Learning

- **Regression Model**: Predicts emissions from supply chain data
- **Recommendation Engine**: Finds similar, lower-emission alternatives
- **R² Score**: 0.9653 (96.5% accuracy)
- **MAE**: 0.86 kg CO₂e

## 🎯 How It Works

### 1. User Input

Select foods and quantities from a database of foods with complete emission data.

### 2. Calculation

Calculate total weekly emissions based on:

- Land use change
- Animal feed production
- Farm operations
- Processing
- Transportation
- Packaging
- Retail

### 3. ML Recommendations

AI analyzes your selections and recommends:

- Similar foods (using cosine similarity)
- Lower emissions (≤80% of original)
- Ranked by similarity score
- Shows potential savings

### 4. Visualization

Beautiful charts and insights to understand your impact.

## 📁 Project Structure

```
food-impact-calculator/
├── app.py                    # Flask application
├── ml_models.py              # ML training & recommendations
├── calculations.py           # Emission calculations
├── seed_db.py               # Database seeding
├── templates/
│   ├── layout.html          # Base template
│   ├── index.html           # Homepage
│   ├── estimates.html       # Results page
│   └── ml_predict.html      # ML predictor page
├── static/
│   ├── styles.css           # Modern CSS
│   └── main.js              # JavaScript
├── models/
│   ├── emission_predictor.pkl  # Trained model
│   └── prediction_plot.png     # Performance viz
├── data/
│   └── Food_Production.csv  # Raw data
└── food_impact.db           # SQLite database
```

## 🧠 Machine Learning Details

### Regression Model

- **Algorithm**: Random Forest Regressor
- **Features**: 7 supply chain stages
- **Target**: Total emissions
- **Performance**:
  - R² Score: 0.9653
  - MAE: 0.86 kg CO₂e
  - RMSE: 1.46 kg CO₂e

### Recommendation System

- **Algorithm**: Cosine Similarity
- **Approach**: Collaborative filtering
- **Criteria**:
  - High similarity (>0.8)
  - Lower emissions (≤80%)
  - Ranked by similarity

### Feature Importance

1. Farm Operations (48.76%)
2. Land Use Change (36.95%)
3. Processing (5.31%)
4. Animal Feed (5.18%)
5. Packaging (1.91%)
6. Transport (1.63%)
7. Retail (0.26%)

## 🙏 Acknowledgments

- **Data Source**: Kaggle - Food Production Emissions Dataset
- **ML Libraries**: scikit-learn
- **Visualization**: Chart.js

---

**Made with 💚 for a sustainable future**
