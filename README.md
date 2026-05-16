# 💰 AI-Powered Expense Tracker (MCP Server)

An AI-compatible Expense Tracking System built using the **Model Context Protocol (MCP)** architecture with a modular tool-based design using **FastMCP**.

This project enables AI agents and LLM applications to manage expenses through MCP tools while supporting scalable async operations and cloud deployment.

---

# 🚀 Features

* Add, edit, and delete expenses
* Retrieve expenses with date filtering
* Expense summarization by category
* SQLite database integration
* Async database operations using `aiosqlite`
* MCP-compatible modular tool architecture
* Claude Desktop integration
* FastMCP Cloud deployment support
* AI Agent & LLM workflow integration

---

# 🧠 MCP Architecture Overview

This project follows the **Model Context Protocol (MCP)** pattern where:

* Every operation is exposed as an MCP tool
* AI agents can invoke tools directly
* Backend is designed for async non-blocking execution
* Easily extensible for future AI workflows

### Available MCP Tools

| Tool Name                        | Description                   |
| -------------------------------- | ----------------------------- |
| `add_expense`                    | Add a new expense             |
| `get_expenses`                   | Retrieve all expenses         |
| `get_expenses_within_date_range` | Fetch expenses between dates  |
| `edit_expense`                   | Update an existing expense    |
| `delete_expense`                 | Delete a specific expense     |
| `delete_all_expenses`            | Remove all expenses           |
| `summarize_expenses`             | Category-wise expense summary |
| `get_categories`                 | Retrieve available categories |

---

# ⚙️ Tech Stack

* **Language:** Python
* **Framework:** FastMCP
* **Database:** SQLite
* **Async Database Handling:** `aiosqlite`
* **Package Manager:** `uv`
* **Protocol:** MCP (Model Context Protocol)

---

# 📂 Project Structure

```bash
.
├── main.py               # MCP server entry point
├── categories.json       # Expense categories
├── expenses.db           # SQLite database
├── pyproject.toml        # Project dependencies
└── README.md
```

---

# 🛠️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker-mcp.git

cd expense-tracker-mcp
```

---

## 2️⃣ Install UV

```bash
pip install uv
```

---

## 3️⃣ Install FastMCP

```bash
uv add fastmcp
```

---

# ▶️ Running the MCP Server Locally

Run the MCP server locally using:

```bash
uv run fastmcp run main.py
```

---

# 🖥️ Install into Claude Desktop

To integrate the MCP server with Claude Desktop:

```bash
uv run fastmcp install claude-desktop main.py
```

After installation:

* Open Claude Desktop
* The MCP server tools will automatically become available
* Claude can directly invoke expense management tools

---

# ☁️ FastMCP Cloud Deployment

This project is also deployed on **FastMCP Cloud** using HTTP transport.

### Live MCP Endpoint

[Live server](https://expense-tracker-mcp-2405.fastmcp.app/mcp)

> Authentication is required to access the deployed endpoint.

---

# 🔄 Local vs Cloud Version

## Local Version

* Uses standard SQLite setup
* Suitable for local MCP integrations
* Runs directly through FastMCP CLI

## Cloud Version

The deployed cloud version includes additional improvements:

* Fully async implementation using `aiosqlite`
* HTTP transport support
* Temporary directory database handling for cloud write permissions
* Improved exception handling
* Production-ready async MCP tool execution

---

# 🤖 AI Agent Use Cases

This MCP server can be integrated with:

* Claude Desktop
* LangChain agents
* OpenAI Agents SDK
* Cursor AI
* MCP-compatible clients
* Custom AI automation systems

### Example AI Workflows

* “Add ₹500 spent on groceries”
* “Show expenses for this month”
* “Summarize food expenses”
* “Delete expense ID 4”

---

### Demo Video
[Youtube](https://youtu.be/cwKEmrP9Dd8)

---

# 📈 Future Enhancements

* Budget tracking system
* Credit and balance management
* AI-generated expense insights
* Natural language expense entry
* Charts & analytics dashboard
* Multi-user authentication
* PostgreSQL migration

---

# 👨‍💻 Author

## Vidya Sagar

* [GitHub Profile](https://github.com/vidyasagar2405?utm_source=chatgpt.com)
* [LinkedIn Profile](https://www.linkedin.com/in/vidya-sagar-a977672ab/?utm_source=chatgpt.com)
* [Portfolio](https://vidyasagar2405.github.io/Empelly-Vidya-Sagar-Portfolio/?utm_source=chatgpt.com)

---

# ⭐ Why This Project Matters

This project demonstrates:

* Real-world MCP architecture implementation
* AI-agent compatible backend engineering
* Async Python backend development
* Tool-oriented AI system design
* Cloud-deployable MCP infrastructure
* Production-oriented modular architecture

It is designed not just as an expense tracker, but as a foundational MCP system for AI-native applications.
