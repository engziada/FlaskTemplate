from app import app,db
from app.auth import models
from app.auth.views import auth_views

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        models.create_default_admin()
    app.run(debug=True)

