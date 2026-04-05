from fastmcp import FastMCP
import os
import sqlite3
from typing import Any, Optional

## define the path to the SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

## path to resources
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

## creating a new instance of FastMCP
mcp = FastMCP("ExpenseTracker")

## Initialize the database and create the expenses table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                  CREATE TABLE IF NOT EXISTS expenses(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL,
                  subcategory TEXT NOT NULL,
                  note TEXT DEFAULT ''
                  )
                  """
        )


## initializing the database
init_db()


## tools for adding the expenses
@mcp.tool("add_expense")
def add_expense(date :str, amount :float, category : str, subcategory :str, note: str= "") -> dict[str,Any]:
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("""
                  INSERT INTO expenses (date, amount, category, subcategory, note)
                  VALUES (?, ?, ?, ?, ?)
                  """, (date, amount, category, subcategory, note)
        )
        return {"status": "success", "expense_id": cur.lastrowid}
    

## tool for retrieving all expenses
@mcp.tool("get_expenses")
def get_expenses():
    """Retrieve all expenses from the database."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    

## listing expenses within a specific date range
@mcp.tool("get_expenses_within_date_range")
def date_range_expenses(start_date :str, end_date :str):
    '''Expenses between a date range'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("""
                 SELECT * FROM expenses
                 WHERE date BETWEEN ? AND ?
                 ORDER BY id ASC """,
                 (start_date, end_date)
        )
                 
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    

## tool for deleting all expenses
@mcp.tool("delete_all_expenses")
def delete_expenses():
    """Deleting the expenses from the database"""
    with sqlite3.connect(DB_PATH) as c:
        c.execute("DELETE FROM expenses")
        return {"status": "success", "message": "All expenses have been deleted."}
    

## tool for deleting a specific expense by id
@mcp.tool("delete_expense")
def delete_expense(expense_id: int):
    """Delete a specific expense from the database."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": "Expense not found."}
        return {"status": "success", "message": f"Expense with id {expense_id} has been deleted."}


## tool for editing an existing expense
@mcp.tool("edit_expense")
def edit_expense(expense_id: int, date: str , amount: float, category: str , subcategory: str , note: str) -> dict[str, Any]:
    """Edit an existing expense in the database."""
    with sqlite3.connect(DB_PATH) as c:
        ## Fetch the existing expense and update 
        cur = c.execute("""
                        UPDATE expenses
                        SET date = ?, amount = ?, category = ?, subcategory = ?, note = ?
                        WHERE id = ?
                        """, (date, amount, category, subcategory, note, expense_id)
        )
        if cur.rowcount == 0:
            return {"status": "error", "message": "Expense not found."}
        return {"status": "success", "messsage": f"Expense with id {expense_id} has been updated."}
    


## tool for summarizing expenses by category within a date range
@mcp.tool("summarize_expenses")
def summarize_expenses(start_date :str, end_date :str, category : Optional[str]= None):
    """summarize the expenses with in a date range with inclusive of category"""
    with sqlite3.connect(DB_PATH) as c:
        query = """
                 SELECT category, SUM(amount) as total
                 FROM expenses
                 WHERE date BETWEEN ? AND ?
                 """
        params = [start_date, end_date]
        
        if category:
            query += """ AND category = ?"""
            params.append(category)

        query += " GROUP BY category ORDER BY total ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


# adding a tool as a resource for the client to access the categories and subcategories
@mcp.tool("get_categories")
def get_categories():
    """Return the list of categories and subcategories from the JSON file."""
    with open(CATEGORIES_PATH, 'r') as f:
        return f.read()

## adding resource for the client to access the categories and subcategories
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """Return the list of categories and subcategories from the JSON file."""
    with open(CATEGORIES_PATH, 'r') as f:
        return f.read()


## starting the server
if __name__ == "__main__":
    mcp.run(transport = "http", host = "0.0.0.0", port = 8000)
    
