# 🌱 Food Impact Calculator

A personal project built with **Flask**, **Python**, **Pandas**, **Jinja**, **Chart.js**, **SQLite3**, **HTML**, **CSS**, and **JavaScript** to estimate the environmental impact of food consumption.

This application calculates **total greenhouse gas (GHG) emissions** based on user-submitted ingredients and quantities (in grams), and provides a breakdown of each item's percentage contribution to the total emissions.

---

## 📸 Preview

<img width="1440" height="776" alt="Screen Shot 2025-08-13 at 19 25 46" src="https://github.com/user-attachments/assets/54b23271-f27e-4506-bbf0-7456ff5a6a9e" />
<img width="1440" height="779" alt="Screen Shot 2025-08-13 at 19 19 54" src="https://github.com/user-attachments/assets/4164c441-bdd3-4599-a08e-627627c42ffa" />
<img width="1440" height="779" alt="Screen Shot 2025-08-13 at 19 20 10" src="https://github.com/user-attachments/assets/bf38e2ca-362b-4697-b59d-6fdb25ff67bd" />

---

## ✨ Features

- **Ingredient-based impact calculation**: Users select ingredients and quantities, and the app calculates their total emissions using real-world data from Kaggle.
- **Breakdown view**: See how much each food contributes to your weekly emissions (KG of C02) in both numbers and percentages.
- **Data visualization**: Interactive charts powered by **Chart.js** for better insight into consumption patterns.
- **CSV-based data**: Uses a preloaded dataset (cleaned and modified) to estimate impacts.

---

## 🛠 Tech Stack

**Backend**
- [Flask](https://flask.palletsprojects.com/)
- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [SQLite3](https://www.sqlite.org/)

**Frontend**
- [Chart.js](https://www.chartjs.org/)
- HTML5 / CSS3 / JavaScript
- [Bootstrap Icons](https://icons.getbootstrap.com/) for visual indicators
- Jinja2 for server-side templating

---

## 🚀 Installation & Setup

1. **Clone the repository**
git clone https://github.com/yourusername/food-impact.git
cd food-impact


2. **Create a virtual environment & activate it**
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate


3. **Install dependencies**
pip install -r requirements.txt


4. **Seed the database (optional if using SQLite sample)**
python seed_db.py


5. **Run the app**
flask run


6. **Open in your browser**
http://127.0.0.1:5000/

---

## 🔮 Future Development

This is an ongoing personal project and will be constantly updated. Planned features include:
- User authentication & registration
- Saving past results for progress tracking
- More chart types (bar charts, trends, comparisons)
- Interactive dashboards
- Enhanced UI/UX with animations and mobile optimization
- Expanded dataset for more food types
- Unit conversions (grams ↔ cups, tablespoons, etc.)
- Multi-language support

---

## 🤝 Contributing

This is currently a personal learning and portfolio project, but suggestions are welcome!
Feel free to open an issue or submit a pull request.
