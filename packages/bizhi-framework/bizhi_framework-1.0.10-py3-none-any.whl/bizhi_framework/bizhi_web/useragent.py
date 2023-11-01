
from app_encrypt import *
from seven_framework import CodingHelper

class UserAgnetHelper:
    def get_useragent(self):
        """
        @description:获取app客户端头部信息
        @return：返回头部信息
        @last_editors: HuangWenBin
        """
        user_agent= UserAgentInfo()
        dic_header=self.request.headers
        if "User-Agent1" not in dic_header:
            return user_agent
        user_agent1=dic_header._dict["User-Agent1"]
        if user_agent1.startswith("2"):
            user_agent1=user_agent1[1:]
        #dict_useragent={}
        decrypt=app_des_encrypt()
        user_agent1=decrypt.des_decrypt(user_agent1)
        list_str = str.split(CodingHelper.url_decode(user_agent1.decode("unicode_escape")), "&")

        for item in list_str:
            key,value=item.split("=")
            if hasattr(user_agent, key):
                if key in["pid","pt","ch","ver","adolescent","login"]:
                    if value:
                        setattr(user_agent, key, int(value))
                    else:
                        setattr(user_agent, key, 0)
                else:
                    setattr(user_agent, key, value)

        user_agent.userip=self.get_remote_ip()
        return user_agent


class UserAgentInfo():
    def __init__(self):
        self.ch="0"
        self.simidfa=""
        self.lang=""
        self.adtid=""
        self.mtype=""
        self.nickname=""
        self.openid=""
        self.osver=""
        self.adolescent=""
        self.uidsign=""
        self.g7udid=""
        self.token=""
        self.ver=0
        self.idfv=""
        self.login=0
        self.pid=0
        self.sdkver="0"
        self.pt=0
        self.screen=""
        self.userip=""
        self.ua=""
        self.net=""