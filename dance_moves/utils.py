import cv2
from settings import BODY_SEGMENTS, BODYPART_INDEX


def angle_to_bodyparts(angle_names=[]):
    bodyparts = []
    for angle_name in angle_names:
        for key, value in BODY_SEGMENTS.items():
            if key in angle_name:
                bodyparts.append(key)
    return bodyparts


def bodyparts_to_angles(bodyparts_names=[]):
    angles = []
    for bodypart in bodyparts_names:
        for key, value in BODYPART_INDEX.items():
            if bodypart in value:
                angles.append(value)
    return angles


def angles_to_ids(angle_names=[]):
    ids = []
    for angle_name in angle_names:
        for key, value in BODYPART_INDEX.items():
            if angle_name == value:
                ids.append(key)
    ids.sort()
    return ids


def angle_ids_to_angles(angle_ids=[]):
    angles = []
    angle_ids.sort()
    for id in angle_ids:
        angles.append(BODYPART_INDEX[id])
    return angles


def bodyparts_to_ids(bodyparts_names=[]):
    ids = []
    for bodypart in bodyparts_names:
        ids.append(BODY_SEGMENTS[bodypart][0])
        ids.append(BODY_SEGMENTS[bodypart][1])
    ids = list(set(ids))
    ids.sort()
    return ids


def update_selected_state(state={'angles': [], 'bodyparts': []}, angle_names=[], bodypart_names=[]):
    new_bodyparts = angle_to_bodyparts(angle_names)
    new_angles = bodyparts_to_angles(bodypart_names)
    state['bodyparts'] = list(set(state['bodyparts'] + new_bodyparts + bodypart_names))
    state['angles'] = list(set(state['angles'] + new_angles + angle_names))
    return state


def calculate_timestamps(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

    while(cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        else:
            break

    cap.release()
    return timestamps
