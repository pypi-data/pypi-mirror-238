#ffmpeg -i INFILE.mp4 -vcodec copy -acodec copy -ss 00:00:00 -t 00:00:10.000 OUTFILE.mp4
import os, sys
import subprocess
import mimetypes, magic

try:
  from . import fs_tools
  from . import os_tools
except ImportError:
  import fs_tools
  import os_tools
  
  
# global variables
FFMPEG_EXE = None
FFPROBE_EXE = None


def set_ffmpeg_exe(ffmpeg_path):
  global FFMPEG_EXE
  assert fs_tools.exists(ffmpeg_path), f'{ffmpeg_path} not found'
  FFMPEG_EXE = ffmpeg_path
  return FFMPEG_EXE

def set_ffprobe_exe(ffprobe_path):
  global FFPROBE_EXE
  assert fs_tools.exists(ffprobe_path), f'{ffprobe_path} not found'
  FFPROBE_EXE = ffprobe_path
  return FFPROBE_EXE

def detect_media_type(file_path):
  assert FFPROBE_EXE is not None, f'FFPROBE_EXE not set.'
  assert fs_tools.exists(file_path), f'{file_path} not found.'
  m = magic.Magic(mime=True)

  # Get the MIME type of the file
  mimetype = m.from_file(file_path)
  extension = mimetypes.guess_extension(mimetype)
  #sample : ffprobe -v error -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1

  if extension is None:
    _,_,extension = fs_tools.parse_full_path(file_path)
    
  if extension == '.bin' :
    sys_cmd = FFPROBE_EXE + ' -v error -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1 ' + file_path
    mimetype = os_tools.exec_sys_cmd(sys_cmd)
    if mimetype == 'mpegts' : extension = '.ts'
    if mimetype == 'mov,mp4,m4a,3gp,3g2,mj2' : extension = '.mp4'

  return extension, mimetype


def get_video_duration(src_file):
  assert FFPROBE_EXE is not None, f'FFPROBE_EXE not set.'
  sys_cmd = FFPROBE_EXE + ' -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + src_file
  duration = os_tools.exec_sys_cmd(sys_cmd)
  duration = int(float(duration))
  return duration


def split_by_time(time_interval, duration):
  file_index = 0
  start_time = 0
  end_time   = 0
  split_list = []
  
  while (True):
    file_index +=1
    if (start_time + time_interval > duration) :
      end_time = duration
    else:
      end_time = start_time + time_interval

    split_list.append({"index":file_index, "start":start_time, "end" : end_time})
    if end_time >= duration : break
    start_time = end_time
    
  return split_list
  
def split_video(source_name, time_interval):
  assert FFMPEG_EXE is not None, f'FFMPEG_EXE not set.'

  #time.strftime('%H:%M:%S', time.gmtime(12345))
  #ffmpeg -i source.m4v -ss 1144.94 -t 581.25 -c copy part3.m4v
  file_path, file_extension = os.path.splitext(source_name)
  split_list = split_by_time(time_interval,get_video_duration(source_name))
  split_part_list = []
  for part in split_list:
    part["output"] = file_path + "_{:04}".format(part["index"]) + file_extension
    if os.path.isfile(part["output"]):  os.remove(part["output"])
    split_part_list.append(part)
  
  for part in split_part_list:
    p = subprocess.Popen([
      FFMPEG_EXE,
      "-loglevel",
      "panic",
      "-i",
      source_name,
      "-ss",
      str(part["start"]),
      "-to",
      str(part["end"]),
      "-c",
      "copy",
      part["output"]
    ], stdout=subprocess.PIPE)    
    
  return split_part_list  


def convert_mp4(source_file, target_file) :
  #ffmpeg -i input_video -c:v copy -c:a copy -y output.mp4
  
  assert FFMPEG_EXE is not None, f'FFMPEG_EXE not set.'
  assert fs_tools.exists(source_file), f'{source_file} not exists.'
  assert source_file!=target_file, f'{source_file} is identical to target.'
  
  
  sys_cmd = FFMPEG_EXE + ' -i ' + '"' + source_file + '"' + ' -c:v copy -c:a copy -y ' + '"' + target_file + '"'
  os.system(sys_cmd)
  """
  p = subprocess.Popen([
      FFMPEG_EXE,
      "-i", "\"" + source_file + "\"",
      "-c:v", "copy",
      "-c:a", "copy",
      "-y",
      "\"" + target_file + "\""
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  
  stdout, stderr = p.communicate()
  """
  return 



if __name__ == "__main__":
  #print (split_video("R:/x.mp4",360))
  #print (detect_file_type("Y:/important/Home_Photo/2003_02_05/101_0189.JPG"))
  #print (detect_file_type("R:/Temp3/1.mp4"))
  #print (detect_file_type("Y:/fan/no-raid/xxx/japanlust/1.japanese-teen-quivers-with-pussy-pleasure.mp4"))
 
  set_ffprobe_exe('C:/Tools/ffmpeg/bin/ffprobe.exe')
  set_ffmpeg_exe('C:/Tools/ffmpeg/bin/ffmpeg.exe')
  #print (detect_media_type("Y:/important/Home_Photo/2003_02_05/101_0189.JPG"))
  print (detect_media_type("R:/Temp3/1.mp4"))
  #print (detect_media_type("R:/Temp3/2.mts"))
  #print (detect_media_type("Y:/fan/no-raid/xxx/japanlust/1.japanese-teen-quivers-with-pussy-pleasure.mp4"))
  print (convert_mp4('R:/Temp3/HDV_CARD_0002.00001.20090414_155250.MTS', 'R:/Temp3/1.mp4'))
  print (convert_mp4('R:/Temp3/20040815_003.mpg', 'R:/Temp3/2.mp4'))
  print ("done")
  
 
