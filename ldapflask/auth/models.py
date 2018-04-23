import ldap
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from ldapflask import db, app
 
 
def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn
 
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
 
    def __init__(self, username, password):
        self.username = username
 
    # https://www.forumsys.com/tutorials/integration-how-to/ldap/online-ldap-test-server/
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        # credentials: tesla / password
        conn.simple_bind_s(
            #'cn={0},ou=scientists,dc=example,dc=com'.format(username), password
            'uid={0},dc=example,dc=com'.format(username), password
        )
 
    @property
    def is_authenticated(self):
        return True
 
    @property
    def is_active(self):
        return True
 
    @property
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
 
class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
