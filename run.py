from geo_service import app
import os


if __name__ == '__main__':
    print(app.name)
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'development'
    app.run()

