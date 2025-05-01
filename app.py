import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from workout_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
