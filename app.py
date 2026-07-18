from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.api_routes import api_bp
from routes.event_routes import event_bp

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

# Define what they user should see when they visit the root URL
@app.route("/")
def index():
    return render_template("index.html")

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(event_bp)

if __name__ == "__main__":
    app.run(debug=False)
