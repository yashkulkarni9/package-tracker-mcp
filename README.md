# 📦 Package Tracker - MCP Server

A local, AI-enhanced **Package Tracking Assistant** that allows users to manage their incoming deliveries via a conversational interface using Claude and the Model Context Protocol (MCP). This lightweight Python server is designed to simulate real-world delivery tracking and provides intelligent summaries, overdue alerts, and manual status updates — all through Claude's natural language interface.

---

## 🚀 What This Project Does

- Tracks packages manually by name, courier, and tracking number
- Supports optional **ETA (Estimated Delivery Date)** for accurate tracking
- Automatically **checks for overdue deliveries**
- Allows users to **manually update delivery status**
- Generates a **summary prompt** that Claude can use to suggest next steps
- Uses Claude’s **MCP** integration for interaction through natural prompts

---

## 🌟 Why This Is Useful

- Perfect for those who receive packages from many sources (e.g., online sellers, postal mail, offline couriers)
- Simulates delivery stages and makes tracking more transparent
- Can be extended for enterprise internal tracking or college mailrooms
- No third-party integration needed — secure, private, and offline

---

## 🛠️ Tools & Technologies

- Python 3.9+
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Claude by Anthropic (supports MCP)
- Local JSON file-based data storage (`packages.json`)

---

## 🧪 How to Run This Project Locally

### 📥 1. Clone the GitHub Repository


- git clone https://github.com/yashkulkarni9/package-tracker-mcp.git
- cd package-tracker-mcp

### 2. (Optional) Create and Activate a Virtual Environment
- On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

- On Windows:
python -m venv .venv 
.venv\Scripts\activate

### 📦 3. Install the MCP CLI Tool
- Ensure you're using Python 3.9+

- Then run:
pip install mcp[cli]

- If you're using uv:
uv pip install mcp[cli]



### ▶️ 4. Install & Register the MCP Server
- Inside the project root directory, run:
mcp install main.py

- This registers your MCP server with Claude so it can be accessed from Claude's Developer Tools.

### 💬 5. Use the Server in Claude
- Download and open Claude Desktop

- Go to: Your Profile → Settings → Developer

- You’ll see the Package Tracker MCP Server listed under available tools

- You can now chat with it using natural prompts like:

- Add a package Shoes from Amazon with tracking number AMZ123 and ETA 2024-04-20

- List all packages

- Update the status of tracking number AMZ123 to Delivered

- Check if I have any overdue deliveries

- Give me a delivery summary
