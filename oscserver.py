"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


class OscServer:
    def __init__(self, func):
        self.func = func
#    pipe_path = "./.pipe_osc"

#    def self.func(endpoint, data):
#        with open(pipe_path, 'w') as pipe:
#            pipe.write(str(endpoint) + "," + str(data))
#
#        def main():
#        os.mkfifo(pipe_path)


    def main(self): 
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
            default="0.0.0.0", help="The ip to listen on")
        parser.add_argument("--port",
            type=int, default=777, help="The port to listen on")
        args = parser.parse_args()

        dispatcher = Dispatcher()
        dispatcher.map("/beat", self.func)
        dispatcher.map("/bar", self.func)
        dispatcher.map("/prog1", self.func)
        dispatcher.map("/prog2", self.func)
        dispatcher.map("/prog3", self.func)
        dispatcher.map("/prog4", self.func)
        dispatcher.map("/prog5", self.func)
        dispatcher.map("/prog6", self.func)
        dispatcher.map("/prog7", self.func)
        dispatcher.map("/prog8", self.func)

        server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

#    try:
#        main()
#    except FileExistsError:
#        os.remove(pipe_path)
#        main()