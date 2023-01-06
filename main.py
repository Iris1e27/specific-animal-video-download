from youtube_dl import YoutubeDL
from pathlib import Path

ANIMAL_LIST = {'giant panda/chinese panda/panda bear','giraffe','horse/zebra/donkey'}  # animals you want to search and download
action_list = {"eating","drinking","hunting","fighting","mating","feeding baby"}

NUMS = 10 # maximal items you can download
iMaxDuration = 1200  # maximal duration in seconds
YDL_OPTIONS = {
    # Download best mp4 format available or any other best if no mp4 available (https://github.com/ytdl-org/youtube-dl)
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'writeautomaticsub': True,
    'writesubtitles': True,
    'ignoreerrors': True,
}
download_path="./test"
YDL_OPTIONS_AUDIO_ONLY = {
    'format': 'bestaudio[ext=m4a]',
    'ignoreerrors': True,
}


def search(arg, nums):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            videos = ydl.extract_info(f"ytsearch{nums}:{arg}", download=False)['entries']
        except:
            videos = ydl.extract_info(arg, download=False)
    return videos


def download(arg,title,action,name):
    path = Path(name)/action
    path.mkdir(exist_ok=True,parents=True)
    YDL_OPTIONS['outtmpl'] = str(path/(title+"_"+arg))
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            video = ydl.extract_info("https://www.youtube.com/watch?v={}".format(arg), download=True)
            YDL_OPTIONS_AUDIO_ONLY['outtmpl'] = str(path/(title+"_"+arg+"_audio"))
            with YoutubeDL(YDL_OPTIONS_AUDIO_ONLY) as ydl_audio:
                audio = ydl_audio.extract_info("https://www.youtube.com/watch?v={}".format(arg), download=True)
                return True
        except:
            video = ydl.extract_info("https://www.youtube.com/watch?v={}".format(arg), download=False)
            return False


def filter(arg):
    if arg["duration"] > iMaxDuration:
        return None
    else:
        return arg

for animals in ANIMAL_LIST:
    DIR = True
    for animal in animals.split("/"):
        if DIR:
            dir_name = animal
            DIR = False
        for action in action_list:
            args = f"{animal} {action}"
            print(args)
            video_nums = 0
            video_infos = search(animal, NUMS)
            for info in video_infos:
                video = filter(info)
                if video is None: continue
                result = download(info["id"],info["title"],action, dir_name)
                if result: video_nums += 1
            print(f"{animal}: [{video_nums} / {NUMS}]")
