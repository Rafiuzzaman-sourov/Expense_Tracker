# Expense Tracker

## Project Overview
Expense Tracker is a simple and efficient web application to help users monitor and manage their daily expenses. Users can add, edit, and delete expenses, categorize them, and view summaries to better understand their spending habits.

---

## Features
- User registration and login
- Add new expenses with details like amount, category, date, and description
- Edit and delete existing expenses
- View expenses in a list or table format
- Summary dashboard with total expenses and category-wise breakdown
- Responsive design for mobile and desktop
- Secure authentication and session management

---

## Technologies Used
- **Backend:** Python Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Authentication:** Flask-Login or custom session management

---

## Installation and Setup

1. **Clone the repository**


git clone https://github.com/yourusername/expense-tracker.git

cd expense-tracker
Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run the application
flask run
Access the app
Open your browser and go to http://localhost:5000




2. **Usage**

Register a new account or log in if you already have one.
Add your expenses by filling out the form with amount, category, date, and description.
View your expenses and monitor your spending habits.
Edit or delete expenses as needed.
Use the dashboard to see summaries and analytics of your expenses.

3. **Project Structure**
```bash
expense-tracker/
│
├── app.py                # Main Flask application
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── expenses.html
├── static/               # CSS, JS, images
│
├── models.py             # Database models
├── requirements.txt      # Python dependencies
└── README.md             # This file
```
4. **Contributing**

Contributions are welcome! Please fork the repo and submit a pull request for any improvements or bug fixes.

5. **License**

This project is licensed under the MIT License.

6. **Contact**
Created by Md.Rafiuzzaman Sowrov — feel free to reach out via email at rafiuzzamansourov@gmail.com or connect on Linkedin with https://www.linkedin.com/in/rafiuzzaman-sourov-715b78279/
