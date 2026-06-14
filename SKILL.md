---
name: bark-push
description: 通过 Bark 服务向 iPhone 发送推送通知。当用户需要：(1) 给手机发送推送消息 (2) 配置 iOS 推送通知 (3) 使用 API 调用 Bark 服务 (4) 自动化推送提醒时使用。包含可编辑的 device_key 配置文件。
---

# Bark Push Skill

通过 Bark 向 iPhone 发送推送通知。

## 配置文件

`config.json` 存储设备 Key 和其他默认参数，用户可随时修改。

```json
{
  "device_keys": {
    "default": "你的设备Key"
  },
  "defaults": {
    "sound": "minuet",
    "group": "default",
    "isArchive": 1
  }
}
```

- `device_keys` - 可配置多个设备 Key，使用 `--key` 指定别名
- `defaults` - 推送默认值，可被命令行参数覆盖

## 推送脚本

使用 `scripts/bark_push.py` 发送推送：

```bash
# 使用默认设备发送
python scripts/bark_push.py --body "你好"

# 指定标题和副标题
python scripts/bark_push.py --title "通知" --subtitle "副标题" --body "内容"

# 使用指定设备
python scripts/bark_push.py --key my_iphone --body "测试"

# 指定推送级别
python scripts/bark_push.py --body "重要" --level critical --volume 8

# 带图标和图片
python scripts/bark_push.py --body "带图" --icon "https://example.com/icon.png" --image "https://example.com/pic.jpg"

# 分组消息
python scripts/bark_push.py --body "订单通知" --group "order"

# Markdown 格式
python scripts/bark_push.py --markdown "# 标题\n- 列表项1\n- 列表项2"

# 点击跳转
python scripts/bark_push.py --body "查看详情" --url "https://example.com"

# 更新已存在的通知（需传入 id）
python scripts/bark_push.py --body "更新内容" --id "msg_001"

# 加密推送
python scripts/bark_push.py --body "机密内容" --encrypt --encrypt-key "1234567890123456"
```

所有参数详见 `references/api.md`。

## 批量推送

```bash
python scripts/bark_push.py --keys "device1,device2" --body "群发消息"
```
