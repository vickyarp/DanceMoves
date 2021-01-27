import os
import json
import cv2
json.encoder.FLOAT_REPR = lambda o: format(o, '.3f')
import numpy as np
import pandas as pd
from utils import DATA_PATH, BODYPART_INDEX



# def calculate_timestamps(video='s'):
#     cap = cv2.VideoCapture('assets/TB_F_FB.mp4')
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
#
#     while(cap.isOpened()):
#         frame_exists, curr_frame = cap.read()
#         if frame_exists:
#             timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
#         else:
#             break
#
#     cap.release()
#     return timestamps

def export_frames_from_video(video='s'):
    vidcap = cv2.VideoCapture('./assets/{}'.format(video))
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("./assets/frames/{}_frame{}.jpg".format(video, count), image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read new frame: {}'.format(count), success)
        count += 1


def read_keypoints(data):
    people_column = data['people']
    for d in people_column:
        keypoints = (d["pose_keypoints_2d"])
    return keypoints


def get_keypoints(video):
    keypoint_dataset = np.array([], dtype=np.float64)
    kp = {}
    datapoints = {}

    # for datum in DATASET_VIDEOS:
    files = []
    for i in sorted(os.listdir(DATA_PATH)):
        if os.path.isfile(os.path.join(DATA_PATH, i)) and video in i:
            files.append(i)

    frames_csv = np.ndarray([len(files),75], dtype=object)
    # frames_df = pd.DataFrame(columns=['frame_num', 'x{}'.format(i) for i in range(75)])
    for i, file in enumerate(files):
        # kp[datum] = {}
        # frames = {}
        # with open(os.path.join(DATA_PATH, file)) as f:
        #     data_f = json.load(f)
        #     frames[i] = json.dumps(data_f['people'][0]["pose_keypoints_2d"])
        #     kp[datum] = json.dumps(frames[i])

        with open(os.path.join(DATA_PATH, file)) as f:
            data_f = json.load(f)
            keypoints = read_keypoints(data_f)
            # frame = json.dumps(data_f['people'][0]["pose_keypoints_2d"]).split(',')
            # frame_float = [float(point.strip()) for point in frame]
            frames_csv[i] = keypoints
    datapoints[video] = frames_csv     ##remove?

    # timestamps = calculate_timestamps() ## add argument
    # timestamps.append(timestamps[-1])  ## add condition depending on number of frames
    # timestamps = np.true_divide(timestamps, 1000)
    # frames_csv = np.insert(frames_csv, 0, timestamps, axis=1)
    return frames_csv


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

        def bodyparts(data):

            # //     {0,  "Nose"},
            # //     {1,  "Neck"},
            # //     {2,  "RShoulder"},
            # //     {3,  "RElbow"},
            # //     {4,  "RWrist"},
            # //     {5,  "LShoulder"},
            # //     {6,  "LElbow"},
            # //     {7,  "LWrist"},
            # //     {8,  "MidHip"},
            # //     {9,  "RHip"},
            # //     {10, "RKnee"},
            # //     {11, "RAnkle"},
            # //     {12, "LHip"},
            # //     {13, "LKnee"},
            # //     {14, "LAnkle"},
            # //     {15, "REye"},
            # //     {16, "LEye"},
            # //     {17, "REar"},
            # //     {18, "LEar"},
            # //     {19, "LBigToe"},
            # //     {20, "LSmallToe"},
            # //     {21, "LHeel"},
            # //     {22, "RBigToe"},
            # //     {23, "RSmallToe"},
            # //     {24, "RHeel"},
            # //     {25, "Background"}

            x = create_x_coordicate(data)
            y = create_y_coordicate(data)

            nose_to_neck = (x[0] - x[1]), (y[0] - y[1])

            right_eye_to_nose = (x[0] - x[15]), (y[0] - y[15])

            right_ear_to_eye = (x[15] - x[17]), (y[15] - y[17])
            left_eye_to_nose = (x[0] - x[16]), (y[0] - y[16])
            left_ear_to_eye = (x[16] - x[18]), (y[16] - y[18])

            torso = (x[1] - x[8]), (y[1] - y[8])

            right_shoulder = (x[1] - x[2]), (y[1] - y[2])
            left_shoulder = (x[1] - x[5]), (y[1] - y[5])

            right_upper_arm = (x[2] - x[3]), (y[2] - y[3])
            right_lower_arm = (x[3] - x[4]), (y[3] - y[4])
            left_upper_arm = (x[5] - x[6]), (y[5] - y[6])
            left_lower_arm = (x[6] - x[7]), (y[6] - y[7])

            right_hip = (x[8] - x[9]), (y[8] - y[9])
            right_upper_leg = (x[9] - x[10]), (y[9] - y[10])
            right_lower_leg = (x[10] - x[11]), (y[10] - y[11])
            left_hip = (x[8] - x[12]), (y[8] - y[12])
            left_upper_leg = (x[12] - x[13]), (y[12] - y[13])
            left_lower_leg = (x[13] - x[14]), (y[13] - y[14])

            left_foot = (x[14] - x[19]), (y[14] - y[19])
            left_toes = (x[19] - x[20]), (y[19] - y[20])
            left_ankle_to_heel = (x[14] - x[21]), (y[14] - y[21])
            right_foot = (x[11] - x[22]), (y[11] - y[22])
            right_toes = (x[22] - x[23]), (y[22] - y[23])
            right_ankle_to_heel = (x[11] - x[24]), (y[11] - y[24])

            body_vector = np.array(
                [nose_to_neck, left_eye_to_nose, left_ear_to_eye, right_eye_to_nose, right_ear_to_eye, torso,
                 left_shoulder, right_shoulder, right_upper_arm, right_lower_arm, left_upper_arm, left_lower_arm,
                 left_hip, left_upper_leg, left_lower_leg, right_hip, right_upper_leg, right_lower_leg, right_foot,
                 right_toes, right_ankle_to_heel, left_foot, left_toes, left_ankle_to_heel])
            return body_vector

        # ANGLE SIMILARITY

        # defines the degree of an angle
        import math
        def degree(x):
            pi = math.pi
            degree = (x * 180) / pi
            return degree

        # produces RunitmeWarning for division with zero
        np.seterr(divide='ignore', invalid='ignore')

        # for every neighbor vectors compute angles

        def compute_angle(vector1, vector2):
            unit_vector_1 = vector1 / np.linalg.norm(vector1)
            unit_vector_2 = vector2 / np.linalg.norm(vector2)
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angle = np.arccos(dot_product)
            return round(degree(angle), 2) ##changed by art
            # return round(math.cos(angle), 2)

        # create a vector with all angles
        def compute_angle_vector(data):
            x = create_x_coordicate(data)
            y = create_y_coordicate(data)

            nose_to_neck = (x[0] - x[1]), (y[0] - y[1])

            right_shoulder = (x[1] - x[2]), (y[1] - y[2])
            left_shoulder = (x[1] - x[5]), (y[1] - y[5])

            angle_nose_to_neck_to_left_shoulder = compute_angle(nose_to_neck, left_shoulder)
            angle_nose_to_neck_to_right_shoulder = compute_angle(nose_to_neck, right_shoulder)
            angle_left_shoulder_to_right_shoulder = compute_angle(left_shoulder, right_shoulder)

            left_upper_arm = (x[5] - x[6]), (y[5] - y[6])
            angle_left_shoulder_to_left_upper_arm = compute_angle(left_upper_arm, left_shoulder)

            left_lower_arm = (x[6] - x[7]), (y[6] - y[7])
            angle_left_lower_arm_to_left_upper_arm = compute_angle(left_upper_arm, left_lower_arm)

            right_upper_arm = (x[2] - x[3]), (y[2] - y[3])
            angle_right_upper_arm_to_right_shoulder = compute_angle(right_upper_arm, right_shoulder)

            right_lower_arm = (x[3] - x[4]), (y[3] - y[4])
            angle_right_upper_arm_to_right_lower_arm = compute_angle(right_upper_arm, right_lower_arm)

            left_eye_to_nose = (x[0] - x[16]), (y[0] - y[16])
            left_ear_to_eye = (x[16] - x[18]), (y[16] - y[18])

            angle_left_eye_to_nose_to_left_ear_to_eye = compute_angle(left_eye_to_nose, left_ear_to_eye)

            angle_left_eye_to_nose_to_neck = compute_angle(left_eye_to_nose, nose_to_neck)

            right_eye_to_nose = (x[0] - x[15]), (y[0] - y[15])
            right_ear_to_eye = (x[15] - x[17]), (y[15] - y[17])

            angle_nose_to_neck_to_right_eye_to_nose = compute_angle(nose_to_neck, right_eye_to_nose)
            angle_left_eye_to_nose_to_right_eye_to_nose = compute_angle(left_eye_to_nose, right_eye_to_nose)

            angle_right_eye_to_nose_to_right_ear_to_eye = compute_angle(right_eye_to_nose, right_ear_to_eye)

            right_hip = (x[8] - x[9]), (y[8] - y[9])
            right_upper_leg = (x[9] - x[10]), (y[9] - y[10])

            angle_right_hip_to_right_upper_leg = compute_angle(right_hip, right_upper_leg)

            right_lower_leg = (x[10] - x[11]), (y[10] - y[11])

            angle_right_upper_leg_to_right_lower_leg = compute_angle(right_upper_leg, right_lower_leg)

            left_hip = (x[8] - x[12]), (y[8] - y[12])
            left_upper_leg = (x[12] - x[13]), (y[12] - y[13])

            angle_left_hip_to_left_upper_leg = compute_angle(left_hip, left_upper_leg)

            left_lower_leg = (x[13] - x[14]), (y[13] - y[14])

            angle_left_upper_leg_to_left_lower_leg = compute_angle(left_upper_leg, left_lower_leg)

            left_ankle_to_heel = (x[14] - x[21]), (y[14] - y[21])

            angle_left_lower_leg_left_ankle_to_heel = compute_angle(left_lower_leg, left_ankle_to_heel)

            right_ankle_to_heel = (x[11] - x[24]), (y[11] - y[24])

            angle_right_lower_leg_to_right_ankle_to_heel = compute_angle(right_lower_leg, right_ankle_to_heel)

            right_toes = (x[22] - x[23]), (y[22] - y[23])
            right_foot = (x[11] - x[22]), (y[11] - y[22])

            angle_right_foot_to_right_toes = compute_angle(right_foot, right_toes)
            angle_right_foot_to_right_lower_leg = compute_angle(right_foot, right_lower_leg)
            angle_right_foot_to_right_ankle_to_heel = compute_angle(right_foot, right_ankle_to_heel)

            left_foot = (x[14] - x[19]), (y[14] - y[19])
            left_toes = (x[19] - x[20]), (y[19] - y[20])

            angle_left_foot_to_left_lower_leg = compute_angle(left_foot, left_lower_leg)
            angle_left_foot_to_left_ankle_to_heel = compute_angle(left_foot, left_ankle_to_heel)
            angle_left_foot_to_left_toes = compute_angle(left_foot, left_toes)

            torso = (x[1] - x[8]), (y[1] - y[8])

            angle_torso_to_right_shoulder = compute_angle(torso, right_shoulder)
            angle_torso_to_left_shoulder = compute_angle(torso, left_shoulder)
            angle_torso_to_nose_to_neck = compute_angle(torso, nose_to_neck)

            angle_torso_to_right_hip = compute_angle(torso, right_hip)
            angle_torso_to_left_hip = compute_angle(torso, left_hip)

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

        bodyvector1 = compute_angle_vector(data)
        new_bodyvector = pd.DataFrame(bodyvector1)

        # newDF['Frame: ',i]=new_bodyvector
        newDF[i] = new_bodyvector #####HERE CHANGED FOR COLUMN VISUALIZATION
        i += 1
        # print(bodyvector1)
    # newDF = newDF.fillna(0)


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



if __name__ == '__main__':
    DATA_PATH = 'assets/keypoints'
    # timestamps = calculate_timestamps()
    # frames_csv = get_keypoints('TB_F_FB')
    # timestamps.append(timestamps[-1])
    # times = np.true_divide(timestamps, 1000)
    # test = np.insert(frames_csv, 0, times, axis=1)
    #
