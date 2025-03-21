# VOICEVOXベンチマーク

リポジトリをフォークして ワンラインで実行できるようにしたやつ

1. リポジトリをクローン
2. `compose.yml`を調整する
  - CPUの場合の構成になっているので、GPUの場合にはコメントアウトを調整する
3. `docker compose up --abort-on-container-exit`

以下、元の README
---
> 
> 1. Pythonのダウンロード
> 2. 解凍してcmdにてディレクトリ移動
> 3. VOICEVOXを起動
> 4. `pip install requests`と`python bench.py`を順番実行
> 
> --address https://voicevox:50021 等で外部へのテストも可能です。
> --header "Key: Value" という感じでheaderの指定が可能です。
> 
> ### 任意
> 5. 結果をフォームで送る
> https://forms.gle/WPXeRtJeACFdoFhF8
> 
