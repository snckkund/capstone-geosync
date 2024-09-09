from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    date = request.form.get('date')

    # For now, we just return a simple JSON response
    # In the future, you'll replace this with real health risk prediction logic
    response = {
        "message": f"Climate prediction requested for {location} on {date}"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
