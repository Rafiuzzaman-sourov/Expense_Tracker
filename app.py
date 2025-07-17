from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('expense.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if 'user_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Username and password required.")
            return redirect("/register")

        conn = get_db_connection()
        existing = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if existing:
            flash("Username already exists.")
            conn.close()
            return redirect("/register")

        hashed = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        flash("Registered successfully! Please log in.")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["hash"], password):
            flash("Invalid username or password.")
            return redirect("/login")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect("/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/login")

    conn = get_db_connection()

    # Filter parameters
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    filter_category = request.args.get("category", "")

    # Build query dynamically based on filters
    query = "SELECT * FROM expenses WHERE user_id = ?"
    params = [session["user_id"]]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if filter_category:
        query += " AND category = ?"
        params.append(filter_category)

    query += " ORDER BY date DESC"
    expenses = conn.execute(query, params).fetchall()

    # Fetch categories and sums for pie chart and filter dropdown
    category_data = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category",
        (session["user_id"],)
    ).fetchall()

    categories = [row['category'] for row in category_data]
    totals = [row['total'] for row in category_data]

    conn.close()

    return render_template("dashboard.html",
                           username=session.get("username"),
                           expenses=expenses,
                           categories=categories,
                           totals=totals,
                           start_date=start_date,
                           end_date=end_date,
                           filter_category=filter_category)


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"]

        if not amount or not category or not date:
            flash("Amount, Category, and Date are required fields.")
            return redirect("/add-expense")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], amount, category, date, note)
        )
        conn.commit()
        conn.close()
        flash("Expense added successfully.")
        return redirect("/dashboard")

    return render_template("add_expense.html")


@app.route("/delete-expense/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, session["user_id"]))
    conn.commit()
    conn.close()
    flash("Expense deleted successfully.")
    return redirect("/dashboard")

@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    expense = conn.execute("SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, session["user_id"])).fetchone()

    if expense is None:
        conn.close()
        flash("Expense not found.")
        return redirect("/dashboard")

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"]

        if not amount or not category or not date:
            flash("All fields except note are required.")
            return redirect(f"/edit-expense/{expense_id}")

        conn.execute(
            "UPDATE expenses SET amount = ?, category = ?, date = ?, note = ? WHERE id = ? AND user_id = ?",
            (amount, category, date, note, expense_id, session["user_id"])
        )
        conn.commit()
        conn.close()
        flash("Expense updated successfully.")
        return redirect("/dashboard")

    conn.close()
    return render_template("edit_expense.html", expense=expense)


if __name__ == "__main__":
    app.run(debug=True)
