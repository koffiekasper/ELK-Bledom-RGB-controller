from flask import Flask
import os

try:
    pipe_path = "./.pipe"
    os.mkfifo(pipe_path)

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/toggle")
    def toggle():
        with open(pipe_path, 'w') as pipe:
            pipe.write('cmd_toggle')
            return ""

    @app.route("/mode/random")
    def mode_random():
        with open(pipe_path, 'w') as pipe:
            pipe.write('mode_random')
            return ""

    app.run(port=8000)

except FileExistsError:
    os.remove(pipe_path)
    
except:
    os.remove(pipe_path)