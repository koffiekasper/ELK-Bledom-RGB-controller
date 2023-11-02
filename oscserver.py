"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

pipe_path = "./.pipe_osc"

def write_pipe(endpoint, data):
  with open(pipe_path, 'w') as pipe:
    pipe.write(str(endpoint) + "," + str(data))

def main():
  os.mkfifo(pipe_path)


  if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=777, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/beat", write_pipe)
    dispatcher.map("/bar", write_pipe)
    dispatcher.map("/prog1", write_pipe)
    dispatcher.map("/prog2", write_pipe)
    dispatcher.map("/prog3", write_pipe)
    dispatcher.map("/prog4", write_pipe)
    dispatcher.map("/prog5", write_pipe)
    dispatcher.map("/prog6", write_pipe)
    dispatcher.map("/prog7", write_pipe)
    dispatcher.map("/prog8", write_pipe)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

try:
    main()
except FileExistsError:
    os.remove(pipe_path)
    main()