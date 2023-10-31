import os
from fer import FER
import cv2
from statistics import mode
from collections import deque
import numpy
import sounddevice
import argparse
import pyvirtualcam
from PIL import Image
import logging
import threading
import time

parser = argparse.ArgumentParser(
    description="A vtuber program with emotion recognition",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog="python -m is_that_you"
)
parser.add_argument("--volume-threshold", "-v", default=10, type=int, help="the amount of volume from your microphone after which the mouth will open")
parser.add_argument("--emotion-stabilization-frames-amount", "-esfa", default=3, type=int, help="the amount of recent frames that are used to calculate the most frequent emotion. This is used to prevent one-off incorrect emotion recognition. Higher numbers lead to more accurate recognition, but it will take more time for the emotion to switch")
parser.add_argument("--video-capture-device-identifier", "-vcdi", default=0, type=int, help="the identifier of the camera device that will be used for capturing emotions")
parser.add_argument("--emotion-recognition-delay", "-erd", default=0, type=int, help="the delay between the frames of emotion recognition. Might help with CPU overheating")
parser.add_argument("--device", "-d", type=str, help="the camera device to use", default=None)
parser.add_argument("--backend", "-b", type=str, help="the camera backend to use", default=None)
parser.add_argument("--debug", action="store_true", help="whether the debug logging is enabled or not")
parser.add_argument("--path", "-p", default=".", help="the path to the image batch")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

current_mouth_state = "closed"
current_emotion = "neutral"
last_sent_image_name = None

width_height = None
images = {}

def make_image_name(emotion: str, mouth_state: str):
    return f"{emotion}_mouth_{mouth_state}"

for emotion in ("anger", "disgust", "fear", "happy", "sad", "surprise", "neutral"):
    for mouth_state in ("closed", "open"):
        image_name = make_image_name(emotion, mouth_state)
        file_name = f"{image_name}.png"
        file_path = os.path.join(args.path, file_name)
        try:
            image = Image.open(file_path)
        except FileNotFoundError:
            continue
        new_width_height = (image.width, image.height)
        if width_height is None:
            width_height = new_width_height
        elif width_height != new_width_height:
            raise Exception(f"inconsistent image sizes: expected {width_height}, got {new_width_height}")
        images[image_name] = numpy.asarray(image)

if width_height is None:
    raise Exception("no images were found in the specified path")
width, height = width_height

class ImageNotFound(Exception):
    pass

with pyvirtualcam.Camera(width=width, height=height, fps=60, device=args.device, backend=args.backend) as cam:
    logging.debug("Connected the camera using the device %s!", cam.device)

    def update_view_if_possible():
        try:
            update_view()
        except ImageNotFound:
            pass

    def update_view():
        global last_sent_image_name
        image_name = make_image_name(current_emotion, current_mouth_state)
        if image_name == last_sent_image_name:
            return
        try:
            image = images[image_name]
        except KeyError:
            raise ImageNotFound
        logging.debug(f"setting the {image_name} image!")
        cam.send(image)
        last_sent_image_name = image_name

    def process_sound(frames: numpy.ndarray):
        global current_mouth_state
        volume_norm = numpy.linalg.norm(frames)
        new_mouth_state = "open" if volume_norm > args.volume_threshold else "closed"
        logging.debug(f"microphone volume: {volume_norm}, mouth state: {new_mouth_state}")
        if current_mouth_state != new_mouth_state:
            logging.debug(f"setting the '{new_mouth_state}' mouth state!")
            current_mouth_state = new_mouth_state
            update_view_if_possible()

    time_to_die = False
    def listen_to_sound():
        while True:
            frames, _overflowed = microphone_input_stream.read(int(audio_frames_per_second * 0.1))
            process_sound(frames)
            if time_to_die:
                break

    microphone_input_stream = sounddevice.InputStream()
    microphone_input_stream.start()

    audio_frames_per_second = microphone_input_stream.samplerate

    try:
        update_view()
    except ImageNotFound:
        raise Exception(f"the image for the default emotion ({make_image_name(current_emotion, current_mouth_state)}) is not present. Provide it")

    detector = FER()
    real_camera = cv2.VideoCapture(args.video_capture_device_identifier)
    recent_emotions = deque(maxlen=args.emotion_stabilization_frames_amount)

    sound_listening_thread = threading.Thread(target=listen_to_sound)
    sound_listening_thread.start()

    try:
        while True:
            ret, frame = real_camera.read()
            if not ret:
                break
            emotion, score = detector.top_emotion(frame)
            logging.debug(f"emotion: {emotion}, score: {score}")
            if emotion is not None:
                recent_emotions.append(emotion)
                probable_emotion = mode(recent_emotions)
                if current_emotion != probable_emotion:
                    logging.debug(f"setting the '{probable_emotion}' emotion!")
                    current_emotion = probable_emotion
                    update_view_if_possible()
            time.sleep(args.emotion_recognition_delay)
    finally:
        time_to_die = True
        sound_listening_thread.join()
