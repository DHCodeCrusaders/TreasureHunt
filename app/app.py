from dotenv import load_dotenv
from flask import Flask
from loguru import logger

logger.info("Loading .env file")
load_dotenv()

from .controllers.riddle import riddle_blueprint
from .controllers.users import user_blueprint

app = Flask(__name__)

URL_PREFIX = "/hunt"

# Blueprints
app.register_blueprint(user_blueprint, url_prefix=URL_PREFIX)
app.register_blueprint(riddle_blueprint, url_prefix=URL_PREFIX)

if __name__ == "__main__":
    app.run()
