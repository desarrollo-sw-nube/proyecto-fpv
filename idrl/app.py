# app.py

from idrl import create_app
from auth.views import auth_blueprint

app = create_app()
app_context = app.app_context()
app_context.push()

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
