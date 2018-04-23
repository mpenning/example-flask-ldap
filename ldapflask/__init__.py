from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
 
### 
### Customize settings below
### 
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' # In-memory DB...
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
# https://www.forumsys.com/tutorials/integration-how-to/ldap/online-ldap-test-server/
app.config['LDAP_PROVIDER_URL'] = 'ldap://ldap.forumsys.com:389/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
# Import auth blueprint later since auth depends on login_manager...
from ldapflask.auth.views import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
 
db.create_all()
