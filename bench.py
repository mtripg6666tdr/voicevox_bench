import requests
import random

def synthesis(text,address="localhost",speaker=0,pitch=0,speed=0):
  """音声生成

  Args:
      text : 生成する文章
      address : VOCIEVOXのAPIサーバーのアドレス
      speaker : speaker_id 
      pitch : ピッチ
      speed : スピード
  """


def bench():
  text = "".join([chr(random.randint(ord("あ"),ord("ん"))) for i in range(10)])