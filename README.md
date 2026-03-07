# 🔐 Investigating Suspicious Login Attempts (Brute Force Case)

A beginner-friendly cybersecurity project that generates a realistic authentication log dataset in Python. The dataset simulates normal user login activity alongside a hidden brute-force attack — perfect for practising security analysis, anomaly detection, and SIEM investigations.

---

## 📁 Project Structure

```
project-folder/
│
├── generate_logs.py   ← Python script that generates the dataset
├── login_logs.csv     ← Output CSV file (created when you run the script)
└── README.md          ← This file
```

---

## ⚙️ Requirements

- Python 3 (pre-installed on Kali Linux)
- The following Python libraries:
  - `pandas` — for building and exporting the dataset
  - `faker`  — for generating realistic fake data (IPs, countries, etc.)

---

## 🚀 Setup & Installation

Follow these steps in order inside your Kali Linux terminal:

**1. Create a project folder and navigate into it**
```bash
mkdir login-investigation
cd login-investigation
```

**2. Place the script inside the folder**

Copy or move `generate_logs.py` into the `login-investigation` folder.

**3. Install the required libraries**
```bash
pip3 install faker pandas
```

**4. Run the script**
```bash
python3 generate_logs.py
```

**5. Check the output**
```bash
cat login_logs.csv
```
Or open it in a spreadsheet tool like LibreOffice Calc.

---

## 📋 Dataset Overview

The generated `login_logs.csv` file contains **500 rows** with the following columns:

| Column       | Description                              | Example                  |
|--------------|------------------------------------------|--------------------------|
| `user_id`    | Numeric ID of the user                   | `14`                     |
| `username`   | Login username                           | `sarah`                  |
| `ip_address` | IP address of the login attempt          | `203.45.12.88`           |
| `login_time` | Timestamp of the attempt                 | `2025-03-03 10:22:00`    |
| `status`     | Outcome of the login                     | `Success` or `Failed`    |
| `country`    | Country the login originated from        | `Germany`                |

### Breakdown
- **494 rows** — normal login activity (random users, IPs, countries)
- **6 rows**   — simulated brute-force attack (same IP, same target user)

---

## 🔍 The Brute-Force Attack Pattern

The script embeds a brute-force attack with this signature:

```
Attempt 1  →  IP: 185.234.72.11  |  user: admin  |  status: Failed
Attempt 2  →  IP: 185.234.72.11  |  user: admin  |  status: Failed
Attempt 3  →  IP: 185.234.72.11  |  user: admin  |  status: Failed
Attempt 4  →  IP: 185.234.72.11  |  user: admin  |  status: Failed
Attempt 5  →  IP: 185.234.72.11  |  user: admin  |  status: Failed
Attempt 6  →  IP: 185.234.72.11  |  user: admin  |  status: Success  ← breach!
```

These 6 records are shuffled into the dataset so you have to query for them — just like a real analyst would.

---

## 🧪 Investigation Exercises

Once you have the dataset, try these analysis tasks:

1. **Find the attacker** — Filter all rows where `status = Failed` and count attempts per IP address.
2. **Confirm the breach** — Check if any IP that had failures also has a `Success`.
3. **Timeline the attack** — Sort the suspicious IP's records by `login_time`.
4. **Red flags to spot:**
   - Same IP with 5+ failed attempts in a short window
   - `country = Unknown`
   - `user_id = 999` (out of the normal 1–50 range)

---

## 🛠️ Customisation

You can easily tweak the script by editing the constants at the top of `generate_logs.py`:

```python
TOTAL_LOGS        = 500          # change total number of records
BRUTE_FORCE_COUNT = 6            # change number of attack attempts
ATTACKER_IP       = "185.234.72.11"   # change the attacker's IP
TARGET_USERNAME   = "admin"           # change the targeted account
```

---
##📚 Troubleshooting tips.
- Install a virtual environment if packages are not installed automatically because kali protects the environment.
- Indentation issues may occur without the uninstalled libraries(install a virtual environment).
- Check out this video https://youtu.be/Y21OR1OPC9A?si=2pj19BUWNVZjbha0
- 

## 📚 Learning Outcomes

By completing this project you will have practised:

- Generating synthetic security datasets with Python
- Understanding what a brute-force attack looks like in log data
- Using `pandas` to filter, sort, and analyse tabular data
- Building the foundation for SIEM detection rules

---

## 👤 Author

 Raspberry Pie — Entry Level Security Analyst Project.
