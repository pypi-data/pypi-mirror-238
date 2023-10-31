import os
import logging
import threading
import queue
import uuid
import subprocess
import re, ast, json, glob

import flask
from flask import Flask
import h5py

##### OS dependent codes #####
def find_executable_path():
    exe_path = None
    path_candidates = glob.glob("/Applications/Igor Pro*/Igor64.app/Contents/MacOS/Igor64")
    assert len(path_candidates) > 0, "Cannot find Igor Pro"
    exe_path = path_candidates[0]
    return exe_path

def convert_to_igor_path(path):
    return path.replace(os.path.sep, ":")
##### OS dependent codes #####


class Connection:
    TIMEOUT = 3
    ### security_hole options makes it possible to execute any Python code by HTTP requests. Do not use unless you are sure of it.
    def __init__(self, port=15556, security_hole=False, timeout=3):
        self._app = Flask(__name__)
        self._task_queue = queue.Queue(maxsize=1)
        self._queue = queue.Queue(maxsize=1)
        self._port = port
        self._registered_functions = {"get": self.get, "put": self.put, "print": print}
        self._basepath = os.getcwd()
        self._executable_path = find_executable_path()
        self._security_hole = security_hole
        self.TIMEOUT = timeout
        
        self._register_route()
        threading.Thread(target=self._run_server, daemon=True).start()

    def reset(self):
        try:
            self._queue.put_nowait(("error", 0))
        except:
            pass
        try:
            self._queue.get_nowait()
        except:
            pass
        try:
            self._task_queue.get_nowait()
        except:
            pass

    def __call__(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        for c in commands:
            c = c.replace("'", "\"")
            self.execute_command(c)    
    
    def get(self, wavename):
        uid = uuid.uuid1().hex
        try:
            self._task_queue.put(("get", uid), timeout=self.TIMEOUT)
        except queue.Full:
            return
        
        self.execute_command(f"PyIgorOutputWave({self._port}, \"{uid}\", \"{wavename}\", \"{self._temp_path(True)}\")")
        result = None
        try:
            reply = self._queue.get(timeout=self.TIMEOUT)
            if reply[0] == "ok":
                assert reply[1] == uid, "Error: Request-response ID does not match."
                result = Wave.from_dict(reply[2])
            
        except queue.Empty:
            pass
        assert self._task_queue.get_nowait() == ("get", uid)
        return result

    def put(self, wave, wavename="", x0=0, dx=1):
        uid = uuid.uuid1().hex
        try:
            self._task_queue.put(("put", uid), timeout=self.TIMEOUT)
        except queue.Full:
            return
        with h5py.File(self._temp_path(), "w") as f:
            dset = f.create_dataset(uid, data=wave)
        self.execute_command(f"PyIgorLoadWave({self._port}, \"{uid}\", \"{wavename}\", \"{self._temp_path(True)}\", 0)")
        try:
            result = self._queue.get(timeout=self.TIMEOUT)
        except queue.Empty:
            result = None
        assert self._task_queue.get_nowait() == ("put", uid)
        return result

    def _run_server(self):
        log = logging.getLogger('werkzeug') 
        log.setLevel(logging.ERROR)
        flask.cli.show_server_banner = lambda *args: None
        self._app.run(port=self._port)
        
    def _register_route(self):
        @self._app.route("/")
        def index():
            return "<p>Bridging Igor and Python</p>"

        @self._app.route("/msg/<string:msg>/<string:uid>")
        def got_message(msg, uid):
            if msg == "get":
                result = self._process_get(uid)
                self._queue.put_nowait(result)
            if msg == "put":
                self._queue.put_nowait(("ok", uid))
            if msg == "error":
                self._queue.put_nowait(("error", uid))
            return "<p>Bridging Igor and Python</p>"

        @self._app.route("/call/<string:commands>")
        def call_command(commands):
            result_list = []
            p = re.compile(r"([\w]+)\(([^\)]*)\)")
            for command in commands.split(";"):
                try:
                    if self._security_hole:
                        result_list.append(eval(command)) # eval is used to execute any Python code.
                    else:
                        m = re.match(p, command)
                        if m is None:
                            continue
                        fname, args = m.groups()
                        args = ast.literal_eval(f"[{args}]")
                        if fname in self._registered_functions:
                            result_list.append(self._registered_functions[fname](*args))
                except Exception as e:
                    print(e)
                    result_list.append(f"error:{command}")
            return ";".join([str(x) for x in result_list if x is not None])

    def _process_get(self, uid):
        with h5py.File(self._temp_path(), mode="r") as f:
            result_dict = {"array": f[uid][...]}
        return ("ok", uid, result_dict)
    
    def _temp_path(self, for_igor=False):
        path = os.path.join(self._basepath, f"temp_pyigor_{self._port}.h5")
        if for_igor:
            path = convert_to_igor_path(path)
        return path

    
    def execute_command(self, command):
        subprocess.run([self._executable_path, "-Q", "-X", command])

    def wait_done(self):
        try:
            while True:
               if input("Input q to finish:") == "q":
                   break
        except KeyboardInterrupt:
            pass
    
    ### Wrapper functions ###
    def function(self, f):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        self._registered_functions[f.__name__] == f
        return wrapper

class Wave:
    def __init__(self, array):
        self.array = array
        self.offsets = 0
        self.deltas = 1
        self.units = None
    
    @classmethod
    def from_dict(cls, d):
        wave = Wave(d["array"])
        return wave
    
    def __str__(self):
        return f"<Wave shape:{self.array.shape}, data_type:{self.array.dtype}>"

if __name__ == "__main__":
    import code
    import numpy as np
    import pandas as pd
    
    igor = Connection()
    code.interact(local=locals())

