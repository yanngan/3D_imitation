import cv2

imgNames = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')

imgs = []
for imgName in imgNames:
    imgs.append(cv2.imread(imgName))


print(imgs)
