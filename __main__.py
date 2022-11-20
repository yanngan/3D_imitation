import sys
from GUI import frame2
from EyesDetector import eyes_detector

img_names = ('center.jpg', 'down.jpg', 'left.jpg','mid.jpg', 'right.jpg', 'up.jpg')
base_path = "../Assets/"


def main() -> int:
    frame2.draw_frame()
    for img_name in img_names:
        try:
            eyes_coordinates = eyes_detector.eyes_detect(img_name)
        except Exception as inst:
            print(inst)

    return 0


if __name__ == '__main__':
    sys.exit(main())
