# BarkSkill

Bark 推送技能包 — 在智能体中通过 Bark 向 iPhone 发送推送通知。

## 安装

将 `bark-skill/` 复制到 opencode 的 skills 目录：

```bash
cp -r bark-skill ~/.config/opencode/skills/
```

## 配置

编辑 `~/.config/opencode/skills/bark-skill/config.json`，填入你的 device_key：

```json
{
  "device_keys": {
    "default": "你的device_key",
    "device_key1":"你另一条设备的device_key"
  }
}
```

device_key 从 Bark App 首页的测试 URL 中获取，例如 `https://api.day.app/xxxxxxxxxx/...` 中的 `xxxxxxxxxx`。

## 使用

安装后直接在对话中告诉 agent：

> 给我手机发一条推送，内容：记得买牛奶

agent 会自动调用 Bark 推送。也可以通过 `--key` 指定不同设备发送。
