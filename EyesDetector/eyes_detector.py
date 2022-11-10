import cv2

imgNames = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')

base_path = "../Assets/"
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

imgs = []
for imgName in imgNames:
    imgs.append(cv2.imread(base_path + imgName))

for i in range(0, 5):
    eyes = eye_cascade.detectMultiScale(imgs[i], scaleFactor=1.2)
    for (x, y, w, h) in eyes:
        cv2.rectangle(imgs[i], (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.imshow("Eyes Detected", imgs[i])


cv2.waitKey(0)
cv2.destroyAllWindows()




