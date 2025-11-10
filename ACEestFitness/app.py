from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

@app.route('/')
def index():
    return render_template('index.html', categories=workouts.keys())

@app.route('/add', methods=['POST'])
def add_workout():
    category = request.form.get('category')
    exercise = request.form.get('exercise')
    duration = request.form.get('duration')

    if not category or not exercise or not duration:
        return render_template('index.html', categories=workouts.keys(), error="Please fill all fields")
    if category not in workouts:
        return render_template('index.html', categories=workouts.keys(), error="Invalid category")

    try:
        duration = int(duration)
    except ValueError:
        return render_template('index.html', categories=workouts.keys(), error="Duration must be an integer")

    workouts[category].append({"exercise": exercise, "duration": duration})

    return redirect(url_for('view_workouts'))

@app.route('/view')
def view_workouts():
    return render_template('view.html', workouts=workouts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
