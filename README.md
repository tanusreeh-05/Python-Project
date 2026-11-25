# Expense Tracker – Personal Finance Management System

## Overview

The Expense Tracker is a Python-based demonstration application for personal finance management, designed to showcase basic financial management functionalities such as income monitoring, expense tracking, category-wise budget allocation, and financial report generation.

The application uses JSON-based file handling to store financial records, ensuring that transaction history, salary information, and budget configurations remain available between application sessions.

## Features

-  Salary Management:  Set, view, and update monthly salary or income.
-  Income Tracking:  Record additional income with relevant categories, dates, and descriptions.
-  Expense Tracking:  Record and organize expenses across predefined categories.
-  Transaction History:  View all recorded income and expense transactions.
-  Edit Transactions:  Modify existing transaction amounts and descriptions.
-  Delete Transactions:  Remove previously recorded transactions.
-  Budget Management:  Establish individual spending limits for different expense categories.
-  Budget Alerts:  Receive notifications when a new expense exceeds the allocated category budget.
-  Search and Filter:  Search transactions using category selection or keywords in descriptions.
-  Financial Reports:  Generate financial summaries displaying total income, total expenses, remaining balance, savings percentage, and category-wise expenditure.
-  Persistent Data Storage:  Automatically save and retrieve financial information using JSON files.

## Expense Categories

The application supports the following predefined categories:
```
1. Food
2. Clothes
3. Entertainment
4. Shopping
5. Grocery
6. Bills
7. Health
8. Education
9. Travel
10. Gas/Petrol
```

## Technologies Used

 Programming Language 
- Python 3

 Data Storage 
- JSON

 Python Standard Libraries 
- `json` – JSON data serialization and deserialization.
- `os` – File and directory operations.
- `sys` – Application termination and system-level operations.
- `datetime` – Date handling and validation.

No external Python packages are required.

## Project Structure
```
Expense-Tracker/
│
├── expense-tracker.py
├── expense_data.json
└── README.md
```

`expense-tracker.py` :  Main application containing the program logic and functionalities.
`expense_data.json` : Stores transaction records, budget configurations, and salary information. 
`README.md` : Documentation describing the project. 

## Installation and Execution

### Prerequisites

- Python 3.x installed on the system.
- A code editor or terminal to execute the application.

### Setup Instructions

 Step 1: Clone the Repository 

git clone <repository-url>

 Step 2: Navigate to the Project Directory 

cd Expense-Tracker

 Step 3: Execute the Application 

python expense-tracker.py

 Step 4: Initialize the Application 

On the first execution, the application prompts the user to enter their monthly salary or income. Users can then access the available functionalities through the interactive menu.

## Application Menu

The application provides the following menu options:

  1   Update / View Salary 
  2   Add Income / Salary Addition  
  3   Add Expense Transaction  
  4   View Transaction History  
  5   Edit Transaction  
  6   Delete Transaction  
  7   Set Category Budgets  
  8   Search and Filter Transactions  
  9   Generate Financial Reports and Summary  
  10   Exit Application  

## Data Management

The application uses a JSON file named `expense_data.json` for persistent data storage.

The file maintains three primary components:

-  Transactions:  Stores transaction IDs, types, categories, amounts, dates, and descriptions.
-  Budgets:  Maintains individual budget limits for each predefined category.
-  Salary:  Stores the user's monthly salary or income.

The application automatically loads previously stored information during initialization and updates the JSON file whenever financial records are modified.

## Programming Concepts Implemented

This project demonstrates the practical implementation of the following Python programming concepts:

- Functions and modular programming
- Lists and dictionaries
- File handling and data persistence
- JSON serialization and deserialization
- Exception handling
- Conditional statements and loops
- Input validation
- Date and time handling
- Financial calculations and data processing

## Future Scope

The application can be further enhanced with the following features:

- Graphical User Interface (GUI).
- Interactive charts and financial visualizations.
- Monthly and yearly financial reports.
- Cloud-based data storage.
- User authentication and account management.
- Web-based accessibility.

## Project Objective

The primary objective of this project is to develop a functional personal finance management system using Python. It aims to simplify income and expense tracking while demonstrating fundamental programming concepts, file handling, data management, and problem-solving techniques.
