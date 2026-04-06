# Fitness Assistant

A local single-user fitness dashboard built with **Flask** and **SQLite**.

## Team Ownership

| Member | Functionality | What to work on |
|--------|--------------|-----------------|
| **Colin** | 1 - User Profile & Account Management | `app.py` (profile routes), `templates/profile.html`, `templates/dashboard.html` |
| **Zack** | 2 - Workout Logging | `app.py` (log routes), `templates/log.html` |
| **Aaron** | 3 - Progress Dashboard & Analytics | `app.py` (progress routes), `templates/progress.html` |
| **Christian** | 4 - Exercise Suggestions | `app.py` (exercises routes), `templates/exercises.html` |
| **Ha** | 5 - Workout Scheduling | `app.py` (schedule routes), `templates/schedule.html` |

**Shared files (coordinate changes):** `app.py`, `database.py`, `templates/layout.html`, `static/style.css`

---

## Getting Started

### 1. Clone & branch
```bash
git clone https://github.com/YOUR_ORG/fitness-assistant.git
cd fitness-assistant
git checkout -b feature/your-feature-name
```

### 2. Install & run
```bash
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

Or on Windows, just double-click `start.bat`.

---

## Project Structure

```
app.py                ← all routes (each member adds theirs here)
database.py           ← database setup and tables
requirements.txt      ← just flask
start.bat             ← one-click startup (Windows)
static/
  style.css           ← shared stylesheet
templates/
  layout.html         ← shared nav and page layout
  dashboard.html      ← home page
  profile.html        ← Functionality 1 (Colin)
  log.html            ← Functionality 2 
  progress.html       ← Functionality 3 
  exercises.html      ← Functionality 4 
  schedule.html       ← Functionality 5 
```

## How to add your functionality

1. Open `app.py` and find your TODO section
2. Add your routes (look at the profile routes as an example)
3. Open your template in `templates/` and replace the placeholder HTML
4. Use `database.py`'s `get_db()` to read/write from the database
5. Test by running `python app.py` and checking your page

## Branch Workflow

1. Work on `feature/your-name` branch
2. `git push origin feature/your-name`
3. Open a Pull Request to main on GitHub
4. Team lead reviews and merges
5. `git checkout main && git pull` to sync
