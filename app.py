import os
from flask import Flask, Blueprint

from rest import api
from setting.database import initialize_db
from ad.views import ad as ad_name_space
from category.views import ca as category_name_space
from user.views import ns as user_name_space


app = Flask(__name__)


blueprint = Blueprint('api', __name__, url_prefix='/')
api.init_app(blueprint)
api.add_namespace(user_name_space)
api.add_namespace(category_name_space)
api.add_namespace(ad_name_space)
app.register_blueprint(blueprint)
# get env variable
app.config['BUNDLE_ERRORS'] = False
db = initialize_db(app)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=os.getenv('PORT'))
