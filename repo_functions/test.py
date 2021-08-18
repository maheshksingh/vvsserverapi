import cv2
import numpy as np
import math

# This function is "image processing", called by the API server to proces sincoming image
# this one only adds "OK" to the picture, and responds with the modified picture and 999 as value, and "no message" as message

def F123456_test(image_source):

    cv2.putText(image_source, 'OK',
            (150 , 300),
            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 5)
   

    return image_source, 999, "no message"





# EXECUTE
if __name__ == "__main__":

    img = cv2.imread("test.jpg")
    output, result = F123456_test(img)
    cv2.imwrite('test_result.jpg', output)

