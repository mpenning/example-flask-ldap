Intro
=====

This project is derived from https://github.com/tutsplus/Flask-LDAP-Auth-Demo,
but I updated several things that no longer work in the original project.

First, Flask-Login's AnonymousUserMixin uses properties like AnonymousUserMixin.is_authenticated, instead of a is_authenticated() method call in the original 
project

Next, the LDAP server had to be changed to reflect a service that is still
online.  I also trapped another LDAP exception (ldap.SERVER_DOWN) in the 
login view.

App Initialization
------------------

Go to ldapflask/__init__.py and customize settings for your environment.  You
probably also need to change try_login() in ldapflask/auth/models.py and 
make the LDAP path reflect your specific environment.

