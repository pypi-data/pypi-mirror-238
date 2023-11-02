from . import make_component,sg
from abstract_utilities import create_new_name
class AbstractWindowManager:
    def __init__(self):
        self.global_windows = []
        self.closed_windows = []
        self.undesignated_value_keys = []
    def _get_screen_size(self):
        return sg.Window.get_screen_size()
    def add_window(self, window_name=None, title=None, default_name=True, 
                   match_true=False, max_size=None,set_current=True,height=0.90,width=0.90, *args, **kwargs):
        window_name = create_new_name(name=window_name, names_list=self.get_window_info_list(key="name"), 
                                      default=default_name, match_true=match_true)
        if title is None:
            title = window_name

        screen_width, screen_height = self._get_screen_size()

        # Ensure we have valid screen dimensions
        if screen_width is None or screen_height is None:
            raise ValueError("Could not determine screen dimensions.")
        else:
            screen_width = int(screen_width*width)
            screen_height = int(screen_height*height)
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
        current = False
        if len(self.global_windows) == 0 or set_current:
            current = True
        self.global_windows.append({"name":window_name,"method":make_component('Window', title=title, *args, **kwargs),"event":False,"values":False,"current":current})

        return window_name     
    def close_window(self, window_name=None,window=None):
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration !=None:
            self.global_windows[window_enumeration]["method"].close()  # Assuming your window object has a close method
            new_global_windows = []
            for i,window_values in enumerate(self.global_windows):
                if i == window_enumeration:
                    self.closed_windows.append(window_values)
                else:
                    new_global_windows.append(window_values)
            self.global_windows=new_global_windows
    def get_window(self,window_name=None,window=None):
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        return self.global_windows[window_enumeration]["method"]
    def append_output(self,key,new_content,window_name=None,window=None):
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            content = self.get_from_value(key=key,window_name=window_name,window=window)+'\n\n'+new_content
            self.update_value(key=key,value=content,window_name=window_name,window=window)
    def update_value(self, key, value=None, args=None,window_name=None,window=None,):
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            window = self.global_windows[window_enumeration]['method']
            values = self.get_values(window_name=window,window=window)
            if key in values:
                if args:
                    window[key].update(**args)
                else:
                    window[key].update(value=value)
### current_window
    def set_current_window(self, window):
        window_enumeration = self.get_any_enumeration(window_name=window,window=window,current_window=True)
        for i,window_info in enumerate(self.global_windows):
            bool_it=False
            if i == window_enumeration:
                bool_it =True
            self.global_windows[i]["current"] = bool_it
    def get_current_window(self):
        for i,window_info in enumerate(self.global_windows):
            if self.global_windows[i]["current"]==True:
                return i
### enumerate value in global window list
    def check_window_value(self,key,value):
        i=self.enumerate_list(list_obj=self.global_windows,key=key,value=value)
        if i != None:
            return i
    def get_window_info_list(self,key=None):
        info_list=[]
        for window_info in self.global_windows:
            info_list.append(window_info[key])
        return info_list
    def enumerate_list(self,list_obj,key,value):
        for i,values in enumerate(list_obj):
            if values[key] == value:
                return i
    def get_any_enumeration(self,window_name=None,window=None,current_window=True):
        json_check = {"name":window_name,"method":window}
        if current_window:
            json_check["current"]=True
 
        for key,value in json_check.items():
            if value != None:
                window_enumeration = self.check_window_value(key,value)
                if window_enumeration != None:
                    return window_enumeration
### get window method
    def get_window_method(self,window):
        window_enumeration = self.get_any_enumeration(window_name=window,window=window,current_window=False)
        if window_enumeration:
            return self.global_windows[window_enumeration]["method"]
### window read
    def update_read_values(self,enumeration):
        window_method = self.global_windows[enumeration]["method"]
        event,values = window_method.read()
        json_check = {"event":event,"values":values}
        for key,value in json_check.items():
            self.global_windows[enumeration][key]=value
        if event == None:
            self.close_window(window=window_method)
        return event,values
    def read_window(self,window_name=None,window=None):
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration != None:
           return self.update_read_values(window_enumeration)
        else:
            print("No current window set!")
            return None, None
        
### window event and values
    def get_window_info(self,key,window_name=None,window=None):
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            values = self.global_windows[window_enumeration][key]
            if not values:
                self.read_window(window=self.global_windows[window_enumeration]["method"])
            return self.global_windows[window_enumeration][key]
    
    def get_event(self,window_name=None,window=None):
        return self.get_window_info("event",window_name=window_name,window=window)
    def get_values(self,window_name=None,window=None):
        return self.get_window_info("values",window_name=window_name,window=window)

    
    def get_from_value(self,key,default=None,delim=None,window_name=None,window=None):
        values = self.get_values(window_name=window_name,window=window)
        if key not in values:
            print(f'{key} has no value')
            if key not in self.undesignated_value_keys:
                self.undesignated_value_keys.append(key)
                print('undesignated_value_keys: \n',self.undesignated_value_keys)
            return
        value = values[key]
        if delim != None:
            if value == delim:
                return default
        return value
    def expand_elements(self, window_name=None, window=None, element_keys=None):
            """
            Expand the specified elements in the window.

            Args:
            - window_name (str, optional): The name of the window.
            - window (object, optional): Direct window object.
            - element_keys (list, optional): List of keys of the elements to be expanded.
            """
            # Get the window using its name or direct object
            target_window = self.get_window(window_name=window_name, window=window)
            
            # If no element_keys are provided, use the default set of keys
            default_keys = ['-TABGROUP-', '-ML CODE-', '-ML DETAILS-', '-ML MARKDOWN-', '-PANE-']
            element_keys = element_keys or default_keys
            
            # Expand the elements
            for key in element_keys:
                if key in target_window:
                    target_window[key].expand(True, True, True)
