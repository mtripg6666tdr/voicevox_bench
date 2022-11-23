import requests
import random
import json
from time import perf_counter
import argparse

def synthesis(text:str,address="127.0.0.1",port=50021,speaker=0,pitch=0.0,speed=1.0):
  """音声生成

  Args:
      text : 生成する文章
      address : VOCIEVOXのAPIサーバーのアドレス
      speaker : speaker_id 
      pitch : ピッチ
      speed : スピード
  
  Returns:
      生成時間(秒), レイテンシ(秒)
  """
  address = "http://"+address
  query_payload = {"text": text,"speaker":speaker}
  resp = requests.post(f"{address}:{port}/audio_query",params=query_payload)
  if not resp.status_code == 200:
    raise ConnectionError("Status code: %d" % resp.status_code)
  query_data = resp.json()
  synth_payload = {"speaker": speaker}
  query_data["speedScale"] = speed
  query_data["pitchScale"] = pitch
  #before = perf_counter()
  #requests.get(f"{address}:{port}/version")
  #after = perf_counter()
  #latency = after - before
  before = perf_counter()
  resp = requests.post(f"{address}:{port}/synthesis",params=synth_payload,data=json.dumps(query_data))
  if not resp.status_code == 200:
    raise ConnectionError("Status code: %d" % resp.status_code)
  after = perf_counter()
  return after - before #- latency , latency

def gen_text(count:int):
  return "".join([chr(random.randint(ord("あ"),ord("ん"))) for i in range(count)])

def get_speakers(address="127.0.0.1",port=50021):
  address = "http://"+address
  speakers = {}
  resp = requests.get(f"{address}:{port}/speakers")
  resp_dict = resp.json()
  for i in resp_dict:
    speakers[i["name"]] = {}
    for s in i["styles"]:
      speakers[i["name"]][s["name"]] = s["id"]
  return speakers

def bench(length:int,count=10,address="127.0.0.1",port=50021,quiet=False):
  synthesis("test",address=address,port=port)
  tmp = 0
  for i in range(count):
    text = gen_text(length)
    #elapsed_time,latency = synthesis(text,address=address,port=port)
    elapsed_time = synthesis(text,address=address,port=port)
    tmp += elapsed_time
    if not quiet:
      print(i+1,"time:",elapsed_time)
    result = round(tmp / count,4)
  return result

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-s",help="VOICEVOX API Server Address",default="127.0.0.1")
  parser.add_argument("-p",help="VOICEVOX API Server Port",default=50021)
  parser.add_argument("-q",help="Quiet benchmark log",action="store_true")
  parser.add_argument("-w",help="No wait for key input",action="store_true")
  args = parser.parse_args()
  if not args.w:
    input("Press Enter key to start benchmark...")
  score_10 = bench(length=10,address=args.s,port=args.p,quiet=args.q)
  score_50 = bench(length=50,address=args.s,port=args.p,quiet=args.q)
  score_100 = bench(length=100,address=args.s,port=args.p,quiet=args.q)
  score_avg = round((score_10 + score_50 + score_100) / 3,4)
  resp = requests.get(f"http://{args.s}:{args.p}/version")
  info_engine = resp.text.replace("\"","")
  resp = requests.get(f"http://{args.s}:{args.p}/supported_devices")
  info_devices = resp.json()
  if info_devices["cuda"]:
    info_device = "CUDA"
  elif info_devices["dml"]:
    info_device = "DirectML"
  else:
    info_device = "CPU"
  print()
  print("=========== Info ===========")
  print(" Engine:",info_engine)
  print(" Device:",info_device)
  print("========== Result ==========")
  print(" 10: ",score_10)
  print(" 50: ",score_50)
  print(" 100:",score_100)
  print(" Avg:",score_avg)
  print("============================")
  print()
  if not args.w:
    input("Press Enter key to exit...")