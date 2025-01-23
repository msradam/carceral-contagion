from cc_network.server import server
import os

server.port = int(os.environ.get("PORT"))

if __name__ == '__main__':
    server.launch()
