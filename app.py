# Created by Jacques Roubaud on 2021-06-24
#
# 
import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import base64
import io
import cv2
import numpy as np
import json
import importlib.util
import yaml

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def runFunction():
    # img = cv2.imread("C:/Users/r389095/OneDrive - Volvo Group/FlaskAPI/static/images/test.JPG")
    print('\n***** REQUEST RECEIVED ******')
    print(request)
    codes = request.json
    code_func = codes["script"]
    code_version = codes['version']
    base64_image = codes["img"]

    # PROCESSING OF THE REQUEST
    if code_func is not None and code_version is not None and base64_image is not None:
        # Decoding the image and saving the RAW image (that is optional, only for debug purpose)
        with open('decoded_image.png', 'wb') as file_to_save:
            im_bytes = base64.b64decode(base64_image)
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_ANYCOLOR)
            cv2.imwrite('RAW.jpg', img)

        # Now we fetch the processing function given in parameters
        try:
            data_func = pyaml["_10_trad_cv"][code_func][code_version]
        except:
            return "code fonction " + str(code_func) + " and/or code version " + str(code_version) + " are not correct"
            quit()

        scriptname = data_func["scriptname"]
        path = data_func["path"]
        fct = data_func["function"]

        # We execute the function
        spec = importlib.util.spec_from_file_location(scriptname, path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        function = getattr(script, fct) # run the associated function defined in the .yaml file
        img_result, val, message = function(img)

        # We store the result as image (optional) ond convert it to base64
        cv2.imwrite('RESULT.jpg', img_result)
        _, img_bytes = cv2.imencode(".jpg", img_result)
        img_str = np.array(img_bytes).tobytes()
        encoded_image = base64.b64encode(img_str).decode("utf-8")
        print (os. getcwd())
        
        # we send back the response json
        return jsonify({"angle":str(val), "message": message, "img_result":encoded_image})
    else:
        return "code fonction " + str(code_func) + " and/or code version " + str(code_version) + " are not correct and/or image is not coorect or empty (must be base64 encoded)"


if __name__ == "__main__":
    # Load of the catalog of functions
    yamlfile = open("repo_function.yaml")
    pyaml = yaml.load(yamlfile, Loader=yaml.FullLoader)
    
    app.run()