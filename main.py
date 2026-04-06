from fastmcp import FastMCP
import os
import aiosqlite
import tempfile
from typing import Any, Optional

## use temparary directory for the database to ensure write permissions
TEMP_DIR = tempfile.gettempdir()
## define the path to database
DB_PATH = os.path.join(TEMP_DIR, "expenses.db")
## path to resources
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")


## creating a new instance of FastMCP with the name "ExpenseTracker"
mcp = FastMCP("ExpenseTracker")


## Initialize the database and create the expenses table if it doesn't exist
def init_db():
    try:
        ## use synchronous sqlite3 for initialization to ensure the database is set up before any async operations
        import sqlite3
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
            ## test write access to the database
            c.execute("INSERT OR IGNORE INTO expenses(date, amount, category) VALUES('2000-01-01', 0, 'test')")
            c.execute("DELETE FROM expenses WHERE category = 'test'")
            print("Database initialized successfully with write access")


    except Exception as e:
        print(f"Database initialization error: {e}")
        raise


## initializing the database
init_db()


## tools for adding the expenses
@mcp.tool("add_expense")
async def add_expense(date :str, amount :float, category : str, subcategory :str, note: str= "") -> dict[str,Any]:
    """Add a new expense to the database."""
    try:
        async with aiosqlite.connect(DB_PATH) as c: ## Changed: added async
            cur = await c.execute(  ## Changed: added await
                """INSERT INTO expenses (date, amount, category, subcategory, note)
                    VALUES (?, ?, ?, ?, ?)
                    """, (date, amount, category, subcategory, note))
            await c.commit() ## Changed: added await
            return {"status": "success", "expense_id": cur.lastrowid, "message": "Expense added successfully"}
    except Exception as e:  ## Changed: Simplified exception handling.
        if "readonly" in str(e).lower():
            return {"status": "error", "message": "Database is in read-only mode. Check file permissions."}
        return {"status": "error", "message": f"Failed to add expense: {e}"}
    

## tool for retrieving all expenses
@mcp.tool("get_expenses")
async def get_expenses(): ## Changed: added async 
    """Retrieve all expenses from the database."""
    try:
        async with aiosqlite.connect(DB_PATH) as c: ## Changed: added async
            cur = await c.execute("SELECT * FROM expenses ORDER BY id ASC") ## Changed: added await
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in await cur.fetchall()] ## Changed: added await
    except Exception as e: ## handling exceptions and returning error message
        return {"status": "error", "message": f"Failed to retrieve expenses: {e}"}
        

## listing expenses within a specific date range
@mcp.tool("get_expenses_within_date_range")
async def date_range_expenses(start_date :str, end_date :str): ## Changed: added async
    '''Expenses between a date range'''
    try:
        async with aiosqlite.connect(DB_PATH) as c: ## Changed: added async
            cur = await c.execute(
                """ SELECT * FROM expenses
                    WHERE date BETWEEN ? AND ?
                    ORDER BY id ASC """,
                    (start_date, end_date)
            )
                    
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in await cur.fetchall()] ## Changed: added await
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to retrieve expenses: {e}"}
        

## tool for deleting all expenses
@mcp.tool("delete_all_expenses")
async def delete_expenses(): ## Changed: added async
    """Deleting the expenses from the database"""
    try:
        async with aiosqlite.connect(DB_PATH) as c: ## Changed: added async
            await c.execute("DELETE FROM expenses") ## Changed: added await
            return {"status": "success", "message": "All expenses have been deleted."}
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to delete expenses: {e}"}
    

## tool for deleting a specific expense by id
@mcp.tool("delete_expense")
async def delete_expense(expense_id: int): # Changed: added async
    """Delete a specific expense from the database."""
    try:
        async with aiosqlite.connect(DB_PATH) as c: # Changed: added async
            cur = await c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,)) # Changed: added await
            if cur.rowcount == 0:
                return {"status": "error", "message": "Expense not found."}
            return {"status": "success", "message": f"Expense with id {expense_id} has been deleted."}
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to delete expense: {e}"}


## tool for editing an existing expense
@mcp.tool("edit_expense")
async def edit_expense(expense_id: int, date: str , amount: float, 
                       category: str , subcategory: str , note: str) -> dict[str, Any]: ## Changed: added async
    """Edit an existing expense in the database."""
    try:
        async with aiosqlite.connect(DB_PATH) as c: ## Changed: added async
            ## Fetch the existing expense and update 
            cur = await c.execute(  ## Changed: added await
                """ UPDATE expenses
                    SET date = ?, amount = ?, category = ?, subcategory = ?, note = ?
                    WHERE id = ?
                    """, (date, amount, category, subcategory, note, expense_id)
            )
            if cur.rowcount == 0:
                return {"status": "error", "message": "Expense not found."}
            return {"status": "success", "messsage": f"Expense with id {expense_id} has been updated."}
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to edit expense: {e}"}
    


## tool for summarizing expenses by category within a date range
@mcp.tool("summarize_expenses")
async def summarize_expenses(start_date :str, end_date :str, category : Optional[str]= None): ## changed: 
    """summarize the expenses with in a date range with inclusive of category"""
    try:
        async with aiosqlite.connect(DB_PATH) as c:
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

            cur = await c.execute(query, params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in await cur.fetchall()]
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to summarize expenses: {e}"}



## adding resource for the client to access the categories and subcategories
@mcp.resource("expense:///categories", mime_type="application/json")
def categories():
    """Return the list of categories and subcategories from the JSON file."""
    try:
        # Provide default categories if file doesn't exist
        default_categories = {
            "categories": [
                "Food & Dining",
                "Transportation",
                "Shopping",
                "Entertainment",
                "Bills & Utilities",
                "Healthcare",
                "Travel",
                "Education",
                "Business",
                "Other"
            ]
        }
        try:
            with open(CATEGORIES_PATH, 'r') as f:
                return f.read()
        except FileNotFoundError:
            import json
            return json.dumps(default_categories, indent = 2)
    except Exception as e: ## handling exceptions.
        return {"status": "error", "message": f"Failed to load categories: {e}"}


if __name__ == "__main__":
    mcp.run(transport = "http", host = "0.0.0.0", port = 8000)
