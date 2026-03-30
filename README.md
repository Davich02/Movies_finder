# Final_Python_Project

Console application in Python for searching movies using a hybrid database architecture (MySQL + MongoDB).

---

## Project description

The application provides a command-line interface for searching movies in the **sakila** database.
It demonstrates practical use of both relational (MySQL) and non-relational (MongoDB) databases in a single application.

---

## Features

- Keyword search — find movies by part of the title
- Genre and year search — filter movies by genre and release year range
- Pagination — display results 10 at a time with the option to load more
- Search analytics — view popular queries and search history
- Search logging — all search queries are saved to MongoDB

---

## Tech stack

- Python 3.x — main language
- MySQL — relational DB (movie data)
- MongoDB — document DB (search logs)
- PyMySQL — MySQL connector
- PyMongo — MongoDB driver
- python-dotenv — environment variable management
- tabulate — table output formatting

---

## Project structure

```
Final_project/
├── main.py                    # Main menu and navigation logic
├── handlers/
│   ├── keyword_search.py      # Keyword search handler
│   ├── genre_search.py        # Genre and year search handler
│   └── stats.py               # Search analytics handlers
├── db/
│   └── mysql_connector.py     # MySQL connection and queries
├── logger/
│   ├── log_writer.py          # Search logging to MongoDB
│   └── log_stats.py           # Analytics and statistics
├── utils/
│   └── formatter.py           # Console output formatting
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables (DB credentials)
└── .env_example               # Environment variables template
```

---

## Installation and launch

**1. Clone the repository and navigate to the project folder**

```bash
git clone <repository-url>
cd Final_project
```

**2. Create and activate a virtual environment**

Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy `.env_example` to `.env` and fill in your database credentials.

**5. Run the application**

```bash
python main.py
```
