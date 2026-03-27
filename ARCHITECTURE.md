# 🏗️ ML ARCHITECTURE OVERVIEW

## FEATURE FLOW EXAMPLES

📊 EXAMPLE 1: User calculates emissions
┌─────────────────────────────────────────────────┐
│ 1. User selects: Beef (500g), Rice (200g) │
│ 2. POST /estimates │
│ 3. calculations.py calculates total emissions │
│ 4. ml_models.py finds alternatives for Beef │
│ 5. Returns: Total + Recommendations │
│ │
│ Output: │
│ Total: 52.3 kg CO2e │
│ │
│ Recommendations for Beef: │
│ 🔄 Chicken (95% similar, saves 90%) │
│ 🔄 Pork (89% similar, saves 87%) │
└─────────────────────────────────────────────────┘

🧠 EXAMPLE 2: User predicts custom food
┌─────────────────────────────────────────────────┐
│ 1. User goes to /ml-predict │
│ 2. Inputs supply chain breakdown: │
│ land_use=2, farm=3, transport=0.5, ... │
│ 3. POST /api/predict │
│ 4. ml_models.py loads trained model │
│ 5. Model predicts: 6.8 kg CO2e │
│ 6. Returns prediction + breakdown chart │
└─────────────────────────────────────────────────┘

🔍 EXAMPLE 3: Developer uses API
┌─────────────────────────────────────────────────┐
│ 1. GET /api/recommend/5?top_n=3&max_ratio=0.7 │
│ 2. ml_models.py: │
│ • Loads food id=5 (e.g., Beef) │
│ • Calculates similarity with all foods │
│ • Filters: emissions ≤ 70% of Beef │
│ • Returns top 3 similar alternatives │
│ │
│ 3. Returns JSON with recommendations │
└─────────────────────────────────────────────────┘

## TECHNOLOGY STACK

**Backend**:
├── Flask → Web framework
├── SQLite3 → Database
├── Pandas → Data manipulation
├── NumPy → Numerical computing
├── scikit-learn → ML algorithms (Random Forest, cosine similarity)
└── joblib → Model persistence

**Frontend**:
├── HTML5/CSS3 → Structure and styling
├── JavaScript (ES6) → Interactivity
├── Chart.js → Visualizations
├── Bootstrap Icons → Icons
└── Jinja2 → Templating

**Machine Learning**:
├── Random Forest → Regression model
├── Cosine Similarity → Recommendation engine
├── Train/Test Split → Validation
└── Feature Importance → Insights
