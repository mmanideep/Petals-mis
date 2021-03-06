import os
import sys

from flask.cli import shell_command
from petals_mis.app import app

if __name__ == '__main__':
    os.environ["PYTHONPATH"] = os.getcwd()
    os.environ["FLASK_APP"] = "petals_mis/app.py"
    try:
        arg = sys.argv.pop(1)
    except IndexError:
        arg = ""
    if arg == "shell":
        shell_command()
    else:
        app.run(host="0.0.0.0", threaded=True, port=8000, debug=True)
