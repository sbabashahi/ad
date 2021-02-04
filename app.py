from flask import Flask, Blueprint

from rest import api
from setting.database import initialize_db
from user.models import init_db
from user.views import ns as user_name_space


app = Flask(__name__)


blueprint = Blueprint('api', __name__, url_prefix='/')
api.init_app(blueprint)
api.add_namespace(user_name_space)
app.register_blueprint(blueprint)
# get env variable
app.config['BUNDLE_ERRORS'] = True
app.config['SECRET_KEY'] = 'set a key and get it from env'
db = initialize_db(app)


if __name__ == "__main__":
    app.run(debug=True)
    init_db()
