import yaml
import cv2 as cv

def load_yaml(path):
    with open(path, "r") as stream:
        try:
            content = yaml.load(stream, Loader=yaml.FullLoader)
            return content
        except yaml.YAMLError as exc:
            print(exc)


def create_video_capture(input_video_path):
    cap = cv.VideoCapture(input_video_path)
    assert cap.isOpened(), "Could not open video file"
    return cap