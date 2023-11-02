import subprocess,time
import json,os
dllname = 'VCIQcap.dll'
exe_path= os.path.dirname(os.path.abspath(__file__))+os.path.sep+dllname
outfile='IQ.txt'

# Define a decorator function
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to run")
        return result
    return wrapper

class iqset():
    """
   Initializes an IQ settings class with default values for various parameters.
        The class allows you to manage and interact with IQ settings.

    """
    def __init__(self):
        self.iq =  {
                        "zoom": "128",
                        "brightness": "128",
                        "contrast": "128",
                        "saturation": "128",
                        "whitebalance": "3000",
                        "backlight": "1",
                        "gain": "0",
                        "exposure": "-1",
                        "focus": "0",
                        "sharpness": "128",
                        "pan": "0",
                        "tilt": "0",
                         "FriendlyName":""
                    }

        # Methods to set IQ settings
    def set_zoom(self, value):
        self.iq["zoom"] = value
        self.set_iq()

    def set_brightness(self, value):
        self.iq["brightness"] = value
        self.set_iq()

    def set_contrast(self, value):
        self.iq["contrast"] = value
        self.set_iq()

    def set_saturation(self, value):
        self.iq["saturation"] = value
        self.set_iq()

    def set_whitebalance(self, value):
        self.iq["whitebalance"] = value
        self.set_iq()

    def set_backlight(self, value):
        self.iq["backlight"] = value
        self.set_iq()

    def set_gain(self, value):
        self.iq["gain"] = value
        self.set_iq()

    def set_exposure(self, value):
        self.iq["exposure"] = value
        self.set_iq()

    def set_focus(self, value):
        self.iq["focus"] = value
        self.set_iq()

    def set_sharpness(self, value):
        self.iq["sharpness"] = value
        self.set_iq()

    def set_pan(self, value):
        self.iq["pan"] = value
        self.set_iq()

    def set_tilt(self, value):
        self.iq["tilt"] = value
        self.set_iq()

        # Methods to get IQ settings
    def get_zoom(self):
        self.reading_iq()
        return self.iq["zoom"]

    def get_brightness(self):
        self.reading_iq()
        return self.iq["brightness"]

    def get_contrast(self):
        self.reading_iq()
        return self.iq["contrast"]

    def get_saturation(self):
        self.reading_iq()
        return self.iq["saturation"]

    def get_whitebalance(self):
        self.reading_iq()
        return self.iq["whitebalance"]

    def get_backlight(self):
        self.reading_iq()
        return self.iq["backlight"]

    def get_gain(self):
        self.reading_iq()
        return self.iq["gain"]

    def get_exposure(self):
        self.reading_iq()
        return self.iq["exposure"]

    def get_focus(self):
        self.reading_iq()
        return self.iq["focus"]

    def get_sharpness(self):
        return self.iq["sharpness"]

    def get_pan(self):
        self.reading_iq()
        return self.iq["pan"]

    def get_tilt(self):
        self.reading_iq()
        return self.iq["tilt"]

    def change_json(self,json_enable=False):
        # Step 1: Read the Text File
        with open(outfile, 'r') as text_file:
            text_data = text_file.read()


        lines = text_data.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                self.iq[key.strip()] = value.strip()

        # Step 3: Convert the Dictionary to JSON
        if json_enable:
            json_data = json.dumps(self.iq, indent=4)

            # Step 4: Write to a JSON File
            with open('IQ.json', 'w') as json_file:
                json_file.write(json_data)
        if os.path.isfile(outfile):
            os.remove(outfile)
        return self.iq

    @measure_time
    def reading_iq(self):
        arguments = ['-iqr']
        try:
            result = subprocess.run([exe_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("Error calling the executable:", e)
        except FileNotFoundError:
            print("Executable not found at the specified path:", exe_path)

        iq=self.change_json()
        return iq

    @measure_time
    def set_iq(self,iqset=None,default=False):
        if iqset is not None:
            for key, value in iqset.items():
                if key in self.iq:
                    self.iq[key] = value
        arguments = ['-iq']+[value for value in self.iq.values()]
        try:
            if default:
                arguments = ['-iqd']
                result = subprocess.run([exe_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            else:
                result = subprocess.run([exe_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        except subprocess.CalledProcessError as e:
            print("Error calling the executable:", e)
        except FileNotFoundError:
            print("Executable not found at the specified path:", exe_path)

        return arguments

if __name__ == "__main__":
    test=iqset()
    #test.set_exposure("-2")
    iq1 = {
        "zoom": "120",
        "brightness": "120",
        "contrast": "119",
        "saturation": "120",
        "whitebalance": "4000",
        "gain": "0",
        "exposure": "-8",
        "focus": "2",
        "sharpness": "120",
        "pan": "-1",
        "tilt": "-2",
        "FriendlyName": "Logitech BRIO"
    }
    #test.set_whitebalance("3000")
    #test.set_pan("-3")
    #test.set_iq(None,True)
    test.set_iq(iq1)
    #print(test.reading_iq())
    #print(test.reading_iq())
