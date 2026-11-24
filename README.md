# MiMo 语音 Skill（TTS / ASR）

基于 MiMo 语音模型（mimo-v2.5 系列）的 OpenCode Skill：文本转语音（预置音色 / 音色设计 / 音色克隆）与语音转文字。具体用法见 [SKILL.md](SKILL.md)。

## 涉及模型

| 模型 | 能力 |
|---|---|
| `mimo-v2.5-tts` | 预置音色合成 |
| `mimo-v2.5-tts-voicedesign` | 音色设计合成 |
| `mimo-v2.5-tts-voiceclone` | 音色克隆合成 |
| `mimo-v2.5-asr` | 语音转文字 |

## 订阅、计费与鉴权（与 Token Plan 订阅绑定）

目前本 Skill 涉及的 MiMo 模型调用、计费与接入鉴权均与 **Token Plan 订阅** 绑定：

- 模型：上表 4 个语音模型通过 Token Plan 调用。
- 计费：TTS 系列**限时免费**；ASR 按音频时长计 30M Credits/小时（从套餐扣）。
- 接入与鉴权：使用 Token Plan 专属 `tp-` Key，由 OpenCode 自动注入为环境变量 `MIMO_API_KEY`；API 地址默认 `https://token-plan-cn.xiaomimimo.com/v1`，可用 `MIMO_BASE_URL` 覆盖。
- 合规：Token Plan 额度仅限编程工具内使用，不要拿 Key 给外部脚本/后端长期调用。

> 其它订阅/计费方式本文不展开，请自行查阅 MiMo 官方文档了解。

相关官方文档：

- [Token Plan 订阅（计费 / 额度）](https://mimo.mi.com/docs/zh-CN/tokenplan/Token%20Plan/subscription)。
- [OpenCode 接入](https://mimo.mi.com/docs/zh-CN/tokenplan/integration/opencode)
