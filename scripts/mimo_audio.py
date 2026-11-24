#!/usr/bin/env python3
"""MiMo 语音模型命令行工具：TTS / 音色设计 / 音色克隆 / 语音识别。

用法：
  python3 mimo_audio.py tts   "要合成的文本" -o out.mp3 [--voice 冰糖] [--style "语气描述"]
  python3 mimo_audio.py design "音色描述" "要合成的文本" -o out.mp3
  python3 mimo_audio.py clone  sample.mp3 "要合成的文本" -o out.mp3
  python3 mimo_audio.py asr    audio.mp3 [-l auto]

依赖环境变量：
  MIMO_API_KEY   Token Plan 专属 Key（tp-xxxxx）
  MIMO_BASE_URL  可选，默认 https://token-plan-cn.xiaomimimo.com/v1
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request

BASE_URL = os.environ.get("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
API_KEY = os.environ.get("MIMO_API_KEY", "")


def chat(payload: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"API 错误 {e.code}：{e.read().decode(errors='replace')[:500]}")


def read_audio_base64(path: str) -> tuple[str, str]:
    with open(path, "rb") as f:
        raw = f.read()
    mime = mimetypes.guess_type(path)[0]
    if mime not in ("audio/mpeg", "audio/mp3", "audio/wav"):
        sys.exit(f"仅支持 mp3 / wav 音频：{path}")
    return base64.b64encode(raw).decode(), mime


def synthesize(model: str, text: str, out: str, *, style: str | None = None,
               voice: str | None = None, sample_path: str | None = None,
               design: str | None = None) -> None:
    messages = []
    if design is not None:
        messages.append({"role": "user", "content": design})
    elif style is not None:
        messages.append({"role": "user", "content": style})
    messages.append({"role": "assistant", "content": text})

    audio: dict = {"format": out.rsplit(".", 1)[-1] or "mp3"}
    if voice is not None:
        audio["voice"] = voice
    if sample_path is not None:
        b64, mime = read_audio_base64(sample_path)
        audio["voice"] = f"data:{mime};base64,{b64}"

    resp = chat({"model": model, "messages": messages, "audio": audio})
    data = (resp.get("choices", [{}])[0].get("message", {}).get("audio") or {}).get("data")
    if not data:
        sys.exit(f"合成失败：{json.dumps(resp, ensure_ascii=False)[:500]}")
    with open(out, "wb") as f:
        f.write(base64.b64decode(data))
    print(f"已保存音频：{out}")


def transcribe(path: str, language: str) -> None:
    data_url, mime = read_audio_base64(path)
    fmt = "wav" if path.lower().endswith(".wav") else "mp3"
    resp = chat({
        "model": "mimo-v2.5-asr",
        "messages": [{
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": {"data": f"data:{mime};base64,{data_url}", "format": fmt},
            }],
        }],
        "asr_options": {"language": language},
    })
    text = (resp.get("choices", [{}])[0].get("message", {}) or {}).get("content")
    if text is None:
        sys.exit(f"识别失败：{json.dumps(resp, ensure_ascii=False)[:500]}")
    print(text)


def main() -> None:
    if not API_KEY:
        sys.exit("请先设置环境变量 MIMO_API_KEY")
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tts", help="预置音色合成")
    t.add_argument("text")
    t.add_argument("-o", "--out", default="out.mp3")
    t.add_argument("--voice", default="mimo_default",
                   help="mimo_default/冰糖/茉莉/苏打/白桦/Mia/Chloe/Milo/Dean")
    t.add_argument("--style", help="语气/风格描述，如：开心、语速稍快")

    d = sub.add_parser("design", help="按描述设计音色并合成")
    d.add_argument("design", help="音色描述，如：温柔的年轻女声，略带笑意")
    d.add_argument("text")
    d.add_argument("-o", "--out", default="out.mp3")

    c = sub.add_parser("clone", help="克隆样本音色并合成")
    c.add_argument("sample", help="音色样本文件（mp3/wav）")
    c.add_argument("text")
    c.add_argument("-o", "--out", default="out.mp3")

    a = sub.add_parser("asr", help="语音转文字")
    a.add_argument("audio", help="音频文件（mp3/wav）")
    a.add_argument("-l", "--language", default="auto", choices=["auto", "zh", "en"])

    args = p.parse_args()
    if args.cmd == "tts":
        synthesize("mimo-v2.5-tts", args.text, args.out, style=args.style, voice=args.voice)
    elif args.cmd == "design":
        synthesize("mimo-v2.5-tts-voicedesign", args.text, args.out, design=args.design)
    elif args.cmd == "clone":
        synthesize("mimo-v2.5-tts-voiceclone", args.text, args.out, sample_path=args.sample)
    elif args.cmd == "asr":
        transcribe(args.audio, args.language)


if __name__ == "__main__":
    main()
