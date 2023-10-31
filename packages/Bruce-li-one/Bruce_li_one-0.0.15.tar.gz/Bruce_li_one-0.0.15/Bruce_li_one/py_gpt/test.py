import SparkApi





text = []


# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

class Py_gpt_config:
    def __init__(self,appid,api_secret,api_key,gpt_version="2"):
        self.Spark_url=None#云端环境的服务地址
        self.domain=""#用于配置大模型版本
        self.appid=appid
        self.api_secret=api_secret
        self.api_key=api_key
        if gpt_version=='2':
            self.version_2_0()
        else:
            self.version_1_5()

    def version_1_5(self):
        self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
        self.domain="general"

    def version_2_0(self):
        self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"
        self.domain = "generalv2"

def xfxun_gpt(rq_text:str,appid,api_secret,api_key):
    global text
    text.clear()
    Input =rq_text
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    py_config=Py_gpt_config(appid,api_secret,api_key)
    SparkApi.main(py_config.appid, py_config.api_key, py_config.api_secret, py_config.Spark_url, py_config.domain, question)
    getText("assistant", SparkApi.answer)


