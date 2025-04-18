from mcp.server.fastmcp import FastMCP
import os, json
from datetime import datetime

mcp = FastMCP("Package Tracker")

PACKAGES_FILE = os.path.join(os.path.dirname(__file__), "packages.json")

def load_packages():
    if not os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, "w") as f:
            json.dump([], f)
    try:
        with open(PACKAGES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(PACKAGES_FILE, "w") as f:
            json.dump([], f)
        return []

def save_packages(packages):
    with open(PACKAGES_FILE, "w") as f:
        json.dump(packages, f, indent=2)

@mcp.tool()
def add_package(name: str, courier: str, tracking_number: str, eta: str = "") -> str:
    """
    Add a package to track. Optional ETA format: YYYY-MM-DD
    """
    packages = load_packages()

    package = {
        "name": name,
        "courier": courier,
        "tracking_number": tracking_number,
        "status": "Not yet shipped",
        "last_updated": datetime.now().isoformat()
    }

    if eta:
        try:
            datetime.strptime(eta, "%Y-%m-%d")  # Validate format
            package["eta"] = eta
        except ValueError:
            return "Invalid ETA format. Use YYYY-MM-DD."

    packages.append(package)
    save_packages(packages)
    return f"Added package '{name}' with tracking number '{tracking_number}'" + (f" and ETA {eta}" if eta else ".")

@mcp.tool()
def update_status(tracking_number: str, new_status: str) -> str:
    """
    Update the delivery status of a package.
    """
    packages = load_packages()
    for pkg in packages:
        if pkg["tracking_number"] == tracking_number:
            pkg["status"] = new_status
            pkg["last_updated"] = datetime.now().isoformat()
            save_packages(packages)
            return f"Status updated to '{new_status}' for '{pkg['name']}'."
    return "Package not found."

@mcp.tool()
def list_all_packages() -> str:
    """
    List all packages with their current status.
    """
    packages = load_packages()
    if not packages:
        return "No packages found."
    return "\n".join([
        f"- {p['name']} ({p['courier']}) — {p['status']} (Last update: {p['last_updated'].split('T')[0]})"
        + (f", ETA: {p['eta']}" if "eta" in p else "")
        for p in packages
    ])

@mcp.tool()
def check_overdue_packages() -> str:
    """
    Check for packages that are overdue based on ETA.
    """
    packages = load_packages()
    today = datetime.now().date()
    overdue = []

    for p in packages:
        if p.get("eta") and p["status"].lower() != "delivered":
            try:
                eta_date = datetime.strptime(p["eta"], "%Y-%m-%d").date()
                if eta_date < today:
                    overdue.append(f"- {p['name']} ({p['courier']}) was due on {p['eta']}")
            except ValueError:
                continue  # Skip malformed ETA

    if not overdue:
        return "No overdue packages found."
    return "Overdue packages:\n" + "\n".join(overdue)

@mcp.resource("packages://delivered")
def delivered_packages() -> str:
    """
    Show all delivered packages.
    """
    packages = load_packages()
    delivered = [p for p in packages if p["status"].lower() == "delivered"]
    if not delivered:
        return "No packages delivered yet."
    return "\n".join([f"- {p['name']} ({p['courier']})" for p in delivered])

@mcp.prompt()
def delivery_summary_prompt() -> str:
    """
    Generate a summary of all packages and ask if any are delayed or need follow-up.
    """
    packages = load_packages()
    if not packages:
        return "There are no packages being tracked currently."

    summary = "\n".join([
        f"{p['name']} ({p['courier']}): {p['status']}" + (f", ETA: {p['eta']}" if "eta" in p else "")
        for p in packages
    ])
    return f"Here are my packages and their statuses:\n{summary}\n\nAre any of these delayed or need follow-up?"
