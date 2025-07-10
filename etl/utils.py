from datetime import datetime
import sqlite3

def log_etl_success(script_name, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {script_name}: {message}\n"
    with open("logs/etl.log", "a") as log_file:
        log_file.write(log_line)

def get_db_connection():
    conn = sqlite3.connect("db/fantasy_football.db")
    return conn

def get_valid_season_years():
    """Returns a list of ESPN-supported seasons that have valid data."""
    return [year for year in range(2019, 2025)]  # ESPN API supports 2019–2024

def get_valid_seasons():
    """Alias for get_valid_season_years to avoid import issues."""
    return get_valid_season_years()
