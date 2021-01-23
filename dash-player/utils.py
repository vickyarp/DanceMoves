import base64
from io import BytesIO
import dash_html_components as html

import numpy as np
from PIL import Image

DATA_PATH = './assets/keypoints/'
THUMBNAIL_PATH = './assets/thumbnails/'
POSE_PATH = './assets/search_query'

DATASET_VIDEOS = [
    'contemp1',
    'TB_F_FB',
    'UP3',
    'UP2',
    'UP1',
    'TR_S',
    'TR_F',
    'TOS_S',
    'TOS_F',
    'TL_S',
    'TL_F',
    'TF_S',
    'TF_F',
    'TB_S',
    'TB_S_FB',
    'TA',
    'SYN_U',
    'SYN_S',
    'SYN_R',
    'SYN_K',
    'SYN_B',
    'SS_S_RT',
    'SS_S_LT',
    'SS_S_FT',
    'SS_S_BK',
    'SS_F_RT',
    'SS_F_LT',
    'SS_F_FT',
    'SS_F_BK',
    'SJ_RT',
    'SJ_LT',
    'SJ_FT',
    'SJ_BK',
    'SB_R_WA',
    'SB_R_NA',
    'RV_R_S',
    'RV_R_F',
    'PV_R_S',
    'PV_R_F',
    'PE',
    'PC_F',
    'PC_S',
    'PB_S',
    'PB_F',
    'P3',
    'P2',
    'P1',
    'LU_S_dis',
    'LU_S_big',
    'LU_F_dis',
    'LU_F_big',
    'LD_S_small',
    'LD_S_dis',
    'LD_F_small',
    'FR_R_WA',
    'LD_F_dis',
    'FR_R_NA',
    'EF',
    'CU_R_WA',
    'CU_R_NA',
    'CH',
    'BSS_S_FT',
    'BSS_S_BK',
    'BS_S_RT',
    'BSS_F_FT',
    'BSS_F_BK',
    'BS_S_LT',
    'BS_S_FT',
    'BS_S_BK',
    'BS_F_RT',
    'BS_F_LT',
    'BS_F_FT',
    'BS_F_BK',
    'BJ_RT',
    'BJ_LT',
    'BJ_FT',
    'BJ_BK',
    'BBS_S_FT',
    'BBS_S_BK',
    'BBS_F_FT',
    'BBS_F_BK',
    'BA_R_WA',
    'BA_R_NA',
    'AS_L_WA',
    'AS_L_NA',
    'TB_F_FB',
    'AR',
]

COLORS_OLD = [
    'rgb(255, 0, 85)',
    'rgb(255, 0, 0)',
    'rgb(255, 85, 0)',
    'rgb(255, 170, 0)',
    'rgb(255, 255, 0)',
    'rgb(170, 255, 0)',
    'rgb(85, 255, 0)',
    'rgb(0, 255, 0)',
    'rgb(255, 0, 0)',
    'rgb(0, 255, 85)',
    'rgb(0, 255, 170)',
    'rgb(0, 255, 255)',
    'rgb(0, 170, 255)',
    'rgb(0, 85, 255)',
    'rgb(0, 0, 255)',
    'rgb(255, 0, 170)',
    'rgb(170, 0, 255)',
    'rgb(255, 0, 255)',
    'rgb(85, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 255, 255)',
    'rgb(0, 255, 255)']

COLORS = [
    'rgb(255, 0, 0)',
    'rgb(255, 0, 0)',
    'rgb(255, 170, 0)',
    'rgb(255, 255, 0)',
    'rgb(255, 85, 0)',
    'rgb(170, 255, 0)',
    'rgb(85, 255, 0)',
    'rgb(0, 255, 0)',
    'rgb(0, 255, 170)',
    'rgb(0, 255, 85)',
    'rgb(0, 170, 255)',
    'rgb(85, 0, 255)',
    'rgb(0, 85, 255)',
    'rgb(255, 0, 85)',
    'rgb(0, 0, 255)',
    'rgb(255, 0, 170)',
    'rgb(170, 0, 255)',
    'rgb(255, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 0, 255)',
    'rgb(0, 255, 255)',
    'rgb(0, 255, 255)',
    'rgb(0, 255, 255)',
]
PAIRS_RENDER = np.array(
    [[1, 8], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [8, 9], [9, 10], [10, 11], [8, 12], [12, 13], [13, 14],
     [1, 0], [0, 15], [15, 17], [0, 16], [16, 18], [14, 19], [19, 20], [14, 21], [11, 22], [22, 23], [11, 24]])

BODY_SEGMENTS = {
    'torso': [1,8],
    'right_shoulder': [1,2],
    'right_upper_arm': [2,3],
    'right_lower_arm': [3,4],
    'left_shoulder': [1,5],
    'left_upper_arm': [5,6],
    'left_lower_arm': [6,7],
    'right_hip': [8,9],
    'right_upper_leg': [9,10],
    'right_lower_leg': [10,11],
    'left_hip': [8,12],
    'left_upper_leg': [12,13],
    'left_lower_leg': [13,14],
    'nose_to_neck': [1,0],
    'right_eye_to_nose': [0,15],
    'right_ear_to_eye': [15,17],
    'left_eye_to_nose': [0,16],
    'left_ear_to_eye': [16,18],
    'left_foot': [14,19],
    'left_toes': [19,20],
    'left_ankle_to_heel': [14,21],
    'right_foot': [11,22],
    'right_toes': [22,23],
    'right_ankle_to_heel': [11,24],
}

BODYPART_INDEX = {
    0: 'nose_to_neck_to_left_shoulder',
    1: 'nose_to_neck_to_right_shoulder',
    2: 'left_shoulder_to_right_shoulder',
    3: 'left_shoulder_to_left_upper_arm',
    4: 'left_lower_arm_to_left_upper_arm',
    5: 'right_upper_arm_to_right_shoulder',
    6: 'right_upper_arm_to_right_lower_arm',
    7: 'left_eye_to_nose_to_left_ear_to_eye',
    8: 'left_eye_to_nose_to_neck',
    9: 'nose_to_neck_to_right_eye_to_nose',
    10: 'left_eye_to_nose_to_right_ear_to_eye',
    11: 'right_eye_to_nose_to_right_ear_to_eye',
    12: 'right_hip_to_right_upper_leg',
    13: 'right_upper_leg_to_right_lower_leg',
    14: 'left_hip_to_left_upper_leg',
    15: 'left_upper_leg_to_left_lower_leg',
    16: 'left_lower_leg_left_ankle_to_heel',
    17: 'right_lower_leg_to_right_ankle_to_heel',
    18: 'right_foot_to_right_toes',
    19: 'right_foot_to_right_lower_leg',
    20: 'right_foot_to_right_ankle_to_heel',
    21: 'left_foot_to_left_lower_leg',
    22: 'left_foot_to_left_ankle_to_heel',
    23: 'left_foot_to_left_toes',
    24: 'torso_to_right_shoulder',
    25: 'torso_to_left_shoulder',
    26: 'torso_to_nose_to_neck',
    27: 'torso_to_right_hip',
    28: 'torso_to_left_hip'
}


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


BODYPART_INDEX_CANONICAL = {
    7: 'left_eye_to_nose_to_left_ear_to_eye',
    8: 'left_eye_to_nose_to_neck',
    9: 'nose_to_neck_to_right_eye_to_nose',
    10: 'left_eye_to_nose_to_right_ear_to_eye',
    11: 'right_eye_to_nose_to_right_ear_to_eye',

    0: 'nose_to_neck_to_left_shoulder',
    1: 'nose_to_neck_to_right_shoulder',
    2: 'left_shoulder_to_right_shoulder',

    3: 'left_shoulder_to_left_upper_arm',
    4: 'left_lower_arm_to_left_upper_arm',
    5: 'right_upper_arm_to_right_shoulder',
    6: 'right_upper_arm_to_right_lower_arm',

    24: 'torso_to_right_shoulder',
    25: 'torso_to_left_shoulder',
    26: 'torso_to_nose_to_neck',
    27: 'torso_to_right_hip',
    28: 'torso_to_left_hip',

    12: 'right_hip_to_right_upper_leg',
    13: 'right_upper_leg_to_right_lower_leg',
    14: 'left_hip_to_left_upper_leg',
    15: 'left_upper_leg_to_left_lower_leg',
    16: 'left_lower_leg_left_ankle_to_heel',
    17: 'right_lower_leg_to_right_ankle_to_heel',

    18: 'right_foot_to_right_toes',
    19: 'right_foot_to_right_lower_leg',
    20: 'right_foot_to_right_ankle_to_heel',
    21: 'left_foot_to_left_lower_leg',
    22: 'left_foot_to_left_ankle_to_heel',
    23: 'left_foot_to_left_toes',
}

def get_thumbnail(path):
    path = '{}{}'.format(THUMBNAIL_PATH, path)
    i = Image.open(path)
    i.thumbnail((100, 100), Image.LANCZOS)
    buff = BytesIO()
    i.save(buff, format="PNG")
    encoded_image = base64.b64encode(buff.getvalue()).decode('UTF-8')
    return (html.Img(src='data:image/png;base64,{}'.format(encoded_image)))

# image = get_thumbnail('thumb.png')

BODYPART_THUMBS = [
    '![myImage-1](assets/thumbnails/nose_to_neck_to_left_shoulder.png)',
    '![myImage-2](assets/thumbnails/nose_to_neck_to_right_shoulder.png)',
    '![myImage-3](assets/thumbnails/left_shoulder_to_right_shoulder.png)',
    '![myImage-4](assets/thumbnails/left_shoulder_to_left_upper_arm.png)',
    '![myImage-5](assets/thumbnails/left_lower_arm_to_left_upper_arm.png)',
    '![myImage-6](assets/thumbnails/right_upper_arm_to_right_shoulder.png)',
    '![myImage-7](assets/thumbnails/right_upper_arm_to_right_lower_arm.png)',
    '![myImage-8](assets/thumbnails/left_eye_to_nose_to_left_ear_to_eye.png)',
    '![myImage-9](assets/thumbnails/left_eye_to_nose_to_neck.png)',
    '![myImage-10](assets/thumbnails/nose_to_neck_to_right_eye_to_nose.png)',
    '![myImage-11](assets/thumbnails/left_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-12](assets/thumbnails/right_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-13](assets/thumbnails/right_hip_to_right_upper_leg.png)',
    '![myImage-14](assets/thumbnails/right_upper_leg_to_right_lower_leg.png)',
    '![myImage-15](assets/thumbnails/left_hip_to_left_upper_leg.png)',
    '![myImage-16](assets/thumbnails/left_upper_leg_to_left_lower_leg.png)',
    '![myImage-17](assets/thumbnails/left_lower_leg_left_ankle_to_heel.png)',
    '![myImage-18](assets/thumbnails/right_lower_leg_to_right_ankle_to_heel.png)',
    '![myImage-19](assets/thumbnails/right_foot_to_right_toes.png)',
    '![myImage-20](assets/thumbnails/right_foot_to_right_lower_leg.png)',
    '![myImage-21](assets/thumbnails/right_foot_to_right_ankle_to_heel.png)',
    '![myImage-22](assets/thumbnails/left_foot_to_left_lower_leg.png)',
    '![myImage-23](assets/thumbnails/left_foot_to_left_ankle_to_heel.png)',
    '![myImage-24](assets/thumbnails/left_foot_to_left_toes.png)',
    '![myImage-25](assets/thumbnails/torso_to_right_shoulder.png)',
    '![myImage-26](assets/thumbnails/torso_to_left_shoulder.png)',
    '![myImage-27](assets/thumbnails/torso_to_nose_to_neck.png)',
    '![myImage-28](assets/thumbnails/torso_to_right_hip.png)',
    '![myImage-29](assets/thumbnails/torso_to_left_hip.png)'
    ]

BODYPART_THUMBS_SMALL = [
    '![myImage-1](assets/thumbnails/small/nose_to_neck_to_left_shoulder.png)',
    '![myImage-2](assets/thumbnails/small/nose_to_neck_to_right_shoulder.png)',
    '![myImage-3](assets/thumbnails/small/left_shoulder_to_right_shoulder.png)',
    '![myImage-4](assets/thumbnails/small/left_shoulder_to_left_upper_arm.png)',
    '![myImage-5](assets/thumbnails/small/left_lower_arm_to_left_upper_arm.png)',
    '![myImage-6](assets/thumbnails/small/right_upper_arm_to_right_shoulder.png)',
    '![myImage-7](assets/thumbnails/small/right_upper_arm_to_right_lower_arm.png)',
    '![myImage-8](assets/thumbnails/small/left_eye_to_nose_to_left_ear_to_eye.png)',
    '![myImage-9](assets/thumbnails/small/left_eye_to_nose_to_neck.png)',
    '![myImage-10](assets/thumbnails/small/nose_to_neck_to_right_eye_to_nose.png)',
    '![myImage-11](assets/thumbnails/small/left_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-12](assets/thumbnails/small/right_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-13](assets/thumbnails/small/right_hip_to_right_upper_leg.png)',
    '![myImage-14](assets/thumbnails/small/right_upper_leg_to_right_lower_leg.png)',
    '![myImage-15](assets/thumbnails/small/left_hip_to_left_upper_leg.png)',
    '![myImage-16](assets/thumbnails/small/left_upper_leg_to_left_lower_leg.png)',
    '![myImage-17](assets/thumbnails/small/left_lower_leg_left_ankle_to_heel.png)',
    '![myImage-18](assets/thumbnails/small/right_lower_leg_to_right_ankle_to_heel.png)',
    '![myImage-19](assets/thumbnails/small/right_foot_to_right_toes.png)',
    '![myImage-20](assets/thumbnails/small/right_foot_to_right_lower_leg.png)',
    '![myImage-21](assets/thumbnails/small/right_foot_to_right_ankle_to_heel.png)',
    '![myImage-22](assets/thumbnails/small/left_foot_to_left_lower_leg.png)',
    '![myImage-23](assets/thumbnails/small/left_foot_to_left_ankle_to_heel.png)',
    '![myImage-24](assets/thumbnails/small/left_foot_to_left_toes.png)',
    '![myImage-25](assets/thumbnails/small/torso_to_right_shoulder.png)',
    '![myImage-26](assets/thumbnails/small/torso_to_left_shoulder.png)',
    '![myImage-27](assets/thumbnails/small/torso_to_nose_to_neck.png)',
    '![myImage-28](assets/thumbnails/small/torso_to_right_hip.png)',
    '![myImage-29](assets/thumbnails/small/torso_to_left_hip.png)'
]

BODYPART_THUMBS_TINY = [
    '![myImage-1](assets/thumbnails/tiny/nose_to_neck_to_left_shoulder.png)',
    '![myImage-2](assets/thumbnails/tiny/nose_to_neck_to_right_shoulder.png)',
    '![myImage-3](assets/thumbnails/tiny/left_shoulder_to_right_shoulder.png)',
    '![myImage-4](assets/thumbnails/tiny/left_shoulder_to_left_upper_arm.png)',
    '![myImage-5](assets/thumbnails/tiny/left_lower_arm_to_left_upper_arm.png)',
    '![myImage-6](assets/thumbnails/tiny/right_upper_arm_to_right_shoulder.png)',
    '![myImage-7](assets/thumbnails/tiny/right_upper_arm_to_right_lower_arm.png)',
    '![myImage-8](assets/thumbnails/tiny/left_eye_to_nose_to_left_ear_to_eye.png)',
    '![myImage-9](assets/thumbnails/tiny/left_eye_to_nose_to_neck.png)',
    '![myImage-10](assets/thumbnails/tiny/nose_to_neck_to_right_eye_to_nose.png)',
    '![myImage-11](assets/thumbnails/tiny/left_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-12](assets/thumbnails/tiny/right_eye_to_nose_to_right_ear_to_eye.png)',
    '![myImage-13](assets/thumbnails/tiny/right_hip_to_right_upper_leg.png)',
    '![myImage-14](assets/thumbnails/tiny/right_upper_leg_to_right_lower_leg.png)',
    '![myImage-15](assets/thumbnails/tiny/left_hip_to_left_upper_leg.png)',
    '![myImage-16](assets/thumbnails/tiny/left_upper_leg_to_left_lower_leg.png)',
    '![myImage-17](assets/thumbnails/tiny/left_lower_leg_left_ankle_to_heel.png)',
    '![myImage-18](assets/thumbnails/tiny/right_lower_leg_to_right_ankle_to_heel.png)',
    '![myImage-19](assets/thumbnails/tiny/right_foot_to_right_toes.png)',
    '![myImage-20](assets/thumbnails/tiny/right_foot_to_right_lower_leg.png)',
    '![myImage-21](assets/thumbnails/tiny/right_foot_to_right_ankle_to_heel.png)',
    '![myImage-22](assets/thumbnails/tiny/left_foot_to_left_lower_leg.png)',
    '![myImage-23](assets/thumbnails/tiny/left_foot_to_left_ankle_to_heel.png)',
    '![myImage-24](assets/thumbnails/tiny/left_foot_to_left_toes.png)',
    '![myImage-25](assets/thumbnails/tiny/torso_to_right_shoulder.png)',
    '![myImage-26](assets/thumbnails/tiny/torso_to_left_shoulder.png)',
    '![myImage-27](assets/thumbnails/tiny/torso_to_nose_to_neck.png)',
    '![myImage-28](assets/thumbnails/tiny/torso_to_right_hip.png)',
    '![myImage-29](assets/thumbnails/tiny/torso_to_left_hip.png)'
]

POSES_DICT = {
    'qsearch-1': {'src': 'TB_S_FB_frame43.png', 'data':'TB_S_FB_000000000043_keypoints.json'},
    'qsearch-2': {'src': 'PC_F_frame_72.png', 'data': 'PC_F_000000000072_keypoints.json'},
    'qsearch-3': {'src': 'SYN_K_frame22.png', 'data': 'SYN_K_000000000022_keypoints.json'},

}


if __name__ == '__main__':
    test = update_selected_state(bodypart_names=['right_upper_arm', 'right_lower_arm'])
