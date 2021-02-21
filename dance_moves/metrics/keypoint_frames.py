import os
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.3f')
import numpy as np
import pandas as pd
from settings import DATA_PATH, BODYPART_INDEX


def read_keypoints(data):
    people_column = data['people']
    for d in people_column:
        keypoints = (d["pose_keypoints_2d"])
    return keypoints


def get_keypoints(video):
    datapoints = {}

    files = []
    for i in sorted(os.listdir(DATA_PATH)):
        if os.path.isfile(os.path.join(DATA_PATH, i)) and video in i:
            files.append(i)

    frames_csv = np.ndarray([len(files),75], dtype=object)
    for i, file in enumerate(files):

        with open(os.path.join(DATA_PATH, file)) as f:
            data_f = json.load(f)
            keypoints = read_keypoints(data_f)
            frames_csv[i] = keypoints
    datapoints[video] = frames_csv

    return frames_csv


def read_keypoints(data):
    people_column = data['people']
    for d in people_column:
        keypoints = (d["pose_keypoints_2d"])
    return keypoints


def remove_confidence_interval(data):
    j = 2
    keypoints = read_keypoints(data)
    keypoints_woconfidence = keypoints.copy()
    while j <= len(keypoints_woconfidence):
        keypoints_woconfidence.pop(j)
        j += 2
    return keypoints_woconfidence


def create_y_coordicate(data):
    df = remove_confidence_interval(data)
    df = np.array(df)
    mask = np.ones(df.size, dtype=bool)
    mask[1::2] = 0
    points = df[mask]
    y = points.tolist()
    return y


def create_x_coordicate(data):
    df = remove_confidence_interval(data)
    df = np.array(df)
    mask = np.zeros(df.size, dtype=bool)
    mask[1::2] = 1
    points = df[mask]
    x = points.tolist()
    return x


def compute_angle(vector1, vector2):
    unit_vector_1 = vector1 / np.linalg.norm(vector1)
    unit_vector_2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return round(degree(angle), 2)

# ANGLE SIMILARITY

# defines the degree of an angle
import math
def degree(x):
    pi = math.pi
    degree = (x * 180) / pi
    return degree

def getAngle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def compute_angle_vector(data):
    x = create_x_coordicate(data)
    y = create_y_coordicate(data)

    nose = [x[0], y[0]]
    neck = [x[1], y[1]]
    right_shoulder = [x[2], y[2]]
    right_elbow = [x[3], y[3]]
    right_wrist = [x[4], y[4]]
    left_shoulder = [x[5], y[5]]
    left_elbow = [x[6], y[6]]
    left_wrist = [x[7], y[7]]
    midhip = [x[8], y[8]]
    right_hip = [x[9], y[9]]
    right_knee = [x[10], y[10]]
    right_ankle = [x[11], y[11]]
    left_hip = [x[12], y[12]]
    left_knee = [x[13], y[13]]
    left_ankle = [x[14], y[14]]
    right_eye = [x[15], y[15]]
    left_eye = [x[16], y[16]]
    right_ear = [x[17], y[17]]
    left_ear = [x[18], y[18]]
    left_big_toe = [x[19], y[19]]
    left_small_toe = [x[20], y[20]]
    left_heel = [x[21], y[21]]
    right_big_toe = [x[22], y[22]]
    right_small_toe = [x[23], y[23]]
    right_heel = [x[24], y[24]]

    angle_nose_to_neck_to_left_shoulder = getAngle(nose, neck, left_shoulder)
    angle_nose_to_neck_to_right_shoulder = getAngle(nose, neck, right_shoulder)
    angle_left_shoulder_to_right_shoulder = getAngle(left_shoulder, neck, right_shoulder)

    angle_left_shoulder_to_left_upper_arm = getAngle(neck, left_shoulder, left_elbow)

    angle_left_lower_arm_to_left_upper_arm = getAngle(left_shoulder, left_elbow, left_wrist)

    angle_right_upper_arm_to_right_shoulder = getAngle(neck, right_shoulder, right_elbow)

    angle_right_upper_arm_to_right_lower_arm = getAngle(right_shoulder, right_elbow, right_wrist)

    angle_left_eye_to_nose_to_left_ear_to_eye = getAngle(nose, left_eye, left_ear)

    angle_left_eye_to_nose_to_neck = getAngle(left_eye, nose, neck)

    angle_nose_to_neck_to_right_eye_to_nose = getAngle(right_eye, nose, neck)
    angle_left_eye_to_nose_to_right_eye_to_nose = getAngle(left_eye, nose, right_eye)

    angle_right_eye_to_nose_to_right_ear_to_eye = getAngle(nose, right_eye, right_ear)

    angle_right_hip_to_right_upper_leg = getAngle(midhip, right_hip, right_knee)

    angle_right_upper_leg_to_right_lower_leg = getAngle(right_hip, right_knee, right_ankle)

    angle_left_hip_to_left_upper_leg = getAngle(midhip, left_hip, left_knee)

    angle_left_upper_leg_to_left_lower_leg = getAngle(left_hip, left_knee, left_ankle)

    angle_left_lower_leg_left_ankle_to_heel = getAngle(left_knee, left_ankle, left_heel)

    angle_right_lower_leg_to_right_ankle_to_heel = getAngle(right_knee, right_ankle, right_heel)

    angle_right_foot_to_right_toes = getAngle(right_ankle, right_big_toe, right_small_toe)
    angle_right_foot_to_right_lower_leg = getAngle(right_knee, right_ankle, right_big_toe)
    angle_right_foot_to_right_ankle_to_heel = getAngle(right_ankle, right_heel, right_big_toe)

    angle_left_foot_to_left_lower_leg = getAngle(left_knee, left_ankle, left_big_toe)
    angle_left_foot_to_left_ankle_to_heel = getAngle(left_ankle, left_heel, left_big_toe)
    angle_left_foot_to_left_toes = getAngle(left_ankle, left_big_toe, left_small_toe)

    angle_torso_to_right_shoulder = getAngle(right_shoulder, neck, midhip)
    angle_torso_to_left_shoulder = getAngle(left_shoulder, neck, midhip)
    angle_torso_to_nose_to_neck = getAngle(nose, neck, midhip)

    angle_torso_to_right_hip = getAngle(neck, midhip, right_hip)
    angle_torso_to_left_hip = getAngle(neck, midhip, left_hip)

    body_vector = np.array([angle_nose_to_neck_to_left_shoulder, angle_nose_to_neck_to_right_shoulder,
                            angle_left_shoulder_to_right_shoulder, angle_left_shoulder_to_left_upper_arm,
                            angle_left_lower_arm_to_left_upper_arm, angle_right_upper_arm_to_right_shoulder,
                            angle_right_upper_arm_to_right_lower_arm, angle_left_eye_to_nose_to_left_ear_to_eye,
                            angle_left_eye_to_nose_to_neck, angle_nose_to_neck_to_right_eye_to_nose,
                            angle_left_eye_to_nose_to_right_eye_to_nose,
                            angle_right_eye_to_nose_to_right_ear_to_eye, angle_right_hip_to_right_upper_leg,
                            angle_right_upper_leg_to_right_lower_leg, angle_left_hip_to_left_upper_leg,
                            angle_left_upper_leg_to_left_lower_leg, angle_left_lower_leg_left_ankle_to_heel,
                            angle_right_lower_leg_to_right_ankle_to_heel, angle_right_foot_to_right_toes,
                            angle_right_foot_to_right_lower_leg, angle_right_foot_to_right_ankle_to_heel,
                            angle_left_foot_to_left_lower_leg, angle_left_foot_to_left_ankle_to_heel,
                            angle_left_foot_to_left_toes, angle_torso_to_right_shoulder,
                            angle_torso_to_left_shoulder, angle_torso_to_nose_to_neck, angle_torso_to_right_hip,
                            angle_torso_to_left_hip])
    return body_vector


def create_df(video, similarity = 'angle'):
    newDF = pd.DataFrame(index=range(29))
    i = 0

    files = []
    for file in sorted(os.listdir(DATA_PATH)):
        if os.path.isfile(os.path.join(DATA_PATH, file)) and video in file:
            files.append(file)

    for data in files:
        data = open(os.path.join(DATA_PATH, data), 'r')
        data = json.load(data)

        # produces RunitmeWarning for division with zero
        np.seterr(divide='ignore', invalid='ignore')

        bodyvector1 = compute_angle_vector(data)
        new_bodyvector = pd.DataFrame(bodyvector1)

        newDF[i] = new_bodyvector
        i += 1


    def create_velocity_df(Z_angles):
        newDF = pd.DataFrame(index=range(29),columns=range(Z_angles.shape[1]-1))
        i=0
        for j in range(Z_angles.shape[1]):
            bodyvector = Z_angles[j+1]-Z_angles[j]
            new_bodyvector =pd.DataFrame(bodyvector)
            newDF[i]=new_bodyvector
            i+=1
            if j == (Z_angles.shape[1] - 2) :
                break
        return newDF

    if similarity == 'velocity':
        newDF = create_velocity_df(newDF)


    ## rename columns and index
    columns = {}
    for i in range(len(newDF.columns)):
        columns[i] = 'Frame:{}'.format(i)
    newDF = newDF.rename(columns=columns, index=BODYPART_INDEX)

    return newDF.reset_index()
