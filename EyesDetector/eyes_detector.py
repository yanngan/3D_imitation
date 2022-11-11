import cv2

imgNames = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')

base_path = "../Assets/"

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

imgs = []
for imgName in imgNames:
    imgs.append(cv2.imread(base_path + imgName))

for i in range(0, 5):
    eyes = eye_cascade.detectMultiScale(imgs[i], scaleFactor=1.2)
    if(eyes.shape[0]!= 2):
        print("Error in img i="+str(i)+" found "+str(eyes.shape[0])+"eyes")
        continue
    for (x, y, w, h) in eyes:
        cv2.rectangle(imgs[i], (x, y), (x + w, y + h), (0, 255, 0), 5)
        x_center = int(x + (w/2))
        y_center = int(y + (h/2))
        image = cv2.circle(imgs[i], (x_center, y_center), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow("Eyes Detected " + str(i), imgs[i])

cv2.waitKey(0)
cv2.destroyAllWindows()




