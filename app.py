from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

class BudgetTracker:
    def __init__(self, filename='budget_data.json'):
        self.filename = filename
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                'income': [],
                'expenses': [],
                'categories': ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']
            }
    
    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)
    
    def add_income(self, amount, description, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        income_entry = {
            'amount': float(amount),
            'description': description,
            'date': date
        }
        self.data['income'].append(income_entry)
        self.save_data()
        return income_entry
    
    def add_expense(self, amount, category, description, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        expense_entry = {
            'amount': float(amount),
            'category': category,
            'description': description,
            'date': date
        }
        self.data['expenses'].append(expense_entry)
        self.save_data()
        return expense_entry
    
    def get_total_income(self):
        return sum(entry['amount'] for entry in self.data['income'])
    
    def get_total_expenses(self):
        return sum(entry['amount'] for entry in self.data['expenses'])
    
    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()
    
    def get_expenses_by_category(self):
        category_totals = {}
        for expense in self.data['expenses']:
            category = expense['category']
            amount = expense['amount']
            category_totals[category] = category_totals.get(category, 0) + amount
        return category_totals
    
    def get_categories(self):
        return self.data.get('categories', [])

app = Flask(__name__)
tracker = BudgetTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_income', methods=['POST'])
def add_income():
    try:
        data = request.json
        income = tracker.add_income(
            amount=data['amount'], 
            description=data['description']
        )
        return jsonify(income), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        expense = tracker.add_expense(
            amount=data['amount'], 
            category=data['category'], 
            description=data['description']
        )
        return jsonify(expense), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/summary')
def get_summary():
    return jsonify({
        'total_income': tracker.get_total_income(),
        'total_expenses': tracker.get_total_expenses(),
        'balance': tracker.get_balance(),
        'expenses_by_category': tracker.get_expenses_by_category()
    })

if __name__ == '__main__':
    app.run(debug=True)