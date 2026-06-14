import argparse
import json
import os
import subprocess
import sys
import base64

if sys.stdout.encoding and sys.stdout.encoding.upper() not in ("UTF-8", "UTF8"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

BARK_API = "https://api.day.app"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 未找到配置文件 {CONFIG_PATH}")
        print("请先在 config.json 中设置 device_key")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_device_key(config, key_alias):
    keys = config.get("device_keys", {})
    if key_alias in keys:
        return keys[key_alias]
    if key_alias:
        print(f"错误: 配置中未找到设备别名 '{key_alias}'")
        print(f"可用设备: {', '.join(keys.keys())}")
        sys.exit(1)
    if "default" in keys:
        return keys["default"]
    print("错误: config.json 中未配置任何 device_key")
    sys.exit(1)


def encrypt_payload(payload, key, iv=None):
    import subprocess
    json_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    key_hex = subprocess.run(
        ["xxd", "-ps", "-c", "200"],
        input=key.encode(),
        capture_output=True,
        text=True
    ).stdout.strip()

    if iv is None:
        iv_bytes = os.urandom(16)
        iv_hex = iv_bytes.hex()
    else:
        iv_hex = subprocess.run(
            ["xxd", "-ps", "-c", "200"],
            input=iv.encode(),
            capture_output=True,
            text=True
        ).stdout.strip()

    result = subprocess.run(
        ["openssl", "enc", "-aes-128-cbc", "-K", key_hex, "-iv", iv_hex, "-base64"],
        input=json_str.encode(),
        capture_output=True
    )
    ciphertext = result.stdout.decode().strip()
    return ciphertext, iv_hex


def send_push(device_key, params, method="post"):
    import urllib.request
    import urllib.parse

    base_url = f"{BARK_API}/{device_key}"

    if method == "post":
        url = f"{BARK_API}/push"
        payload = {"device_key": device_key, **params}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    else:
        query = urllib.parse.urlencode(params)
        url = f"{base_url}?{query}"
        req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            if result.get("code") == 200:
                print(f"推送成功: {result.get('message', '')}")
            else:
                print(f"推送失败: {result}")
            return result
    except urllib.error.HTTPError as e:
        print(f"HTTP 错误 {e.code}: {e.read().decode()}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"响应解析失败: {body}")
        sys.exit(1)


def main():
    config = load_config()
    defaults = config.get("defaults", {})

    parser = argparse.ArgumentParser(
        description="通过 Bark 向 iPhone 发送推送通知",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  bark_push.py --body "你好"
  bark_push.py --title "通知" --subtitle "副标题" --body "内容"
  bark_push.py --key my_iphone --body "测试" --group "test"
  bark_push.py --body "重要" --level critical --volume 8
  bark_push.py --markdown "# 标题\\n- 列表"
  bark_push.py --body "机密" --encrypt --encrypt-key "1234567890123456"
  bark_push.py --keys "dev1,dev2" --body "群发"
  bark_push.py --body "内容" --id "msg_001"   # 更新通知
  bark_push.py --id "msg_001" --delete         # 删除通知"""
    )

    parser.add_argument("--key", default="default", help="设备别名 (config.json 中配置)")
    parser.add_argument("--keys", help="批量推送，多个设备别名用逗号分隔")
    parser.add_argument("--title", help="推送标题")
    parser.add_argument("--subtitle", help="推送副标题")
    parser.add_argument("--body", help="推送内容")
    parser.add_argument("--markdown", help="Markdown 内容（传此参数忽略 body）")
    parser.add_argument("--level", choices=["active", "timeSensitive", "critical", "passive"],
                        default=defaults.get("level", "active"), help="推送中断级别")
    parser.add_argument("--volume", type=int, choices=range(0, 11),
                        help="重要警告音量 0-10")
    parser.add_argument("--badge", type=int, help="角标数字")
    parser.add_argument("--sound", default=defaults.get("sound"), help="铃声")
    parser.add_argument("--group", default=defaults.get("group"), help="分组")
    parser.add_argument("--icon", help="图标 URL")
    parser.add_argument("--image", help="图片 URL")
    parser.add_argument("--url", help="点击跳转 URL")
    parser.add_argument("--copy", help="复制时指定的内容")
    parser.add_argument("--autoCopy", choices=["1", "0"], help="自动复制")
    parser.add_argument("--call", choices=["1", "0"], help="铃声重复播放")
    parser.add_argument("--isArchive", choices=["1", "0"],
                        default=str(defaults.get("isArchive", "")), help="是否保存推送")
    parser.add_argument("--ttl", type=int, help="保存有效期（秒）")
    parser.add_argument("--id", help="通知 ID（用于更新或删除）")
    parser.add_argument("--delete", choices=["1"], help="删除通知，需配合 --id")
    parser.add_argument("--action", choices=["alert"], help="点击弹出操作弹窗")
    parser.add_argument("--encrypt", action="store_true", help="启用加密推送")
    parser.add_argument("--encrypt-key", help="加密密钥（16位）")
    parser.add_argument("--encrypt-iv", help="加密 IV（16位，不传则随机生成）")

    args = parser.parse_args()

    if not args.body and not args.markdown and not args.delete:
        parser.print_help()
        print("\n错误: 请提供 --body 或 --markdown 或 --delete")
        sys.exit(1)

    if args.delete and not args.id:
        print("错误: --delete 必须配合 --id 使用")
        sys.exit(1)

    params = {}
    for key in ("title", "subtitle", "body", "level", "sound", "group",
                 "icon", "image", "url", "copy", "autoCopy", "call",
                 "badge", "isArchive", "ttl", "id", "delete", "action"):
        val = getattr(args, key)
        if val is not None:
            val_str = str(val)
            if val_str:
                params[key] = val_str

    if args.markdown:
        params["markdown"] = args.markdown
        params.pop("body", None)

    if args.volume is not None:
        params["volume"] = str(args.volume)

    if args.encrypt:
        if not args.encrypt_key:
            print("错误: 加密推送需提供 --encrypt-key")
            sys.exit(1)
        ciphertext, iv_hex = encrypt_payload(params, args.encrypt_key, args.encrypt_iv)
        params = {"ciphertext": ciphertext, "iv": iv_hex}

    target_keys = []
    if args.keys:
        target_keys = [k.strip() for k in args.keys.split(",")]
    else:
        target_keys = [args.key]

    for alias in target_keys:
        device_key = get_device_key(config, alias)
        print(f"发送到设备 [{alias}]: ", end="")
        send_push(device_key, params)


if __name__ == "__main__":
    main()
