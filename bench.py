import requests
import random
import json
from time import perf_counter
import argparse


def parse_headers(header_list: list) -> dict:
    """ヘッダーリストを辞書形式に変換"""
    headers = {}
    for header in header_list:
        key, value = header.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def synthesis(
    text: str,
    address: str,
    headers: dict = None,
    speaker: int = 0,
    pitch: float = 0.0,
    speed: float = 1.0,
) -> float:
    """音声生成

    Args:
        text : 生成する文章
        address : VOICEVOXのAPIサーバーのフルアドレス
        headers : リクエストに追加するヘッダー
        speaker : speaker_id
        pitch : ピッチ
        speed : スピード

    Returns:
        生成時間(秒)
    """
    query_payload = {"text": text, "speaker": speaker}
    try:
        resp = requests.post(f"{address}/audio_query", params=query_payload, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to send audio_query request: {e}")

    query_data = resp.json()
    query_data["speedScale"] = speed
    query_data["pitchScale"] = pitch

    try:
        before = perf_counter()
        resp = requests.post(f"{address}/synthesis", params={"speaker": speaker}, json=query_data, headers=headers)
        resp.raise_for_status()
        after = perf_counter()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to send synthesis request: {e}")

    return after - before


def gen_text(count: int) -> str:
    """ランダムなひらがなの文字列を生成"""
    return "".join(random.choice("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん") for _ in range(count))


def bench(length: int, count: int, address: str, headers: dict = None, quiet: bool = False) -> float:
    """ベンチマークを実行"""
    synthesis("test", address, headers)  # 初回呼び出しでキャッシュなどをウォームアップ
    total_time = 0
    for i in range(count):
        text = gen_text(length)
        elapsed_time = synthesis(text, address, headers)
        total_time += elapsed_time
        if not quiet:
            print(f"Run {i + 1}, Time: {elapsed_time:.4f} seconds")
    return round(total_time / count, 4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VOICEVOX Benchmark Script")
    parser.add_argument(
        "-a",
        "--address",
        help="Full VOICEVOX API Server Address (e.g., http://127.0.0.1:50021)",
        default="http://127.0.0.1:50021",
    )
    parser.add_argument(
        "--header",
        help="Specify request headers (e.g., 'Authorization: Bearer token')",
        action="append",
        default=[],
    )
    parser.add_argument("-q", "--quiet", help="Suppress benchmark logs", action="store_true")
    args = parser.parse_args()

    # ヘッダーをパース
    headers = parse_headers(args.header)

    print("Starting benchmark...")
    score_10 = bench(length=10, count=10, address=args.address, headers=headers, quiet=args.quiet)
    score_50 = bench(length=50, count=10, address=args.address, headers=headers, quiet=args.quiet)
    score_100 = bench(length=100, count=10, address=args.address, headers=headers, quiet=args.quiet)
    avg_score = round((score_10 + score_50 + score_100) / 3, 4)

    try:
        version = requests.get(f"{args.address}/version", headers=headers).text.strip('"')
        devices = requests.get(f"{args.address}/supported_devices", headers=headers).json()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch engine info: {e}")

    device_type = "CUDA" if devices.get("cuda") else "DirectML" if devices.get("dml") else "CPU"

    print("\n=========== Info ===========")
    print(f" Engine: {version}")
    print(f" Device: {device_type}")
    print("========== Result ==========")
    print(f" 10 char: {score_10} sec")
    print(f" 50 char: {score_50} sec")
    print(f"100 char: {score_100} sec")
    print(f" Avg: {avg_score} sec")
    print("============================\n")
