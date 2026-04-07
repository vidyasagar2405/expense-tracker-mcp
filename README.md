# 💰 AI-Powered Expense Tracker (MCP Server)

An AI-compatible expense tracking system built using MCP (Model Context Protocol) architecture with modular tool-based design. This project enables efficient expense management and is designed to integrate seamlessly with AI agents and LLM workflows.

---

## 🚀 Features

- Add, update, and delete expenses
- Categorize transactions
- Async database operations using `aiosqlite`
- Modular MCP tool-based architecture
- Designed for AI agent integration
- Scalable and extensible backend design

---

## 🧠 Architecture Overview

This project follows an MCP (Model Context Protocol) pattern where:

- Each operation (add/edit/delete expense) is implemented as a **tool**
- Tools are exposed to AI agents for automated interaction
- Backend is designed for **non-blocking async execution**

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Framework:** FastMCP  
- **Database:** SQLite  
- **Async Handling:** aiosqlite  

---

## 📂 Project Structure

```

.
├── main.py              # MCP server entry point
├── categories.json     # Expense categories
├── expenses.db        # SQLite database
├── pyproject.toml     # Dependencies
└── README.md

````

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/expense-tracker-mcp.git

cd expense-tracker-mcp

# Install dependencies
pip install .
````

---

## ▶️ Running the Server

```bash
python main.py
```

---

## 🔗 MCP Server Endpoint

The server is deployed and accessible via:

```
https://expense-tracker-mcp-2405.fastmcp.app/mcp
```

> Note: Authentication is required to access the endpoint.

---

## 🤖 Use Case with AI Agents

This system is designed to be used by AI agents where:

* Agents can call tools to manage expenses
* Enables automation of financial tracking
* Can be integrated into LLM workflows (LangChain, etc.)

---

## 📈 Future Enhancements

* Budget tracking system
* Credit & balance management
* AI-based expense insights and analytics
* Natural language expense input via LLM

---

## 👤 Author

**Vidya Sagar**
Navigate to:
    [GitHub Profile](https://github.com/vidyasagar2405)
    [LinkedIn Profile](https://www.linkedin.com/in/vidya-sagar-a977672ab)
    [Portfolio](https://vidyasagar2405.github.io/Empelly-Vidya-Sagar-Portfolio/)

---