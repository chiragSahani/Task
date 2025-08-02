# RetainSureTask

This repository contains two main Python projects:

## 1. messy-migration
A sample Flask application for user management and database migration tasks.

**Features:**
- User management API
- Database initialization and configuration
- Error handling and custom exceptions
- Unit tests for API endpoints

**Structure:**
- `src/` - Application source code
- `tests/` - Unit tests
- `users.db` - SQLite database
- `init_db.py` - Database initialization script

**How to Run:**
```bash
python src/main.py
```

**How to Test:**
```bash
pytest tests/
```

---

## 2. url-shortener
A simple URL shortener API built with Flask.

**Features:**
- Shorten URLs and generate short codes
- Redirect to original URLs
- View statistics for shortened URLs
- In-memory storage for URLs
- Comprehensive API tests

**Structure:**
- `app/` - Application source code
- `tests/` - Unit tests

**How to Run:**
```bash
python app/main.py
```

**How to Test:**
```bash
pytest tests/
```

---

## Requirements
Install dependencies for each project:
```bash
pip install -r messy-migration/requirements.txt
pip install -r url-shortener/requirements.txt
```

## License
This project is for educational/demo purposes.

## Contributing
Feel free to fork and submit pull requests!

## Contact
For questions, open an issue on GitHub.
