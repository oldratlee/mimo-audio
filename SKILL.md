---
name: MiMo 语音（TTS / ASR）
description: 用 MiMo 语音模型生成语音（朗读文本、配音、音色克隆、音色设计、唱歌）或把音频转写成文字。当用户想"读出来/念出来/生成语音/配音/合成声音/转写音频/语音识别/听写/把录音变成文字"或提到 TTS、ASR、音色时使用。
---

# MiMo 语音（TTS / ASR）

用本目录下的脚本调用：

```bash
python3 {baseDir}/scripts/mimo_audio.py <子命令> ...
```

## 运行前提与检查

- 依赖环境变量 `MIMO_API_KEY`（脚本从环境变量读取），缺失时脚本会报错退出；可用 `opencode auth list` 检查注入情况。
- 可选 `MIMO_BASE_URL` 覆盖 API 地址（默认 `https://token-plan-cn.xiaomimimo.com/v1`）。

## 能做什么

| 需求 | 子命令 |
|---|---|
| 把文本读成语音 | `tts` |
| 按描述创造新音色朗读 | `design` |
| 用某段录音的声音朗读 | `clone` |
| 音频转文字 | `asr` |

## 用法

```bash
# 朗读（--voice 可选：mimo_default/冰糖/茉莉/苏打/白桦/Mia/Chloe/Milo/Dean；中文用前 4 个）
python3 {baseDir}/scripts/mimo_audio.py tts "要读的文本" -o out.mp3 --voice 茉莉 --style "温柔、舒缓"

# 音色设计（第一参数是音色描述，如"温柔知性的深夜电台女声"）
python3 {baseDir}/scripts/mimo_audio.py design "音色描述" "要读的文本" -o out.mp3

# 音色克隆（样本限 mp3/wav，建议 5 秒以上）
python3 {baseDir}/scripts/mimo_audio.py clone sample.mp3 "要读的文本" -o out.mp3

# 转写（-l 可选 auto/zh/en）
python3 {baseDir}/scripts/mimo_audio.py asr audio.mp3 -l auto
```

输出格式由 `-o` 扩展名决定（`.mp3` 或 `.wav`）。

## 播放与排查（macOS 下的注意提示）

> 以下是 macOS 下的提示；其它系统暂不特别说明，由 Agent 自行处理播放。

**播放给用户听**：用 `afplay 文件`（建议放后台执行，长音频不阻塞），不要用 `open 文件`——`open` 会唤起系统默认的「音乐」App 等界面程序，打扰用户。`afplay` 是系统自带命令行播放器，直接出声、不启动任何界面。

**用户说"没听到声音"时排查**（按序）：

1. 文件是否有效：`afinfo 文件` 能看到 duration/bit rate 即正常；0 字节或打不开说明合成失败，重新跑 TTS。
2. 系统音量：`osascript -e 'get volume settings'`，确认 `output volume` 不为 0 且 `output muted:false`。
3. 是否用了 `open`：`open` 不保证自动播放，改用后台 `afplay`；后台命令无输出、正常退出即代表播放完毕，可据此判断。
4. 以上都正常仍听不到：让用户检查「系统设置 → 声音 → 输出」的耳机/音箱是否选对。

## 风格控制（tts / clone 有效）

- `--style` 放自然语言指令：情绪、语速、场景、导演模式（角色/场景/指导三段式）都行。
- 也可直接在待合成文本里嵌标签：开头 `(风格)` 定基调，如 `(东北话)……`、`(怅然)……`、`(唱歌)歌词……`（唱歌仅 tts）；文中可插 `[叹气]`、`[轻笑]`、`[哽咽]`、`[停顿]` 等细粒度标签。

## 注意事项

- 这些语音模型不是对话模型，不能当 OpenCode 的 chat 模型用，只能按上述方式调 API。
