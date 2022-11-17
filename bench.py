import requests
import random
import json
from time import perf_counter

def synthesis(text:str,address="127.0.0.1",port=50021,speaker=0,pitch=0.0,speed=1.0):
  """音声生成

  Args:
      text : 生成する文章
      address : VOCIEVOXのAPIサーバーのアドレス
      speaker : speaker_id 
      pitch : ピッチ
      speed : スピード
  
  Returns:
      
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
  before = perf_counter()
  resp = requests.post(f"{address}:{port}/synthesis",params=synth_payload,data=json.dumps(query_data))
  if not resp.status_code == 200:
    raise ConnectionError("Status code: %d" % resp.status_code)
  after = perf_counter()
  return after - before

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

def bench(length:int,count=10,address="127.0.0.1",port=50021):
  synthesis("test",address=address,port=port)
  tmp = 0
  for i in range(count):
    text = gen_text(length)
    elapsed_time = synthesis(text,address=address,port=port)
    tmp += elapsed_time
    print(i+1,elapsed_time)
    result = round(tmp / count,4)
  return result

score_10 = bench(length=10,address="127.0.0.1")
score_50 = bench(length=50,address="127.0.0.1")
score_100 = bench(length=100,address="127.0.0.1")
print("10:",score_10)
print("50:",score_50)
print("100:",score_100)