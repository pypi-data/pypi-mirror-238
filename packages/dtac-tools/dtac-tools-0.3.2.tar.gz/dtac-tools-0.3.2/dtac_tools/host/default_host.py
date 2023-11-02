# default_host.py
import os
import socket
import sys
import json

from .helpers.encryptor import RpcEncryptor
from .plugin_host import PluginHost
from .helpers.network import get_unused_tcp_port

class DefaultPluginHost(PluginHost):
    def __init__(self, plugin):
        self.plugin = plugin
        self.proto = "tcp"
        self.ip = "127.0.0.1"
        self.interface_version = 'plug_api_1.0'
        self.port = None
        self.route_map = {}
        self.encryptor = RpcEncryptor.new_encryptor()

    def handle_request(self, data):
        request = json.loads(data)
        if request["method"] == f"{self.plugin.name()}.Register":
            routes = self.plugin.register(request["params"])
            for route in routes:
                key = route.handle_func.__name__
                self.route_map[key] = route.handle_func
                route.handle_func = key
            response = {
                "id": request["id"],
                "result": {
                    "Routes": [r.__dict__() for r in routes],
                },
                "error": None
            }
            return json.dumps(response)
        else:
            key = request["method"].replace(f"{self.plugin.name()}.", "")
            if key in self.route_map:
                f = self.route_map[key]
                response = {
                    "id": request["id"],
                    "result": json.dumps(f(request["params"])),
                    "error": None
                }
        return json.dumps(response)

    def serve(self):

        env_cookie = os.getenv("DTAC_PLUGINS")
        if env_cookie is None:
            print('============================ WARNING ============================')
            print('This is a DTAC plugin and is not designed to be executed directly')
            print('Please use the DTAC agent to load this plugin')
            print('==================================================================')
            sys.exit(-1)

        self.port = get_unused_tcp_port()

        print(f"CONNECT{{{{{self.plugin.name()}:{self.plugin.route_root()}:{self.proto}:{self.ip}:{self.port}:{self.interface_version}:{self.encryptor.key_string()}}}}}")
        sys.stdout.flush()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()

            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(8192)
                    response = self.handle_request(data.decode('utf-8'))
                    if response:
                        conn.sendall(response.encode('utf-8'))

    def get_port(self):
        return self.port