from . import make_component,sg
from abstract_utilities import create_new_name
class AbstractWindowManager:
    def __init__(self):
        self.global_windows = {}
        self.current_window = None  # you can change this as per the window you're working with
        self.event = None
        self.values = None
        self.undesignated_value_keys = []
    def _get_screen_size(self):
        return sg.Window.get_screen_size()
    def add_window(self, window_name=None, title=None, default_name=True, 
                   match_true=False, max_size=None,set_current=True, *args, **kwargs):
        window_name = create_new_name(name=window_name, names_list=list(self.global_windows.keys()), 
                                      default=default_name, match_true=match_true)
        if title is None:
            title = window_name

        screen_width, screen_height = self._get_screen_size()

        # Ensure we have valid screen dimensions
        if screen_width is None or screen_height is None:
            raise ValueError("Could not determine screen dimensions.")
        
        # If max_size is specified and valid, use it. Otherwise, default to screen dimensions.
        if max_size and isinstance(max_size, tuple) and len(max_size) == 2 and \
           isinstance(max_size[0], int) and isinstance(max_size[1], int):
            max_width, max_height = max_size
        else:
            max_width, max_height = screen_width, screen_height

        # Check size in kwargs
        w, h = kwargs.get("size", (max_width, max_height))

        # Ensure w and h are not None
        w = w if w is not None else max_width
        h = h if h is not None else max_height

        # Update the size in kwargs
        kwargs["size"] = (min(w, max_width), min(h, max_height))

        self.global_windows[window_name] = make_component('Window', title=title, *args, **kwargs)
        if set_current:
            self.set_current_window(window_name = window_name)
        return window_name
    def close_window(self, window_name):
            if window_name in self.global_windows:
                self.global_windows[window_name].close()  # Assuming your window object has a close method
                del self.global_windows[window_name]
    def set_current_window(self, window_name):
            self.current_window = self.get_window(window_name)
    def get_window(self,window_name=None):
        if window_name == None:
            if self.current_window == None:
                print("No current window set!")
                return None
            return self.current_window
        window = self.global_windows.get(window_name)
        if window == None:
            print(f"window_name {window_name} not in global_windows")
            window=self.current_window
        return window
    def append_output(self,key,new_content):
        content = self.get_from_value(key)+'\n\n'+new_content
        self.update_value(key=key,value=content)
    def update_value(self, key, value=None, args=None):
        if self.current_window:
            if args:
                self.current_window[key].update(**args)
            else:
                self.current_window[key].update(value=value)
        else:
            print("No current window set!")

    def read_window(self):
        if self.current_window:
            self.event, self.values = self.current_window.read()
            return self.event, self.values
        else:
            print("No current window set!")
            return None, None

    def get_event(self):
        if not self.event:
            self.read_window()
        return self.event
    
    def get_values(self):
        if not self.values:
            self.read_window()
        return self.values
    def get_from_value(self,key,default=None,delim=None):
        self.get_values()
        if key not in self.values:
            print(f'{key} has no value')
            if key not in self.undesignated_value_keys:
                self.undesignated_value_keys.append(key)
                print('undesignated_value_keys: \n',self.undesignated_value_keys)
            return
        value = self.values[key]
        if delim != None:
            if value == delim:
                return default
        return value
