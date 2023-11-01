from flask import Flask
from flask import request, jsonify
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
        
    @app.route("/color/<color>")
    def colorName(color):
        with open(pipe_path, 'w') as pipe:
            pipe.write(f'cmd_colorName,{color}')
            return ""
        
    @app.route("/hexcolor/<hex>")
    def colorHex(hex):
        with open(pipe_path, 'w') as pipe:
            pipe.write(f'cmd_colorHex,{hex}')
            return ""
    
    @app.route("/setiteratelist", methods=["POST"])
    def setiteratelist():
        colors = request.form.get('colors')
        with open(pipe_path, 'w') as pipe:
            pipe.write(f'cmd_setIterateList,{colors}')
            return ""

    @app.route("/mode/random")
    def mode_random():
        with open(pipe_path, 'w') as pipe:
            pipe.write('mode_random')
            return ""

    app.run(port=8000)

except FileExistsError:
    os.remove(pipe_path)