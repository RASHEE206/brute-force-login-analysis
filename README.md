# 🔐 Project Name: Investigating Suspicious Login Attempts (Brute Force Case)

**Role:** Tier 1 Security Analyst  
**Scenario:** Multiple failed login alerts were triggered overnight. As a Tier 1 analyst, you are tasked with analysing authentication logs to identify suspicious activity, detect attack patterns, and determine whether any accounts were compromised.

---

## 🖥️ Environment & Tools Used

| Tool | Purpose |
|------|---------|
| Windows 10/11 | Operating system |
| VS Code | Writing and running the Python script |
| Python 3 | Generating the dataset |
| Python Extension (VS Code) | Running Python inside VS Code |
| pandas | Building and exporting the CSV dataset |
| faker | Generating realistic fake data |
| MySQL Workbench | Running SQL investigation queries |
| MySQL Server 8.0 | Database engine |

---

## 📁 Project Structure

```
brute-force-log-analysis/
│
├── generate_logs.py     ← Python script that generates the dataset
├── login_logs.csv       ← Authentication log dataset (500 records)
└── README.md            ← This file
```

---

## ⚙️ Prerequisites

Before starting, make sure you have the following installed:

- [Python 3](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)
- [MySQL Server 8.0](https://dev.mysql.com/downloads/mysql/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

---

## 🐍 Part 1 — Generating the Dataset (Python + VS Code)

### Step 1 — Install Python 3

Download Python 3 from https://www.python.org/downloads/ and run the installer.

> ⚠️ During installation, tick **"Add Python to PATH"** before clicking Install. If you miss this, Python commands will not work in the terminal.

### Step 2 — Install VS Code

Download from https://code.visualstudio.com/ and install it.

### Step 3 — Install the Python Extension in VS Code

1. Open VS Code
2. Press `Ctrl + Shift + X` to open Extensions
3. Search **Python** by Microsoft
4. Click **Install**

### Step 4 — Create your project folder

Create a folder called `brute-force-log-analysis` anywhere on your computer, for example:
```
C:\Users\YourName\brute-force-log-analysis\
```

### Step 5 — Open the folder in VS Code

1. Open VS Code
2. Click **File → Open Folder**
3. Select your `brute-force-log-analysis` folder

### Step 6 — Open the VS Code terminal

Press `` Ctrl + ` `` (backtick key) to open the built-in terminal at the bottom.

### Step 7 — Install required Python libraries

In the terminal, run:

```bash
pip install pandas faker
```

> ⚠️ If you see `pip is not recognised`, run `python -m pip install pandas faker` instead.

### Step 8 — Create and run the script

1. In VS Code, create a new file called `generate_logs.py`
2. Paste the full Python script into it
3. Save it (`Ctrl + S`)
4. In the terminal, run:

```bash
python generate_logs.py
```

You should see:
```
494 normal login records created.
6 brute-force attack records created.
Attacker IP : 185.234.72.11
Target user : admin
Dataset saved to 'login_logs.csv'
Total records : 500
```

`login_logs.csv` will appear in your project folder.

---

## 📋 Dataset Overview

The file `login_logs.csv` contains 500 rows with the following columns:

| Column       | Description                          | Example               |
|--------------|--------------------------------------|-----------------------|
| `user_id`    | Numeric ID of the user               | `14`                  |
| `username`   | Login username                       | `admin`               |
| `ip_address` | IP address of the login attempt      | `185.234.72.11`       |
| `login_time` | Timestamp of the attempt             | `2025-03-09 16:00:00` |
| `status`     | Outcome — `Success` or `Failed`      | `Failed`              |
| `country`    | Country the login originated from    | `Unknown`             |

**Breakdown:**
- 494 rows — normal login activity (random users, IPs, countries)
- 6 rows — simulated brute-force attack (same IP targeting `admin`)

---

## 🗄️ Part 2 — Setting Up MySQL Workbench

### Step 1 — Install MySQL Server and Workbench

Download and install both from https://dev.mysql.com/downloads/

During installation, set a **root password** — you will need this to log in.

### Step 2 — Open MySQL Workbench and connect

1. Open MySQL Workbench
2. Click **Local instance MySQL80** to connect
3. Enter your root password when prompted

### Step 3 — Create the database

In the query editor, type and execute (`Ctrl + Shift + Enter`):

```sql
CREATE DATABASE IF NOT EXISTS brute_force_analysis;
```

You should see `1 row(s) affected` in the Output panel.

### Step 4 — Select the database

Either:
- **Double-click** `brute_force_analysis` in the Schemas panel on the left until it turns **bold**

Or run:
```sql
USE brute_force_analysis;
```

> ⚠️ This step is essential. MySQL needs to know which database to work in before you can create tables or run queries. If you skip this, you will get a syntax or "no database selected" error.

### Step 5 — Import the CSV using the Import Wizard

This automatically creates the table and loads your data in one step:

1. In the **Schemas** panel on the left, expand `brute_force_analysis`
2. Right-click **Tables**
3. Select **"Table Data Import Wizard"**
4. Click **Browse** and locate your `login_logs.csv` file
5. Select it and click **Next**
6. Choose **"Create new table"**
7. Make sure the destination database is `brute_force_analysis`
8. Set table name to `login_logs`
9. Click **Next**
10. On the column mapping screen, verify these types:

| Column | Type |
|--------|------|
| user_id | INT |
| username | TEXT or VARCHAR |
| ip_address | TEXT or VARCHAR |
| login_time | DATETIME |
| status | TEXT or VARCHAR |
| country | TEXT or VARCHAR |

11. Click **Next** then **Finish**

### Step 6 — Verify the import

Run this query:

```sql
SELECT COUNT(*) FROM login_logs;
```

Expected result: **500**

Then preview your data:

```sql
SELECT * FROM login_logs LIMIT 10;
```

---

## 🔍 Part 3 — SQL Investigation Tasks

All queries below are written in **MySQL syntax**. Run each one in MySQL Workbench.

---

### Task 1 — Users with More Than 5 Failed Login Attempts

**SQL Skills:** `WHERE`, `COUNT()`, `GROUP BY`, `HAVING`

```sql
SELECT username, COUNT(*) AS failed_attempts
FROM login_logs
WHERE status = 'Failed'
GROUP BY username
HAVING COUNT(*) > 5
ORDER BY failed_attempts DESC;
```

**Expected Findings:**

| Username | Failed Attempts |
|----------|----------------|
| mary     | 31             |
| linda    | 29             |
| fatima   | 29             |
| admin    | 29             |
| michael  | 24             |
| david    | 21             |
| alex     | 21             |
| ahmed    | 21             |
| sarah    | 18             |
| john     | 14             |

> ⚠️ All 10 usernames exceeded 5 failed attempts. The `admin` account is of particular concern given its elevated privileges.

---

### Task 2 — Logins Outside Business Hours (Before 8am or After 6pm)

**SQL Skills:** `WHERE`, `HOUR()` time-based filtering

```sql
SELECT username, ip_address, login_time, status, country
FROM login_logs
WHERE HOUR(login_time) < 8
   OR HOUR(login_time) >= 18
ORDER BY login_time;
```

> ℹ️ MySQL uses `HOUR()` for time filtering. This is different from SQLite which uses `strftime()`.

**Expected Findings:**

- **290 out of 500** logins occurred outside business hours
- Logins came from multiple countries including France, UAE, Singapore, Japan, and Turkey

> ⚠️ 58% of all login activity happened outside business hours — a significant anomaly that warrants further investigation.

---

### Task 3 — IP Addresses Attempting Multiple Usernames

**SQL Skills:** `COUNT(DISTINCT ...)`, `GROUP BY`, `HAVING`, `GROUP_CONCAT()`

```sql
SELECT ip_address,
       COUNT(DISTINCT username)        AS unique_users,
       GROUP_CONCAT(DISTINCT username) AS usernames_tried
FROM login_logs
GROUP BY ip_address
HAVING COUNT(DISTINCT username) > 1
ORDER BY unique_users DESC;
```

**Expected Findings:**

- No single IP targeted more than one username in this dataset

> ℹ️ In a real-world dataset, one IP hitting multiple usernames is a strong indicator of **credential stuffing**. This query is essential for detecting that attack pattern.

---

### Task 4 — Successful Login After Multiple Failed Attempts (Brute Force Detection)

**SQL Skills:** `CASE`, `SUM()`, `GROUP BY`, `HAVING`

```sql
SELECT username, ip_address,
       SUM(CASE WHEN status = 'Failed'  THEN 1 ELSE 0 END) AS failed_count,
       SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS success_count
FROM login_logs
GROUP BY username, ip_address
HAVING failed_count >= 3 AND success_count >= 1
ORDER BY failed_count DESC;
```

**Expected Findings:**

| Username | IP Address     | Failed Attempts | Successful Logins |
|----------|---------------|-----------------|-------------------|
| admin    | 185.234.72.11 | 5               | 1                 |

> 🚨 **CONFIRMED BREACH** — IP `185.234.72.11` made 5 consecutive failed attempts against `admin` before successfully logging in. This is a textbook brute-force attack pattern.

---

## 🚨 Summary of Findings

| # | Finding | Severity |
|---|---------|----------|
| 1 | All 10 usernames had more than 5 failed login attempts | Medium |
| 2 | 290 logins (58%) occurred outside business hours | High |
| 3 | No credential stuffing detected in this dataset | Low |
| 4 | IP `185.234.72.11` brute-forced and breached the `admin` account | Critical |

---

## 🛡️ Recommended Actions

1. **Lock the `admin` account** and force a password reset immediately
2. **Block IP `185.234.72.11`** at the firewall level
3. **Investigate the 290 after-hours logins** — verify against known employee locations and VPN usage
4. **Enable account lockout policies** — lock accounts after 3–5 failed attempts
5. **Set up SIEM alert rules** for repeated failures from the same IP within a short time window

---

## ⚠️ Challenges Faced & Troubleshooting

---

### Challenge 1 — Externally Managed Python Environment (Kali Linux)

**Error:**
```
error: externally-managed-environment
This environment is externally managed
```

**Why it happens:**
Kali Linux (and modern Debian-based systems) protect the system Python installation. Running `pip install` directly is blocked to prevent conflicts with OS-managed packages.

**How it was resolved:**
The project was moved to **Windows with VS Code**, where `pip install` works without restrictions.

**Alternative — use a virtual environment on Kali Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
./venv/bin/pip install faker pandas
python3 generate_logs.py
```

> ⚠️ You must activate the virtual environment every time you open a new terminal session.

---

### Challenge 2 — IndentationError in Python

**Error:**
```
IndentationError: unindent does not match any outer indentation level
```

**Why it happens:**
Python requires consistent indentation throughout a file. Editing in nano on Kali Linux can accidentally mix tabs and spaces, which Python does not allow.

**How it was resolved:**
Switched to **VS Code**, which uses spaces consistently and highlights indentation errors in real time before the script is even run.

**If you must use nano:**
```bash
# Check for tabs in your file
cat -A generate_logs.py | grep -n "	"
# Any line showing ^I has a tab character — replace with 4 spaces
```

---

### Challenge 3 — MySQL "No Database Selected" Error

**Error:**
```
Error Code 1046: No database selected
```

**Why it happens:**
MySQL has multiple databases and needs to be told which one to use before running any queries.

**Fix — always select your database first:**
```sql
USE brute_force_analysis;
```

Or double-click the database name in the Schemas panel until it turns **bold**.

---

### Challenge 4 — Error Code 1064 SQL Syntax Error

**Error:**
```
Error Code 1064: You have an error in your SQL syntax
```

**Common causes and fixes:**

| Cause | Fix |
|-------|-----|
| Using SQLite syntax in MySQL | Use `HOUR()` instead of `strftime()` |
| Missing semicolon at end of query | Add `;` at the end |
| Database not selected before query | Run `USE brute_force_analysis;` first |
| Typo in table or column name | Check spelling matches exactly |

---

### Challenge 5 — login_time Column Imports as TEXT Instead of DATETIME

**Why it happens:**
The CSV Import Wizard sometimes detects `login_time` as plain text instead of DATETIME.

**Fix — convert the column after import:**
```sql
ALTER TABLE login_logs
MODIFY COLUMN login_time DATETIME;

UPDATE login_logs
SET login_time = STR_TO_DATE(login_time, '%Y-%m-%d %H:%i:%S');
```

**Verify it worked:**
```sql
SELECT login_time, HOUR(login_time) FROM login_logs LIMIT 5;
```
If `HOUR()` returns numbers, the column is correctly set as DATETIME.

---

### Challenge 6 — pip Not Recognised on Windows

**Error:**
```
'pip' is not recognized as an internal or external command
```

**Why it happens:**
Python was installed without ticking **"Add Python to PATH"**.

**Fix:**
```bash
python -m pip install pandas faker
```

Or reinstall Python and tick the PATH option during installation.

---

## 📚 SQL Skills Demonstrated

| Skill | Used In |
|-------|---------|
| `WHERE` clause filtering | Tasks 1, 2, 4 |
| `COUNT()` aggregation | Tasks 1, 3 |
| `GROUP BY` & `HAVING` | Tasks 1, 3, 4 |
| Time-based filtering with `HOUR()` | Task 2 |
| Conditional aggregation with `CASE` | Task 4 |
| `COUNT(DISTINCT ...)` | Task 3 |
| `GROUP_CONCAT()` | Task 3 |

---

## 👤 Author

Cybersecurity Student — Entry Level Security Analyst Portfolio Projects.
Tools: Python 3, VS Code, MySQL Workbench, pandas, faker  
OS: Windows
