from flask import Flask
from modules.database import session,models
from modules.Api import api

app = Flask(__name__)

@app.route("/")
def get_data():
    return "A"

if __name__ == "__main__":
    
    session.init_db()

    app.register_blueprint(api.bp)
    app.run(debug=True)

    