
#!/usr/bin/env python
import os
import subprocess
import json
import sys, getopt


'''time ./ffmpeg -i ./VIDEO.mp4 -vf "select=gt(scene\,0.4),scale=160:-1,tile=6x80" -frames:v 1 -qscale:v 3 preview.jpg'''
def extract_scenes(_video_path):
    ffmpeg_exe = os.path.dirname(os.path.dirname(__file__))+"/lib/ffmpeg-2022-04-03-git-1291568c98-essentials_build/bin/ffmpeg.exe"
    output_path = os.path.dirname(_video_path)+"/preview.jpg"
    args = []
    args.append(ffmpeg_exe)
    args.append('-i')
    args.append(_video_path)
    args.append('-vf')
    args.append("select=gt(scene\,0.4),scale=160:-1,tile=6x8")
    args.append('-frames:v')
    args.append('1')
    args.append('-qscale:v')
    args.append('3')
    args.append(output_path)
    cmd =" ".join(args)
    print(cmd)
    subprocess.run(args)

    
def main(argv):
    video_path = None
    try:
      opts, args = getopt.getopt(argv,"hv:",["video_path="])
    except getopt.GetoptError:
      print ('talk.py -s <input_sound_path> ')
      print ('input_sound_path can be a file or folder')
      print ('if folder given , it will be searched for a recent audio file')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
        sys.exit()
      elif opt in ("-v", "--video_path"):
        if os.path.exists(arg):
            video_path = arg
    if video_path:
        extract_scenes(video_path)
    else:
        print("incorrect video path ")

if __name__ == "__main__":
   main(sys.argv[1:])
'''
 python D:/1_TRAVAIL/WIP/ALARIGGER/CODING/PYTHON/REPOSITORIES/AL_ExtractScenes/python/ExtractScene.py -v D:/1_TRAVAIL/TEST_MATERIAL/test_video.mkv

'''