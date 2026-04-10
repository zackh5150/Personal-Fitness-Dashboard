from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db
from datetime import datetime

app = Flask(__name__)

# set up the database tables when the app starts
init_db()


# ---- helper to get the current user ----
def get_user():
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = 1").fetchone()
    db.close()
    return user

def getUpcomingWorkout(schedules):
    now = datetime.now()
    upcoming = None

    for s in schedules:
        try:
            dt = datetime.strptime(s["scheduled_date"], "%Y-%m-%dT%H:%M")
        except:
            try:
                dt = datetime.strptime(s["scheduled_date"], "%Y-%m-%d %H:%M")
            except:
                continue

        if dt > now:
            if upcoming is None or dt < upcoming[0]:
                upcoming = (dt, s)

    return upcoming[1] if upcoming else None

# ---- Dashboard (home page) ----

@app.route("/")
def dashboard():
    user = get_user()

    db = get_db()
    workout_count = db.execute(
        "SELECT COUNT(*) FROM workout_logs WHERE user_id = 1"
    ).fetchone()[0]

    upcoming_count = db.execute(
        "SELECT COUNT(*) FROM workout_schedules WHERE user_id = 1 AND completed = 0"
    ).fetchone()[0]
    db.close()

    return render_template("dashboard.html",
                           user=user,
                           workout_count=workout_count,
                           upcoming_count=upcoming_count)


# ================================================================
#  Functionality 1: User Profile & Account Management (Colin)
# ================================================================

@app.route("/profile")
def profile():
    user = get_user()
    return render_template("profile.html", user=user)


@app.route("/profile/update", methods=["POST"])
def update_profile():
    db = get_db()
    db.execute("""
        UPDATE users
        SET display_name = ?,
            height = ?,
            weight = ?,
            age = ?,
            goal = ?,
            fitness_level = ?
        WHERE id = 1
    """, (
        request.form.get("display_name"),
        request.form.get("height") or None,
        request.form.get("weight") or None,
        request.form.get("age") or None,
        request.form.get("goal"),
        request.form.get("fitness_level"),
    ))
    db.commit()
    db.close()
    return redirect(url_for("profile"))


# ================================================================
#  Functionality 2: Workout Logging ( - Zack)
# ================================================================

@app.route("/log")
def log_page():
    # : query workout_logs table for user_id = 1
    db = get_db()


    #  create a list of common gym equipment for the datalist in the form for allowing smart excercise suggestions based on available equipment
    equipmentPool = [
        "bench press machine", "bicep curl machine", "cable machine", "calf raise machine",
        "chest fly machine / pec deck machine", "chest press machine", "dip machine", "elliptical machine",
        "glute-ham developer", "hack squat machine", "high row machine", "hyperextension bench / roman chair",
        "lat pulldown machine", "lateral raise machine", "leg curl machine", "leg extension machine",
        "leg press machine", "leverage deadlift machine", "pullover machine", "rear delt fly machine",
        "rowing machine", "seated back extension machine", "seated row machine", "shoulder press machine",
        "shrug machine", "smith machine", "squat machine", "stair climber machine", "standing leg curl machine",
        "t-bar row machine", "treadmill", "triceps extension machine", "adjustable bench", "decline bench",
        "flat bench", "incline bench", "military press bench", "preacher bench", "bench", "barbell", "axle bar",
        "body bar", "ez curl bar", "trap bar / hex bar", "strongman log", "dumbbell", "kettlebell", "weight plate",
        "medicine ball", "power rack / squat rack", "barbell rack", "captain's chair", "pull-up bar",
        "dip bars / parallel bars", "gymnastic rings", "cable handle / d-handle", "v-bar / row handle",
        "rope attachment", "straight bar attachment", "lat pulldown bar", "ez bar attachment", "ankle strap",
        "resistance band", "bfr bands / occlusion bands", "chain", "plyo box", "aerobic step", "block",
        "platform", "exercise mat", "foam roller", "stability ball", "bosu ball", "weight belt / dip belt",
        "head harness", "barbell pad", "barbell collars", "knee pad", "wrist wraps", "ankle weights", "weight vest",
        "wrist weights", "atlas stone", "farmer's walk implements", "sled", "tire", "yoke", "sandbag", "keg",
        "rickshaw frame", "conan's wheel", "circus bell", "stationary bike", "jump rope", "agility ladder",
        "cone", "hurdle", "sliders", "anchor point / door anchor", "landmine attachment", "suspension trainer",
        "towel", "wrist roller", "safety pins / j-hooks", "strap", "chair", "climbing rope", "heavy bag",
        "sledgehammer", "wall", "training partner", "post", "stairs", "dowel / pvc pipe"]
    workouts= db.execute(

        "Select *" 
        "From workout_logs " 
        "Where user_id = 1 " 
        "Order by id " 
        ""
    ).fetchall()
    db.close()

    #  pass the list of workouts and equipment pool to the template
    return render_template("log.html", workouts=workouts, equipmentPool=equipmentPool)

#  POST route for logging a new workout

@app.route("/log/add", methods=["POST"])
def add_workout():

    db = get_db()
    # Get form data and INSERT into workout_logs
    db.execute("""
               
    INSERT INTO workout_logs (user_id, exercise_name, muscle_group, sets, reps, weight, notes, equipment)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    1,
    request.form.get("exercise_name"),
    request.form.get("muscle_group"),
    request.form.get("sets") or None,
    request.form.get("reps") or None,
    request.form.get("weight") or None,
    request.form.get("notes"),
    # Added equipment for excercise funcionality 
    request.form.get("equipment") or None,
))
    db.commit()
    db.close()
    # - redirect back to /log
    return redirect(url_for("log_page"))



#  POST route for deleting a workout
@app.route("/log/delete/<int:workout_id>", methods=["POST"])

def delete_workout(workout_id):
    db = get_db()

        # DELETE from workout_logs WHERE id = ? AND user_id = 1
    db.execute("""
        DELETE FROM workout_logs
        WHERE id = ? AND user_id = 1
    """, (workout_id,))
    db.commit()

    db.close()

    #  - redirect back to /log
    return redirect(url_for("log_page"))
#    



# ================================================================
#  Functionality 3: Progress Dashboard & Analytics (TODO - Aaron)
# ================================================================

@app.route("/progress")
def progress_page():
    # TODO: query workout_logs for user_id = 1
    # TODO: calculate stats like total volume, most common exercises, etc.
    # TODO: pass the stats to the template to display
    return render_template("progress.html")


# ================================================================
#  Functionality 4: Exercise Suggestions (TODO - Christian)
# ================================================================

@app.route("/exercises")
def exercises_page():
    # TODO: let user pick a muscle group or equipment type
    # TODO: call the API Ninjas exercise API to get suggestions
    #       API URL: https://api.api-ninjas.com/v1/exercises
    # TODO: show the results on the page
    return render_template("exercises.html")

# TODO: add a POST route for rating an exercise
#       - INSERT or UPDATE exercise_ratings table
#       - redirect back to /exercises


# ================================================================
#  Functionality 5: Workout Scheduling (TODO - Ha)
# ================================================================

# VIEW SCHEDULE PAGE

@app.route("/schedule")
def schedule_page():
    db = get_db()

    schedules = db.execute("""
        SELECT * FROM workout_schedules
        WHERE user_id = 1
        ORDER BY scheduled_date ASC
    """).fetchall()

    db.close()

    upcoming = getUpcomingWorkout(schedules)

    return render_template("schedule.html", schedules=schedules, upcoming=upcoming)

# CREATE SCHEDULE

@app.route("/schedule/create", methods=["POST"])
def create_schedule():
    db = get_db()

    scheduled_date = request.form["scheduled_date"]
    duration = request.form["duration_minutes"]
    notes = request.form.get("notes", "")

    db.execute("""
        INSERT INTO workout_schedules (user_id, scheduled_date, duration_minutes, notes, completed)
        VALUES (1, ?, ?, ?, 0)
    """, (scheduled_date, duration, notes))

    db.commit()
    db.close()

    return redirect(url_for("schedule_page"))

# UPDATE SCHEDULE

@app.route("/schedule/update/<int:id>", methods=["POST"])
def update_schedule(id):
    db = get_db()

    scheduled_date = request.form["scheduled_date"]
    duration = request.form["duration_minutes"]
    notes = request.form.get("notes", "")
    completed = request.form.get("completed", 0)

    db.execute("""
        UPDATE workout_schedules
        SET scheduled_date = ?, duration_minutes = ?, notes = ?, completed = ?
        WHERE id = ? AND user_id = 1
    """, (scheduled_date, duration, notes, completed, id))

    db.commit()
    db.close()

    return redirect(url_for("schedule_page"))

# DELETE SCHEDULE

@app.route("/schedule/delete/<int:id>", methods=["POST"])
def delete_schedule(id):
    db = get_db()

    db.execute("""
        DELETE FROM workout_schedules
        WHERE id = ? AND user_id = 1
    """, (id,))

    db.commit()
    db.close()

    return redirect(url_for("schedule_page"))

# ---- start the server ----
if __name__ == "__main__":
    app.run(debug=True, port=5000)
