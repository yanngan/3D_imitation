import sys
from EyesDetector import eyes_detector
from GUI import frame

img_names = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')
base_path = "../Assets/"


def main() -> int:
    the_frame = frame.Frame()
    the_frame.draw_frame(0, 1)
    for img_name in img_names:
        try:
            eyes_coordinates = eyes_detector.eyes_detect(img_name)
            frame.Frame.resetTaitBryanAngles
        except Exception as inst:
            print(inst)
    while 1:
        i = 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
