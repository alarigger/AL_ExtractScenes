
#!/usr/bin/env python
from __future__ import print_function # Only Python 2.x
import os
import subprocess
import json
import sys, getopt
import json
import uuid
import subprocess

CURRENT_BATCH_ID= str(uuid.uuid4())[:8]

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)

def load_config():
  path= os.path.dirname(os.path.dirname(__file__))+"/config.json"
  print(path)
  if os.path.exists(path):
    with open(path, "r") as jsonFile:
          data = json.load(jsonFile)
          return data
  else:
    print(f"config file not found at {path}")

def get_user_data(_key,_default=None):
  path= os.path.dirname(os.path.dirname(__file__))+"/data/user.json"
  if os.path.exists(path):
    with open(path, "r") as jsonFile:
          data = json.load(jsonFile)
          if _key in data:
            return data[_key]
          else:
            return _default
  else:
    print(f"user file not found at {path}")
    return _default

def set_user_data(_key,_value):
  path= os.path.dirname(os.path.dirname(__file__))+"/data/user.json"
  data = {}
  if os.path.exists(path):
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
    data[_key] = _value
    with open(path, "w") as jsonFile:
        string = json.dumps(data)
        jsonFile.write(string)
  else:
    print(f"user file not found at {path}")

def get_output_path_for_video(_video_path,_suffix):
  output_dir = os.path.dirname(_video_path)
  id = CURRENT_BATCH_ID
  video_name = os.path.basename(_video_path).split(".")[0]
  dir_name = f"{video_name}"
  dir_path = f"{output_dir}/{dir_name}/{_suffix}_{id}"
  if os.path.exists( dir_path)==False:
      os.mkdir(dir_path)
  if os.path.exists( dir_path):
    print(dir_path)
    return  f"{dir_path}/{video_name}_{_suffix}_%5d.jpg"
  else:
    print(f"could not create output dir {dir_path}")
    return None

def create_shot_images(_video_path,sensibility=0.3):
    print(_video_path)
    print(sensibility)
    config = load_config()
    ffmpeg_dict_key = 'ffmpeg_path'
    ffmpeg_exe = config.get(ffmpeg_dict_key,None)
    if ffmpeg_exe is not None : 
      output_path = get_output_path_for_video(_video_path,"shot")
      if output_path is not None:
        args = []
        args.append(ffmpeg_exe)
        args.append('-i')
        args.append(_video_path)
        args.append('-vf')
        args.append(f"select=gt(scene\,{sensibility})")
        args.append('-vsync')
        args.append('0')
        args.append(output_path)
        cmd =" ".join(args)
        print(cmd)
        print("----running ffmpeg cmd")
        execute(args)
        return f"shot images created at {os.path.dirname(output_path)}"
    else:
      print(f"key {ffmpeg_dict_key} not found in config json")

def create_tile_images(_video_path,sensibility=0.3,scale=400,tilex=5,tiley=5):
    print(_video_path)
    print(sensibility)
    print(scale)
    config = load_config()
    ffmpeg_dict_key = 'ffmpeg_path'
    ffmpeg_exe = config.get(ffmpeg_dict_key,None)
    if ffmpeg_exe is not None : 
      output_path = output_path = get_output_path_for_video(_video_path,"tile")
      if output_path is not None:
        args = []
        args.append(ffmpeg_exe)
        args.append('-i')
        args.append(_video_path)
        args.append('-vf')
        args.append(f"select=gt(scene\,{sensibility}),scale={scale}:-1,tile={tilex}x{tiley}")
        '''
        args.append('-frames:v')
        args.append('1')
        args.append('-qscale:v')
        args.append('3')
        '''
        args.append('-vsync')
        args.append('0')
        args.append(output_path)
        cmd =" ".join(args)
        print(cmd)
        print("----running ffmpeg cmd")
        execute(args)
        return f"tile images created at {os.path.dirname(output_path)}"
    else:
      print(f"key {ffmpeg_dict_key} not found in config json")

    
def main(argv):
    input_video_path = None
    input_sensibiliy = 0.3
    try:
      opts, args = getopt.getopt(argv,"hv:s:",["input_video_path=","input_sensibiliy="])
    except getopt.GetoptError:
      print ('ExtractScene.py -v <input_video_path> ')
      print ('ExtractScene.py -s <input_sensibiliy> ')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
        sys.exit()
      elif opt in ("-v", "--input_video_path"):
        if os.path.exists(arg):
             input_video_path = arg
      elif opt in ("-s", "--input_sensibiliy"):
        if os.path.exists(arg):
             input_sensibiliy =int(arg)
    if input_video_path :
        create_tile_images(input_video_path , input_sensibiliy )
        create_shot_images(input_video_path , input_sensibiliy )
    else:
        print("incorrect video path ")

if __name__ == "__main__":
   main(sys.argv[1:])
'''
 python D:/1_TRAVAIL/WIP/ALARIGGER/CODING/PYTHON/REPOSITORIES/AL_ExtractScenes/python/ExtractScene.py -v D:/1_TRAVAIL/TEST_MATERIAL/test_video.mkv

'''