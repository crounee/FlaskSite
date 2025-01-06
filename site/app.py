from flask import Flask
from modules.database import session,models
from modules.Api import api
from werkzeug.middleware.proxy_fix import ProxyFix
from waitress import serve

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def get_data():
    return "main page"

if __name__ == "__main__":
    session.init_db()
    app.register_blueprint(api.bp)
    #app.run(debug=True,host="0.0.0.0",port=5000)
    serve(app,host="0.0.0.0",port=5000)

    