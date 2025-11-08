from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

workouts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_workout():
    workout = request.form.get('workout')
    duration = request.form.get('duration')
    if not workout or not duration:
        return render_template('index.html', error="Please fill all fields")
    try:
        duration = int(duration)
    except ValueError:
        return render_template('index.html', error="Duration must be a number")
    workouts.append({"workout": workout, "duration": duration})
    return redirect(url_for('view_workouts'))

@app.route('/view')
def view_workouts():
    return render_template('view.html', workouts=workouts)

if __name__ == '__main__':
    app.run(debug=True)
