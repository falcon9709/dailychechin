# -*- coding: utf-8 -*-
import json
import os
import re

import requests


class WoMailCheckIn:
    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def login(womail_url):
        try:
            url = womail_url
            headers = {
                "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
            }
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("WT_FPC.*?;", set_cookie)[0]
            if "WT_FPC" in cookies:
                return cookies
            else:
                print("沃邮箱获取 cookies 失败")
                return None
        except Exception as e:
            print("沃邮箱错误:", e)
            return None

    @staticmethod
    def dotask(cookies):
        msg = ""
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
            "Cookie": cookies,
        }
        try:
            url = "https://wap.sn.10086.cn/h5/SignInForTreasure/html/SignIndex.html?&targetId=WXE018&token=9aa3c77c36294e10a4f96f8a4edd3c93"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxName = result.get("result").get("wxName")
            userMobile = result.get("result").get("userMobile")
            userdata = f"帐号信息: {wxName} - {userMobile[:3]}****{userMobile[-4:]}\n"
            msg += userdata
        except Exception as e:
            print("沃邮箱获取用户信息失败", e)
            msg += "沃邮箱获取用户信息失败\n"
        try:
            url = "https://wap.sn.10086.cn/h5/SignInForTreasure/html/SignIndex.html?&targetId=WXE018&token=9aa3c77c36294e10a4f96f8a4edd3c93"
            res = requests.post(url=url, headers=headers).json()
            result = res.get("result")
            if result == -2:
                msg += "每日签到: 已签到\n"
            elif result is None:
                msg += f"每日签到: 签到失败\n"
            else:
                msg += f"每日签到: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"

        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        return msg

if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/config.json"), "r", encoding="utf-8"
    ) as f:
        datas = json.loads(f.read())
    _check_item = datas.get("WOMAIL_URL_LIST", [])[0]
    print(WoMailCheckIn(check_item=_check_item).main())
