import os

from app import app, db


def create_tables():
    with app.app_context():
        if not database_exists():
            print("create db")
            db.create_all()

def database_exists():
    return os.path.exists("instance/temp.db")

if __name__ == "__main__":
    create_tables()
    app.run(debug=False)
