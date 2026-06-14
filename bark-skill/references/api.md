# Bark API 参数参考

## 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| body | 是 | 推送内容 |
| title | 否 | 推送标题 |
| subtitle | 否 | 推送副标题 |
| markdown | 否 | 支持基础 Markdown，传此参数忽略 body |
| level | 否 | critical / active(默认) / timeSensitive / passive |
| volume | 否 | 重要警告音量 0-10，默认5 |
| badge | 否 | 角标数字 |
| call | 否 | 传 1 铃声重复播放 |
| autoCopy | 否 | 传 1 自动复制（iOS14.5以下） |
| copy | 否 | 指定复制内容 |
| sound | 否 | 铃声名称 |
| icon | 否 | 自定义图标 URL |
| image | 否 | 推送图片 URL |
| group | 否 | 分组名称 |
| ciphertext | 否 | 加密密文 |
| isArchive | 否 | 传 1 保存，0 不保存 |
| ttl | 否 | 保存有效期（秒） |
| url | 否 | 点击跳转 URL |
| action | 否 | 传 alert 弹出操作弹窗 |
| id | 否 | 更新通知时用（字符串类型） |
| delete | 否 | 传 1 删除通知，需配合 id |

## 推送级别

| level | 说明 |
|-------|------|
| active | 默认，立即亮屏显示 |
| timeSensitive | 时效性通知，专注模式下可显示 |
| critical | 重要警告，静音模式也响铃 |
| passive | 不亮屏，仅加入通知列表 |

## 支持的所有铃声（共 32 个）

| 名称 | 时长 | 说明 |
|------|------|------|
| alarm | 2.09s | 警报 |
| anticipate | 4.57s | 期待 |
| bell | 1.49s | 铃声 |
| birdsong | 0.72s | 鸟鸣 |
| bloom | 1.65s | 绽放 |
| calypso | 0.95s | 卡利普索 |
| chime | 4.60s | 钟声 |
| choo | 2.25s | 啾啾 |
| descent | 1.93s | 下降 |
| electronic | 1.53s | 电子 |
| fanfare | 1.56s | 号角 |
| glass | 1.76s | 玻璃 |
| gotosleep | 3.05s | 入睡 |
| healthnotification | 1.86s | 健康通知 |
| horn | 1.58s | 喇叭 |
| ladder | 1.37s | 阶梯 |
| mailsent | 1.53s | 邮件已发送 |
| minuet | 7.06s | 小步舞曲 |
| multiwayinvitation | 2.25s | 多人邀请 |
| newmail | 1.56s | 新邮件 |
| newsflash | 3.00s | 新闻快讯 |
| noir | 1.95s | 黑色 |
| paymentsuccess | 1.46s | 支付成功 |
| shake | 0.65s | 摇晃 |
| sherwoodforest | 4.78s | 舍伍德森林 |
| silence | 0.56s | 静音 |
| spell | 2.93s | 咒语 |
| suspense | 4.25s | 悬疑 |
| telegraph | 1.25s | 电报 |
| tiptoes | 1.60s | 踮脚 |
| typewriters | 2.67s | 打字机 |
| update | 4.55s | 更新 |
