# import requests
# import socketio

# class TieUiNameSpace(socketio.ClientNamespace):
#     def __init__(self, namespace, adk):
#         super().__init__(namespace)
#         self.adk = adk
#     def on_connect(self):
#         print('Connected to namespace:', self.namespace)

#     def on_disconnect(self):
#         print('Disconnected from namespace:', self.namespace)

#     def on_callBack(self, item):
#         print("CALLBACK RECEIVED:", item)
#         callback_id = item.get("componentId")
#         if callback_id and callback_id in self.adk.component_callbacks:
#             self.adk.component_callbacks[callback_id](item)
#         elif self.adk.execute_callback:  # default callback
#             self.adk.execute_callback(item)


# class TieUi:
#     def __init__(self, execute_callback=None):
#         self.components = []
#         self.sio = socketio.Client()
#         self.component_callbacks = {}
#         self.execute_callback = execute_callback

#         @self.sio.event
#         def connect():
#             print('Connected to Flask server.')

#         @self.sio.event
#         def disconnect():
#             print('Disconnected from Flask server.')

#         @self.sio.on('callBack')
#         def on_execute_callback(item):
#             print("executing callback")
#             callback_id = item["componentId"]
#             if callback_id and callback_id in self.component_callbacks:
#                 self.component_callbacks[callback_id](item)
#             elif self.execute_callback:  # default callback
#                 self.execute_callback(item)

#         # Connect to the Flask server upon initialization
#         self.sio.connect('http://localhost:8080')


#     def add(self, component):
#         self.components.append(component)
#         return self

#     def textBox(self, settings, callback=None):
#         # Translates Python settings to necessary JSON for React
#         component =  {"type": "textBox", "settings": settings}
#         if callback:
#             component_id = f"textBox_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def select(self, settings, callback=None):
#         component = {"type": "select", "settings": settings}
#         if callback:
#             component_id = f"select_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def button(self, settings, callback=None):
#         component = {"type": "button", "settings": settings}
#         if callback:
#             component_id = f"button_{len(self.components)}"
#             self.component_callbacks[component_id] = callback
#             component["callback_id"] = component_id
#         return component

#     def dataViz(self, chart):
#         return {"type": "dataViz", "settings": chart}
    
#     def publish(self):
#         response = requests.post("http://localhost:8080/publish", json=self.components)
#         self.wait_for_events()
#         return response.json()
    
#     def update(self):
#         self.publish()
    
#     def wait_for_events(self):
#         # To keep the script running and listening for events
#         try:
#             self.sio.wait()
#         except KeyboardInterrupt:
#             print("Interrupted by user.")
#             self.sio.disconnect()


import inspect
import os
import requests
import socketio
import time
import inspect
import json


url = 'http://172.105.148.14'
url = 'http://localhost:8080'
url = 'https://tieui-5c69a6002efd.herokuapp.com/'

class TieUiNameSpace(socketio.ClientNamespace):
    def __init__(self, namespace, adk):
        super().__init__(namespace)
        self.adk = adk
    def on_connect(self):
        print('Connected to namespace:', self.namespace)

    def on_disconnect(self):
        print('Disconnected from namespace:', self.namespace)

    def on_callBack(self, item):
        print("CALLBACK RECEIVED:", item)
        callback_id = item.get("componentId")
        if callback_id and callback_id in self.adk.component_callbacks:
            self.adk.component_callbacks[callback_id](item)
        elif self.adk.execute_callback:  # default callback
            self.adk.execute_callback(item)


class TieUi:
    def __init__(self, app_name, execute_callback=None):
        self.components = []
        self.app_name = app_name
        self.sio = socketio.Client()
        self.component_callbacks = {}
        self.execute_callback = execute_callback
        self.layout_data = self._load_layout_data()


        # Create and register custom namespace
        self.namespace = TieUiNameSpace('/' + app_name, self)
        self.sio.register_namespace(self.namespace)

        # Connect to the Flask server upon initialization
        self.sio.connect('https://tieui-5c69a6002efd.herokuapp.com/', namespaces=['/' + app_name])

    def _load_layout_data(self):
        print("inside layout data")
        """
        Load layout data from the saved JSON file.
        """
        layout_file_path = f'./{self.app_name}_layout.json'
        print(layout_file_path)

        try:
            with open(layout_file_path, 'r') as layout_file:
                return json.load(layout_file)
        except FileNotFoundError:
            return {}  # return an empty dict if the layout file doesn't exist

    # ------------------- COMPONENTS ------------------

    def textBox(self, settings, callback=None):
        # Translates Python settings to necessary JSON for React
        component =  {"type": "textBox", "settings": settings}
        if callback:
            component_id = f"textBox_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def select(self, settings, callback=None):
        component = {"type": "select", "settings": settings}
        if callback:
            component_id = f"select_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def button(self, settings, callback=None):
        component = {"type": "button", "settings": settings}
        if callback:
            component_id = f"button_{len(self.components)}"
            self.component_callbacks[component_id] = callback
            component["callback_id"] = component_id
        return component

    def dataViz(self, chart):
        return {"type": "dataViz", "settings": chart}
    
    def barChart(self, settings):
        component = {"type": "barChart", "settings": settings}
        return component
    
    def lineChart(self, settings):
        component = {"type": "lineChart", "settings": settings}
        return component
    
    def label(self, settings):
        component = {"type": "label", "settings": settings}
        return component

    # ----------------- FUNCTIONS -------------------

    def add(self, component):
        self.components.append(component)
        return self
    
    def publish(self, script_code=None):
        styling = self._load_layout_data()
        
        if script_code is not None:
            # If script_code is provided, use it
            response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling})
        else:
            # If script_code is not provided, try to retrieve it from __main__
            try:
                import __main__
                script_code = open(__main__.__file__).read()
                response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling})
            except AttributeError:
                response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": 'N/A', "styling": styling})

                # raise Exception("script_code is not provided, and __main__ module has no __file__ attribute.")

        self.wait_for_events()
        return response.json()

    
    def publishFromAi(self, script_code=None):
        print("punlishing from AI")
        print(self.app_name)
        print(self.components)         
        response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": ""})
        self.wait_for_events()
        return response.json()
    
    def update(self):
        self.publish()
    
    def liveUpdate(self, script_code=None):
        if script_code is None:
            # If script_code is not provided, get the code of the current module
            script_code = inspect.getsource(self.__class__)

        import __main__
        script_code = open(__main__.__file__).read()
        
        styling = self._load_layout_data()
        print(styling)
        response = requests.post(f"{url}/publish/{self.app_name}", json={"components": self.components, "code": script_code, "styling": styling})
        # self.wait_for_events()
        return response.json()

    def registerApp(self):
        print('register')
        print(self.app_name)
        response = requests.post(f"{url}/register-app/{self.app_name}", json=self.components)
        time.sleep(5)
        return response.json()
    
    def wait_for_events(self):
        # To keep the script running and listening for events
        try:
            self.sio.wait()
        except KeyboardInterrupt:
            print("Interrupted by user.")
            self.sio.disconnect()


    # ----------------- HELPER -----------------
    @staticmethod
    def _get_calling_script_code():
        # Get the frame of the caller (the script that imports and uses the TieUi class)
        caller_frame = inspect.currentframe().f_back

        # Get the filename of the calling script
        calling_script_file = caller_frame.f_globals['__file__']

        # Get the absolute path of the calling script
        calling_script_path = os.path.abspath(calling_script_file)

        # Read the contents of the calling script
        with open(calling_script_path, 'r') as script_file:
            script_code = script_file.read()

        return script_code