import json
import os
import sys
from datetime import datetime

DATA_FILE = "expense_data.json"

DEFAULT_BUDGETS = {
    "Food": 0.0,
    "Clothes": 0.0,
    "Entertainment": 0.0,
    "Shopping": 0.0,
    "Grocery": 0.0,
    "Bills": 0.0,
    "Health": 0.0,
    "Education": 0.0,
    "Travel": 0.0,
    "Gas/Petrol": 0.0,
}

CATEGORIES = list(DEFAULT_BUDGETS.keys())

state = {
    "transactions": [],
    "budgets": dict(DEFAULT_BUDGETS),
    "salary": 0.0,
}


def load_data():
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        state["transactions"] = data.get("transactions", [])
        merged_budgets = dict(DEFAULT_BUDGETS)
        merged_budgets.update(data.get("budgets", {}))
        state["budgets"] = merged_budgets
        state["salary"] = float(data.get("salary", 0.0))
        print("Previous data loaded successfully from file!")
    except Exception as e:
        print(f"Error loading data file: {e}")


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"Error saving data file: {e}")


def prompt_float(prompt, allow_zero=True, allow_empty=False, default=None):
    while True:
        raw = input(prompt).strip()
        if allow_empty and raw == "":
            return default
        try:
            val = float(raw)
            if val != val or val in (float("inf"), float("-inf")):
                print("Please enter a valid finite number.")
                continue
            if val < 0 or (not allow_zero and val == 0):
                print("Amount must be positive." if not allow_zero else "Amount cannot be negative.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a numeric value.")


def get_category_choice():
    print("\n===== CATEGORIES =====")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}. {cat}")
    print(f"{len(CATEGORIES) + 1}. Cancel / Back")

    cancel_idx = str(len(CATEGORIES) + 1)
    cat_lookup = {cat.lower(): cat for cat in CATEGORIES}

    while True:
        choice = input("\nEnter category name or number: ").strip().lower()
        if choice in ("exit", cancel_idx):
            return None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx]
        if choice in cat_lookup:
            return cat_lookup[choice]
        print("Invalid Category! Please try again.")


def print_transactions_table(items):
    if not items:
        print("\nNo matching transactions found.")
        return
    print("\n" + "=" * 81)
    print(f"{'ID':<4} | {'Type':<8} | {'Category':<16} | {'Amount':<12} | {'Date':<10} | {'Description'}")
    print("=" * 81)
    for t in items:
        amt_str = f"₹{t['amount']:.2f}"
        print(f"{t['id']:<4} | {t['type']:<8} | {t['category']:<16} | {amt_str:<12} | {t['date']:<10} | {t['description']}")
    print("=" * 81)


def initialize_salary():
    if state["salary"] > 0:
        print(f"\nCurrent Active Salary / Income: ₹{state['salary']:.2f}")
        if input("Do you want to update it? (y/n): ").strip().lower() != "y":
            return

    print("\n===== EXPENSE TRACKER SETUP =====")
    state["salary"] = prompt_float("Enter Initial Monthly Salary / Income: ₹")
    save_data()
    print("Salary updated successfully!")


def add_transaction_flow(trans_type):
    category = get_category_choice()
    if not category:
        return

    amount = prompt_float(f"Enter {category} {trans_type} Amount: ₹", allow_zero=False)

    while True:
        date_str = input("Enter Date (YYYY-MM-DD) [Leave blank for today]: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")

    description = input("Enter Description / Notes: ").strip() or "N/A"

    if trans_type == "Expense":
        spent = sum(
            t["amount"]
            for t in state["transactions"]
            if t["type"] == "Expense" and t["category"] == category
        )
        budget = state["budgets"][category]
        if budget > 0 and (spent + amount) > budget:
            print(f"Warning: This expense exceeds your budget for {category} (Budget: ₹{budget:.2f})!")

    next_id = max((t["id"] for t in state["transactions"]), default=0) + 1
    state["transactions"].append({
        "id": next_id,
        "type": trans_type,
        "category": category,
        "amount": amount,
        "date": date_str,
        "description": description,
    })
    save_data()
    print(f"Success! {trans_type} of ₹{amount:.2f} added under [{category}].")


def find_transaction_by_id(prompt_text):
    txns = state["transactions"]
    if not txns:
        print("\nNo transactions recorded yet.")
        return None
    print_transactions_table(txns)
    try:
        tid = int(input(prompt_text).strip())
    except ValueError:
        print("Invalid ID.")
        return None
    target = next((t for t in txns if t["id"] == tid), None)
    if not target:
        print("Transaction ID not found.")
    return target


def edit_transaction():
    target = find_transaction_by_id("\nEnter Transaction ID to edit: ")
    if not target:
        return

    print(f"Editing Transaction #{target['id']} [{target['category']} - ₹{target['amount']:.2f}]")
    target["amount"] = prompt_float(
        f"Enter new amount [press Enter to keep ₹{target['amount']:.2f}]: ",
        allow_zero=False,
        allow_empty=True,
        default=target["amount"],
    )
    new_desc = input(f"Enter new description [press Enter to keep '{target['description']}']: ").strip()
    if new_desc:
        target["description"] = new_desc

    save_data()
    print("Transaction updated successfully!")


def delete_transaction():
    target = find_transaction_by_id("\nEnter Transaction ID to delete: ")
    if not target:
        return
    state["transactions"].remove(target)
    save_data()
    print("Transaction deleted successfully!")


def manage_budgets():
    print("\n===== SET CATEGORY BUDGETS =====")
    category = get_category_choice()
    if not category:
        return
    budget_amt = prompt_float(f"Enter monthly budget limit for {category}: ₹")
    state["budgets"][category] = budget_amt
    save_data()
    print(f"Budget for {category} set to ₹{budget_amt:.2f}")


def search_and_filter():
    if not state["transactions"]:
        print("\nNo transactions recorded yet.")
        return

    print("\n--- SEARCH & FILTER ---")
    print("1. Filter by Category")
    print("2. Search by Keyword in Description")
    choice = input("Enter choice (1-2): ").strip()

    if choice == "1":
        cat = get_category_choice()
        if not cat:
            return
        results = [t for t in state["transactions"] if t["category"] == cat]
    elif choice == "2":
        kw = input("Enter search keyword: ").strip().lower()
        results = [t for t in state["transactions"] if kw in t["description"].lower()]
    else:
        print("Invalid choice.")
        return

    print_transactions_table(results)


def generate_reports():
    txns = state["transactions"]
    total_income = state["salary"] + sum(t["amount"] for t in txns if t["type"] == "Income")
    total_expense = sum(t["amount"] for t in txns if t["type"] == "Expense")
    remaining_balance = total_income - total_expense

    print("\n" + "=" * 30 + " FINANCIAL REPORT " + "=" * 30)
    print(f"Total Income / Salary   : ₹{total_income:.2f}")
    print(f"Total Expenses          : ₹{total_expense:.2f}")
    print(f"Remaining Balance       : ₹{remaining_balance:.2f}")

    if total_income > 0:
        spent_pct = (total_expense / total_income) * 100
        print(f"Total Income Spent      : {spent_pct:.2f}%")
        print(f"Total Income Saved      : {100 - spent_pct:.2f}%")

    print("\n--- Category-wise Breakdown & Budget Status ---")
    print(f"{'Category':<16} | {'Spent':<12} | {'Budget':<12} | {'Remaining Budget':<16} | {'% of Income'}")
    print("-" * 81)

    for cat in CATEGORIES:
        cat_spent = sum(t["amount"] for t in txns if t["type"] == "Expense" and t["category"] == cat)
        cat_budget = state["budgets"][cat]
        pct = (cat_spent / total_income * 100) if total_income > 0 else 0.0

        spent_str = f"₹{cat_spent:.2f}"
        if cat_budget > 0:
            budget_str = f"₹{cat_budget:.2f}"
            rem_str = f"₹{cat_budget - cat_spent:.2f}"
        else:
            budget_str = "Not Set"
            rem_str = "N/A"

        print(f"{cat:<16} | {spent_str:<12} | {budget_str:<12} | {rem_str:<16} | {pct:.2f}%")
    print("=" * 81)


def main():
    load_data()
    if state["salary"] == 0.0:
        initialize_salary()

    menu_actions = {
        "1": initialize_salary,
        "2": lambda: add_transaction_flow("Income"),
        "3": lambda: add_transaction_flow("Expense"),
        "4": lambda: print_transactions_table(state["transactions"]),
        "5": edit_transaction,
        "6": delete_transaction,
        "7": manage_budgets,
        "8": search_and_filter,
        "9": generate_reports,
    }

    while True:
        print("\n================ MAIN MENU ================")
        print("1. Update / View Salary")
        print("2. Add Income / Salary Addition")
        print("3. Add Expense Transaction")
        print("4. View Transaction History")
        print("5. Edit Transaction")
        print("6. Delete Transaction")
        print("7. Set Category Budgets")
        print("8. Search & Filter Transactions")
        print("9. Generate Financial Reports & Summary")
        print("10. Exit Application")

        choice = input("\nEnter your choice (1-10): ").strip()
        if choice == "10" or choice.lower() == "exit":
            print("\nThank you for using Expense Tracker!")
            sys.exit(0)

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid Choice! Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()