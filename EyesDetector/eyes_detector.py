import cv2


# https://www.etutorialspoint.com/index.php/324-eye-detection-program-in-python-opencv


imgNames = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')

base_path = "../Assets/"



def eyes_detect(img_full_name):
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    img = cv2.imread(img_full_name)
    eyes = eye_cascade.detectMultiScale(img, scaleFactor=1.2)
    if eyes.shape[0] != 2:
        print("Error in img " + img_full_name + " found " + str(eyes.shape[0]) + "eyes")
        raise Exception("Error in img " + img_full_name + " found " + str(eyes.shape[0]) + "eyes")
    eyes_coordinates = []
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        x_center = int(x + (w/2))
        y_center = int(y + (h/2))
        image = cv2.circle(img, (x_center, y_center), radius=5, color=(0, 0, 255), thickness=-1)
        # cv2.imshow("Eyes Detected " + str(i), imgs[i])
        print(img_full_name + ": eye location (" + str(x_center) + " , " + str(y_center) + ") ")
        eyes_coordinates.appentd((x_center,y_center))

    return eyes_coordinates
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




