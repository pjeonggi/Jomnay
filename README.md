
# Jomnay: Expense Tracking System

Jomnay is a simple expense tracking system developed to help users manage their daily spending and monthly budget. It allows users to record expenses, review transaction history, and monitor their monthly allowance. The system also provides smart alerts and spending analysis to support better financial decisions.

## Key Features

- Member Access: Users can create accounts and log in to manage their personal expense data.
- Monthly Allowance: Calculates a monthly spending limit for each month.
- Add Expense: Record spending with date and category.
- Expense History: View all previous expense transactions.
- Smart Alerts: Sends Telegram alerts when spending is close to or exceeds the monthly limit.
- File Exporter: Export all expense records into a file.
- Spending Trends: Compare spending between the current month and the previous month.
- Savings Goal Planner: Tracks the remaining budget and adds it to savings.

## Project Setup

### Prerequisites

Before running the project, make sure you have:

- Python 3 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pjeonggi/Jomnay.git
cd Jomnay
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

To start the program, run:

```bash
python main.py
```

## Required Dependencies

The project uses the following Python libraries:

- pandas – for data handling and analysis
- requests – for API communication and Telegram alerts
- python-telegram-bot – for sending Telegram notifications
- reportlab – for file export and report generation

You can install them with:

```bash
pip install -r requirements.txt
```

## Project Structure 

The project follows a modular Object-Oriented Programming (OOP) design.

| Directory/File                  | Purpose                | Key Files            |
| ------------------------------- | ---------------------- | -------------------- |
| 📁`src/`                      | Core application logic | Main system features |
| ├── 📄`main.py`            | Entry point            | Runs the program     |
| ├── 📄`expense_tracker.py` | Expense handling       | Core feature         |
| ├── 📄`member_access.py`   | User management        | Login system         |
| ├── 📄`saving_plan.py`     | Savings tracking       | Budget leftover      |
| ├── 📄`smart_alert.py`     | Alert system           | Telegram API         |
| ├── 📄`spendingTrend.py`   | Trend analysis         | Monthly comparison   |
| ├── 📄`fileExporter.py`    | Export reports         | PDF/CSV              |
| 📁`data/`                     | Input data storage     | CSV files            |
| 📁`reportPDF/`                | Output reports         | Generated files      |
| 📄`requirements.txt`          | Dependencies           | Python libraries     |
| 📄`README.md`                 | Documentation          | Project info         |

## Contribution

Prepared by: Nin Ponharoth, Kong Leak Smey, Sitha Viyalin, Bet Sreypich

Course: Object-Oriented Programming (Python)

Lecturer: Mr. Han Leangsiv

Department: Computer Science, Specializing in Data Science, Cambodia Academy of Digital Technology (CADT)
