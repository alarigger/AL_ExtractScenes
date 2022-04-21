
#!/usr/bin/env python
import os
import subprocess
import json
import sys, getopt

'''
    args.append(f"select=gt(scene\,{sensibility}),scale={scale}:-1,tile={tilex}x{tiley}")
    args.append('-frames:v')
    args.append('1')
    args.append('-qscale:v')
    args.append('3')
'''

def load_config():
  json_path= os.path.dirname(os.path.dirname(__file__))+"config.json"
  if os.path.exists(jjson_path):
    with open(json_path, "r") as jsonFile:
          data = json.load(jsonFile)
          return data



def extract_scenes(_video_path):
    config = load_config()
    ffmpeg_exe = config['ffmpeg']
    sensibility = 0.3
    scale = 400
    tilex = 10
    tiley = 100
    output_dir = os.path.dirname(_video_path)
    dir_name = f"scenes_se{str(sensibility)}_sc{str(scale)}"
    dir_path = f"{output_dir}/{dir_name}"
    if os.path.exists( dir_path)==False:
      os.mkdir(dir_path)
    output_path = f"{dir_path}/shot_%4d.jpg"
    args = []
    args.append(ffmpeg_exe)
    args.append('-i')
    args.append(_video_path)
    args.append('-vf')
    args.append(f"select=gt(scene\,{sensibility}),scale={scale}:-1")
    args.append('-vsync')
    args.append('0')
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