# 🌱 Food Impact Calculator - AI-Powered Edition

A modern, machine learning-powered web application to calculate the environmental impact of your weekly food consumption with intelligent recommendations for lower-emission alternatives.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![ML](https://img.shields.io/badge/ML-Powered-blue)
![Design](https://img.shields.io/badge/Design-Modern-purple)

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
- Complete LCA from farm to retail
- Insights on:
  - Farm operations (methane, fertilizers)
  - Land use changes (deforestation)
  - Transportation emissions
  - Packaging impact
- Educational content debunking myths

### 🎨 **Modern UI/UX**
- Professional dark theme
- Responsive design (mobile/tablet/desktop)
- Smooth animations
- Gradient visualizations
- Print support

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
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
- **Inter Font** - Typography

### Machine Learning
- **Regression Model**: Predicts emissions from supply chain data
- **Recommendation Engine**: Finds similar, lower-emission alternatives
- **R² Score**: 0.9653 (96.5% accuracy)
- **MAE**: 0.86 kg CO₂e

## 📖 Documentation

### Getting Started
- **QUICK_START.md** - How to run the app
- **README.md** - This file

### ML & Implementation
- **ML_GUIDE.md** (10KB) - Learn ML concepts step-by-step
- **IMPLEMENTATION_SUMMARY.md** (10KB) - ML implementation details
- **ARCHITECTURE.md** (22KB) - System architecture diagrams

### Recent Updates
- **REDESIGN_SUMMARY.md** (13KB) - Complete UI/UX redesign details
- **VISUAL_GUIDE.md** (13KB) - Visual improvements explained
- **PROJECT_STATUS.md** (10KB) - Current project status
- **CHANGES_AT_A_GLANCE.txt** - Quick reference card

## 🎯 How It Works

### 1. User Input
Select foods and quantities from a database of 43 foods with complete emission data.

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

## 📊 Sample Results

```
Total Weekly Emissions: 52.3 kg CO₂e
Annual Impact: ~2.7 tons CO₂e

Breakdown:
1. Beef (500g)     → 49.74 kg CO₂e (95.2%)
2. Chicken (300g)  →  1.97 kg CO₂e (3.8%)
3. Rice (200g)     →  0.52 kg CO₂e (1.0%)

Recommendations for Beef:
→ Poultry Meat (95% similar) - Saves 80% (-39.87 kg)
→ Pork (89% similar) - Saves 75% (-37.44 kg)
```

## 🎨 Design Highlights

- **Modern Dark Theme**: Professional gradient backgrounds
- **Card-Based Layout**: Clean, organized sections
- **Responsive Grid**: Works on all devices
- **Smooth Animations**: Hover effects, transitions
- **Visual Hierarchy**: Clear information flow
- **Accessibility**: Semantic HTML, high contrast

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

## 🤝 Contributing

This is a learning project, but suggestions are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Data Source**: Kaggle - Food Production Emissions Dataset
- **ML Libraries**: scikit-learn
- **Visualization**: Chart.js
- **Icons**: Bootstrap Icons
- **Font**: Inter by Rasmus Andersson

## 📧 Contact

For questions or feedback, open an issue on GitHub.

---

**Made with 💚 for a sustainable future**
