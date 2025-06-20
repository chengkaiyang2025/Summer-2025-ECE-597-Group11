import os.path

# PATH_PKL = r'D:\GITHUB\Summer-2025-ECE-597-Group11\code\web_v2\models\parameters'

# HUGGING_FACE_MODEL_1_PATH="D:\GITHUB\email-spam-detection-roberta"
def get_pkl_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(current_dir, 'models','parameters')
    return pkl_path
VERSION = 'v1'
BAYES_VERSION=  'v1'

