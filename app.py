from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)

# set up the database tables when the app starts
init_db()


# ---- helper to get the current user ----
def get_user():
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = 1").fetchone()
    db.close()
    return user


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

    workouts= db.execute(

        "Select *" 
        "From workout_logs " 
        "Where user_id = 1 " 
        "Order by id " 
        ""
    ).fetchall()
    db.close()

    # : pass the list of workouts to the template
    return render_template("log.html", workouts=workouts)

#  POST route for logging a new workout
@app.route("/log/add", methods=["POST"])
def add_workout():

    db = get_db()
    # Get form data and INSERT into workout_logs
    db.execute("""
        INSERT INTO workout_logs (user_id, exercise_name, muscle_group, sets, reps, weight, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        request.form.get("exercise_name"),

        request.form.get("muscle_group"),
        request.form.get("sets") or None,

        request.form.get("reps") or None,

        request.form.get("weight") or None,

        request.form.get("notes"),
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

@app.route("/schedule")
def schedule_page():
    # TODO: query workout_schedules for user_id = 1, ordered by date
    # TODO: pass the list to the template
    return render_template("schedule.html")

# TODO: add a POST route for creating a new scheduled workout
#       - read form fields: title, scheduled_date, duration_minutes, notes
#       - INSERT into workout_schedules table
#       - redirect back to /schedule

# TODO: add a POST route for marking a scheduled workout as completed
#       - UPDATE workout_schedules SET completed = 1 WHERE id = ?
#       - redirect back to /schedule

# TODO: add a POST route for deleting a scheduled workout
#       - DELETE from workout_schedules WHERE id = ? AND user_id = 1
#       - redirect back to /schedule


# ---- start the server ----
if __name__ == "__main__":
    app.run(debug=True, port=5000)
