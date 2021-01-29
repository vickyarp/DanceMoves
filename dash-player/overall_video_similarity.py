import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
from tslearn.metrics import dtw_path
from utils import DATA_PATH, BODYPART_INDEX
from keypoint_frames import compute_angle_vector as compute_angle_vector_new
from missingpy import MissForest

# %%
#
# path_1 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\AR'
# path_2 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\AS_L_NA'
# path_3 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\AS_L_WA'
# path_4 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\BA_R_NA'
# path_5 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\BA_R_WA'
# path_6 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\TB_S'
# path_7 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\TB_S_FB'
# path_8 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\SYN_K'
# path_9 = 'C:\\Users\\user\\Desktop\\project\\1453169-20200914T174236Z-001\\SYN_B'


# %%

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


# %%

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
        [nose_to_neck, left_eye_to_nose, left_ear_to_eye, right_eye_to_nose, right_ear_to_eye, torso, left_shoulder,
         right_shoulder, right_upper_arm, right_lower_arm, left_upper_arm, left_lower_arm, left_hip, left_upper_leg,
         left_lower_leg, right_hip, right_upper_leg, right_lower_leg, right_foot, right_toes, right_ankle_to_heel,
         left_foot, left_toes, left_ankle_to_heel])
    return body_vector


# %%

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

def compute_angle(vector1, vector2, type='cosine'):
    unit_vector_1 = vector1 / np.linalg.norm(vector1)
    unit_vector_2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    if type == 'degrees':
        return round(degree(angle), 2)
    else:
        return round(math.cos(angle), 3)


# create a vector with all angles
def compute_angle_vector(data, type):
    ############################################################################### impute
    # data[data == 0] = np.nan
    # imputer = MissForest()
    # data = imputer.fit_transform(data)
    ######################################################
    x = create_x_coordicate(data)
    y = create_y_coordicate(data)

    nose_to_neck = (x[0] - x[1]), (y[0] - y[1])

    right_shoulder = (x[1] - x[2]), (y[1] - y[2])
    left_shoulder = (x[1] - x[5]), (y[1] - y[5])

    angle_nose_to_neck_to_left_shoulder = compute_angle(nose_to_neck, left_shoulder, type)
    angle_nose_to_neck_to_right_shoulder = compute_angle(nose_to_neck, right_shoulder, type)
    angle_left_shoulder_to_right_shoulder = compute_angle(left_shoulder, right_shoulder, type)

    left_upper_arm = (x[5] - x[6]), (y[5] - y[6])
    angle_left_shoulder_to_left_upper_arm = compute_angle(left_upper_arm, left_shoulder, type)

    left_lower_arm = (x[6] - x[7]), (y[6] - y[7])
    angle_left_lower_arm_to_left_upper_arm = compute_angle(left_upper_arm, left_lower_arm, type)

    right_upper_arm = (x[2] - x[3]), (y[2] - y[3])
    angle_right_upper_arm_to_right_shoulder = compute_angle(right_upper_arm, right_shoulder, type)

    right_lower_arm = (x[3] - x[4]), (y[3] - y[4])
    angle_right_upper_arm_to_right_lower_arm = compute_angle(right_upper_arm, right_lower_arm, type)

    left_eye_to_nose = (x[0] - x[16]), (y[0] - y[16])
    left_ear_to_eye = (x[16] - x[18]), (y[16] - y[18])

    angle_left_eye_to_nose_to_left_ear_to_eye = compute_angle(left_eye_to_nose, left_ear_to_eye, type)

    angle_left_eye_to_nose_to_neck = compute_angle(left_eye_to_nose, nose_to_neck, type)

    right_eye_to_nose = (x[0] - x[15]), (y[0] - y[15])
    right_ear_to_eye = (x[15] - x[17]), (y[15] - y[17])

    angle_nose_to_neck_to_right_eye_to_nose = compute_angle(nose_to_neck, right_eye_to_nose, type)
    angle_left_eye_to_nose_to_right_eye_to_nose = compute_angle(left_eye_to_nose, right_eye_to_nose, type)

    angle_right_eye_to_nose_to_right_ear_to_eye = compute_angle(right_eye_to_nose, right_ear_to_eye, type)

    right_hip = (x[8] - x[9]), (y[8] - y[9])
    right_upper_leg = (x[9] - x[10]), (y[9] - y[10])

    angle_right_hip_to_right_upper_leg = compute_angle(right_hip, right_upper_leg, type)

    right_lower_leg = (x[10] - x[11]), (y[10] - y[11])

    angle_right_upper_leg_to_right_lower_leg = compute_angle(right_upper_leg, right_lower_leg, type)

    left_hip = (x[8] - x[12]), (y[8] - y[12])
    left_upper_leg = (x[12] - x[13]), (y[12] - y[13])

    angle_left_hip_to_left_upper_leg = compute_angle(left_hip, left_upper_leg, type)

    left_lower_leg = (x[13] - x[14]), (y[13] - y[14])

    angle_left_upper_leg_to_left_lower_leg = compute_angle(left_upper_leg, left_lower_leg, type)

    left_ankle_to_heel = (x[14] - x[21]), (y[14] - y[21])

    angle_left_lower_leg_left_ankle_to_heel = compute_angle(left_lower_leg, left_ankle_to_heel, type)

    right_ankle_to_heel = (x[11] - x[24]), (y[11] - y[24])

    angle_right_lower_leg_to_right_ankle_to_heel = compute_angle(right_lower_leg, right_ankle_to_heel, type)

    right_toes = (x[22] - x[23]), (y[22] - y[23])
    right_foot = (x[11] - x[22]), (y[11] - y[22])

    angle_right_foot_to_right_toes = compute_angle(right_foot, right_toes, type)
    angle_right_foot_to_right_lower_leg = compute_angle(right_foot, right_lower_leg, type)
    angle_right_foot_to_right_ankle_to_heel = compute_angle(right_foot, right_ankle_to_heel, type)

    left_foot = (x[14] - x[19]), (y[14] - y[19])
    left_toes = (x[19] - x[20]), (y[19] - y[20])

    angle_left_foot_to_left_lower_leg = compute_angle(left_foot, left_lower_leg, type)
    angle_left_foot_to_left_ankle_to_heel = compute_angle(left_foot, left_ankle_to_heel, type)
    angle_left_foot_to_left_toes = compute_angle(left_foot, left_toes, type)

    torso = (x[1] - x[8]), (y[1] - y[8])

    angle_torso_to_right_shoulder = compute_angle(torso, right_shoulder, type)
    angle_torso_to_left_shoulder = compute_angle(torso, left_shoulder, type)
    angle_torso_to_nose_to_neck = compute_angle(torso, nose_to_neck, type)

    angle_torso_to_right_hip = compute_angle(torso, right_hip, type)
    angle_torso_to_left_hip = compute_angle(torso, left_hip, type)

    body_vector = np.array([angle_nose_to_neck_to_left_shoulder, angle_nose_to_neck_to_right_shoulder,
                            angle_left_shoulder_to_right_shoulder, angle_left_shoulder_to_left_upper_arm,
                            angle_left_lower_arm_to_left_upper_arm, angle_right_upper_arm_to_right_shoulder,
                            angle_right_upper_arm_to_right_lower_arm, angle_left_eye_to_nose_to_left_ear_to_eye,
                            angle_left_eye_to_nose_to_neck, angle_nose_to_neck_to_right_eye_to_nose,
                            angle_left_eye_to_nose_to_right_eye_to_nose, angle_right_eye_to_nose_to_right_ear_to_eye,
                            angle_right_hip_to_right_upper_leg, angle_right_upper_leg_to_right_lower_leg,
                            angle_left_hip_to_left_upper_leg, angle_left_upper_leg_to_left_lower_leg,
                            angle_left_lower_leg_left_ankle_to_heel, angle_right_lower_leg_to_right_ankle_to_heel,
                            angle_right_foot_to_right_toes, angle_right_foot_to_right_lower_leg,
                            angle_right_foot_to_right_ankle_to_heel, angle_left_foot_to_left_lower_leg,
                            angle_left_foot_to_left_ankle_to_heel, angle_left_foot_to_left_toes,
                            angle_torso_to_right_shoulder, angle_torso_to_left_shoulder, angle_torso_to_nose_to_neck,
                            angle_torso_to_right_hip, angle_torso_to_left_hip])
    return body_vector


def create_velocity_df(Z_angles):
    newDF = pd.DataFrame(index=range(29),columns=range(Z_angles.shape[1]-1))
    i=0
    for j in range(Z_angles.shape[1]):
        bodyvector = Z_angles[j+1]-Z_angles[j]
        new_bodyvector=pd.DataFrame(bodyvector)
        newDF[i]=new_bodyvector
        i+=1
        if j == (Z_angles.shape[1] - 2) :
            break
    return newDF


# %%

def create_angles(video, type='cosine', similarity='angle'):
    newDF = pd.DataFrame(index=range(29))
    i = 0

    files = []
    for file in sorted(os.listdir(DATA_PATH)):
        if os.path.isfile(os.path.join(DATA_PATH, file)) and video in file:
            files.append(file)

    for data in files:
        f = open(os.path.join(DATA_PATH, data), 'r')
        data = json.load(f)

        bodyvector1 = compute_angle_vector(data, type)
        new_bodyvector = pd.DataFrame(bodyvector1)

        # newDF['Frame: ',i]=new_bodyvector
        newDF[i] = new_bodyvector
        i += 1
        f.close()
        # print(bodyvector1)
    if similarity == 'velocity':
        newDF = create_velocity_df(newDF)
    return newDF

# %%



def overall_similarity(X_angles, Y_angles):
    similar_num = 0
    cos_vector = np.array([])
    path = dtw_path(X_angles.T, Y_angles.T)[0]

    path_dict = dict()
    for f1, f2 in path:
        path_dict.setdefault(f1, []).append(f2)

    for i, j in path:
        a = cosine_similarity(X_angles[i].values.reshape(1, -1), Y_angles[j].values.reshape(1, -1))
        # delete arrays with zeros
        if a != (np.array([0])):
            cos_vector = np.append(cos_vector, a)
    similar_num = round(np.mean(cos_vector), 3)
    return similar_num, path_dict

# %%

def create_angles_new(video, type='cosine', similarity='angle'):
    newDF = pd.DataFrame(index=range(29))
    i = 0

    files = []
    for file in sorted(os.listdir(DATA_PATH)):
        if os.path.isfile(os.path.join(DATA_PATH, file)) and video in file:
            files.append(file)

    for data in files:
        f = open(os.path.join(DATA_PATH, data), 'r')
        data = json.load(f)

        bodyvector1 = compute_angle_vector_new(data)
        new_bodyvector = pd.DataFrame(bodyvector1)

        # newDF['Frame: ',i]=new_bodyvector
        newDF[i] = new_bodyvector
        i += 1
        f.close()
        # print(bodyvector1)
    if similarity == 'velocity':
        newDF = create_velocity_df(newDF)
    return newDF

# %%

def pose_query(video='TB_F_FB', pose='TB_F_FB_000000000043_keypoints.json'):
    # video_angles = create_angles(video)
    video_angles = create_angles_new(video, type='degrees')
    f = open(os.path.join(DATA_PATH, pose), 'r')
    data = json.load(f)
    f.close()
    pose_angles = compute_angle_vector_new(data)
    pose_angles_ = pd.Series(pose_angles)
    df =  video_angles.sub(pose_angles_, axis='rows')
    columns = {}
    for i in range(len(df.columns)):
        columns[i] = 'Frame:{}'.format(i)
    df = df.rename(columns=columns, index=BODYPART_INDEX)
    df.insert(0, 'Pose', pose_angles, True)

    return df.reset_index()

if __name__ == '__main__':
    df_angles = create_angles('UP3')
