from VideoEdit import *
from FileUtil import *

# names:
# 'short sleeve top'
# 'long sleeve top'
# 'short sleeve outwear'
# 'long sleeve outwear'
# 'vest'
# 'sling'
# 'shorts'
# 'trousers'
# 'skirt'
# 'short sleeve dress'
# 'long sleeve dress'
# 'vest dress'
# 'sling dress'

if __name__ == '__main__':
    video_path = get_video_path("video.mp4")
    sample_clothes = ["long sleeve top"] # 찾고싶은 종류 ui로 받아서 리스트로
    edit_video(video_path, sample_clothes)