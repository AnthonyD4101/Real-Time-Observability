import time, os
from dotenv import load_dotenv
from pymongo import MongoClient
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box

load_dotenv()

database_url = os.getenv("DATABASE_URL")
client = MongoClient(database_url)

try:
    client.admin.command('ping')
    print("Successful connection to MongoDB")
except Exception as e:
    print(e)

db = client.get_database("FastAPI")

exploration_collection = db.get_collection("ExplorationKPI")
financial_collection = db.get_collection("FinancialKPI")
health_collection = db.get_collection("HealthKPI")


def get_exploration_kpi():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_drilling_success_rate": {"$avg": "$drilling_success_rate"},
                "avg_machine_downtime": {"$avg": "$avg_machine_downtime"},
                "avg_operational_efficiency": {"$avg": "$avg_operational_efficiency"},
            }
        }
    ]
    result = list(exploration_collection.aggregate(pipeline))
    return result[0] if result else None

def get_financial_kpi():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_revenue_growth_rate": {"$avg": "$avg_revenue_growth_rate"},
                "avg_net_income_ratio": {"$avg": "$avg_net_income_ratio"},
            }
        }
    ]
    result = list(financial_collection.aggregate(pipeline))
    return result[0] if result else None

def get_health_kpi():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_lost_time_incident_rate": {"$avg": "$avg_lost_time_incident_rate"},
                "avg_environmental_compliance_rate": {"$avg": "$avg_environmental_compliance_rate"},
            }
        }
    ]
    result = list(health_collection.aggregate(pipeline))
    return result[0] if result else None

def colorize(value, good_threshold, bad_threshold, higher_is_better=True):
    if higher_is_better:
        if value > good_threshold:
            return f"[green]{value:.2f}[/green]"
        elif value < bad_threshold:
            return f"[red]{value:.2f}[/red]"
    else:
        if value < good_threshold:
            return f"[green]{value:.2f}[/green]"
        elif value > bad_threshold:
            return f"[red]{value:.2f}[/red]"
    return f"[yellow]{value:.2f}[/yellow]"

def create_kpi_table(exploration_kpi, financial_kpi, health_kpi):
    table = Table(title="KPI Metrics Dashboard", box = box.ROUNDED)

    table.add_column("Exploration KPIs", justify="center", style="cyan", no_wrap=True)
    table.add_column("Value", justify="center")
    table.add_column("Financial KPIs", justify="center", style="cyan", no_wrap=True)
    table.add_column("Value", justify="center")
    table.add_column("Health KPIs", justify="center", style="cyan", no_wrap=True)
    table.add_column("Value", justify="center")

    # Adding rows with conditional colors
    table.add_row(
        "Drilling Success Rate",
        colorize(exploration_kpi['avg_drilling_success_rate'], 90, 60, higher_is_better=True),
        "Revenue Growth Rate (%)",
        colorize(financial_kpi['avg_revenue_growth_rate'], 5000, 1000, higher_is_better=True),
        "Lost Time Incident Rate",
        colorize(health_kpi['avg_lost_time_incident_rate'], 2, 5, higher_is_better=False)
    )

    table.add_row(
        "Machine Downtime (hours)",
        colorize(exploration_kpi['avg_machine_downtime'], 5, 10, higher_is_better=False),
        "Net Income Ratio",
        colorize(financial_kpi['avg_net_income_ratio'], 1, 0.5, higher_is_better=True),
        "Environmental Compliance Rate",
        colorize(health_kpi['avg_environmental_compliance_rate'], 0.8, 0.5, higher_is_better=True)
    )

    table.add_row(
        "Operational Efficiency",
        colorize(exploration_kpi['avg_operational_efficiency'], 80, 50, higher_is_better=True),
        "", "",
        "", ""
    )

    return table


def show_dashboard():
    console = Console()
    
    with Live(console = console, refresh_per_second = 2):
        while True:
            exploration_kpi = get_exploration_kpi()
            financial_kpi = get_financial_kpi()
            health_kpi = get_health_kpi()

            if exploration_kpi and financial_kpi and health_kpi:
                kpi_table = create_kpi_table(exploration_kpi, financial_kpi, health_kpi)
                console.clear()
                console.print(kpi_table)
            else:
                console.print("No data found.")
            
            time.sleep(2)

if __name__ == "__main__":
    show_dashboard()
