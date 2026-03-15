import pandas as pd
import random
from datetime import datetime, timedelta

# --- Configuration ---
TOTAL_LOGS       = 500
BRUTE_FORCE_COUNT = 6
NORMAL_COUNT     = TOTAL_LOGS - BRUTE_FORCE_COUNT

START_TIME       = datetime(2025, 3, 1, 8, 0, 0)
OUTPUT_PATH      = "login_logs.csv"

USERNAMES = [
    "admin", "john", "mary", "david", "fatima",
    "alex", "sarah", "ahmed", "linda", "michael"
]

COUNTRIES = [
    "United States", "United Kingdom", "Germany", "France", "Canada",
    "Australia", "Brazil", "India", "Japan", "South Korea", "Mexico",
    "Italy", "Spain", "Netherlands", "Sweden", "Norway", "Poland",
    "Argentina", "South Africa", "Nigeria", "Egypt", "Turkey",
    "Saudi Arabia", "UAE", "Singapore", "Malaysia", "Indonesia",
    "Philippines", "Vietnam", "Thailand", "Pakistan", "Bangladesh",
    "Ukraine", "Romania", "Czech Republic", "Portugal", "Greece",
    "Chile", "Colombia", "Peru", "New Zealand", "Ireland", "Denmark"
]


def random_ipv4() -> str:
    """Generate a random valid IPv4 address."""
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_normal_logs(n: int) -> list:
    """Generate n normal (non-attack) login log entries."""
    logs = []
    for _ in range(n):
        logs.append({
            "user_id":    random.randint(1, 50),
            "username":   random.choice(USERNAMES),
            "ip_address": random_ipv4(),
            "login_time": START_TIME + timedelta(minutes=random.randint(1, 10_000)),
            "status":     random.choice(["Success", "Failed"]),
            "country":    random.choice(COUNTRIES),
        })
    return logs


def generate_brute_force_logs(
    attacker_ip: str,
    target_user: str,
    count: int,
    time_offset_minutes: int = 12_000,
) -> list:
    """
    Simulate a brute-force attack: (count - 1) failed attempts
    followed by a single successful login.
    """
    logs = []
    for i in range(count):
        logs.append({
            "user_id":    999,
            "username":   target_user,
            "ip_address": attacker_ip,
            "login_time": START_TIME + timedelta(minutes=time_offset_minutes + i),
            "status":     "Failed" if i < count - 1 else "Success",
            "country":    "Unknown",
        })
    return logs


def main():
    # Build full dataset
    logs = generate_normal_logs(NORMAL_COUNT)
    logs += generate_brute_force_logs(
        attacker_ip="185.234.72.11",
        target_user="admin",
        count=BRUTE_FORCE_COUNT,
    )

    df = pd.DataFrame(logs, columns=[
        "user_id", "username", "ip_address", "login_time", "status", "country"
    ])

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ {len(df)} login logs saved to '{OUTPUT_PATH}'")
    print(f"   Normal logs     : {NORMAL_COUNT}")
    print(f"   Brute-force logs: {BRUTE_FORCE_COUNT}")


if __name__ == "__main__":
    main()
