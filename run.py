from flask import Flask
from config.config import Config
from app.routes.receipt_routes import receipt_routes

app = Flask(__name__)
app.config.from_object(Config)

# In mem db for uuid data mapping
app.receipt_db = dict()
#In mem db for uuid points mapping
app.receipt_rewards = dict()

app.register_blueprint(receipt_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
