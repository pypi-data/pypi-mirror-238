# default_host.py
import os
import socket
import sys
import json
import traceback

from .helpers.debug_sender import DebugSender
from .helpers.encryptor import RpcEncryptor
from .plugin_host import PluginHost
from .helpers.network import get_unused_tcp_port
from ..plugins.types import InputArgs


class DefaultPluginHost(PluginHost):
    def __init__(self, plugin, debug=False, debug_port=5678):
        self.plugin = plugin
        self.proto = "tcp"
        self.ip = "127.0.0.1"
        self.interface_version = 'plug_api_1.0'
        self.port = None
        self.route_map = {}
        self.encryptor = RpcEncryptor.new_encryptor()
        if debug:
            self.debug_sender = DebugSender(debug_port)
            self.debug(f"Debugging enabled on port {debug_port}")
            self.debug(f"Plugin Name: {self.plugin.name()}")

    def debug(self, message):
        if self.debug_sender is not None:
            self.debug_sender.write(message + "\n")

    def handle_request(self, data):
        try:
            request = json.loads(data)
            self.debug(f"request: {request}")
            if request["method"] == f"{self.plugin.name()}.Register":
                self.debug(f"Calling {request['method']} - Params: {request['params']}")
                endpoints = self.plugin.register(request["params"])
                self.debug(f"endpoints: {endpoints}")
                for endpoint in endpoints:
                    self.route_map[endpoint.function_name] = endpoint
                response = {
                    "id": request["id"],
                    "result": {
                        "Endpoints": [e.to_dict() for e in endpoints],
                    },
                    "error": None
                }
                output = json.dumps(response)
                self.debug(f"output: {output}")
                return output
            else:
                self.debug(f"Calling {request['method']} - Params: {request['params']}")
                key = request["method"].replace(f"{self.plugin.name()}.", "")
                if key in self.route_map:
                    f = self.route_map[key].function
                    input_args = InputArgs.from_dict(request["params"][0])
                    response = f(input_args)
                    output = json.dumps(response.to_dict())
                    self.debug(f"output: {output}")
                    return output
                else:
                    response = {
                        "id": request["id"],
                        "result": None,
                        "error": f"Unknown method: {request['method']}"
                    }
                    output = json.dumps(response)
                    self.debug(f"output: {output}")
                    return output
        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())

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