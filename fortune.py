import requests
import json

flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上
plugin_name = "今日运势"
plugin_viasion = "V1.0.1"

def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print(plugin_name, plugin_viasion,"加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    print(flora_api)


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    try:
        global ws_client
        global ws_server
        send_address = data.get("SendAddress")
        ws_client = send_address.get("WebSocketClient")
        ws_server = send_address.get("WebSocketServer")
    except:
        ws_server=None
        ws_client=None
        pass
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        if msg == "#今日运势":
            fortune_url = f"https://api.fanlisky.cn/api/qr-fortune/get/{uid}"
            response = requests.get(fortune_url)
            data_dict = response.json()
            fortune_data = data_dict["data"]
            send_compatible(msg=f"[CQ:at,qq={uid}]\n今日运势：\n{fortune_data["fortuneSummary"]}\n    {fortune_data["luckyStar"]}\n运势：{fortune_data["signText"]}\n---------------------\n建议：{fortune_data["unSignText"]}", uid=uid, gid=gid, mid=mid)
        if msg == "#一言":
            yy_url = f"https://api.fanlisky.cn/niuren/getSen"
            response_yy = requests.get(yy_url)
            yy_dict = response_yy.json()
            send_compatible(msg=f"[CQ:at,qq={uid}]\n{yy_dict["data"]}", uid=uid, gid=gid, mid=mid)
        if msg == "#二次元图片":
            ecy_url = f"https://www.loliapi.com/acg/?type=url"
            response_ecy = requests.get(ecy_url)
            ery_dict = response_ecy.text
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={ery_dict}]", uid=uid, gid=gid, mid=mid)
        if msg == "#二次元头像":
            ecytx_url = f"https://www.loliapi.com/acg/pp/"
            response_ecytx = requests.get(ecytx_url)
            ecytxcdx_url = response_ecytx.url
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={ecytxcdx_url}]", uid=uid, gid=gid, mid=mid)
        if msg == "#疯狂星期四":
            crazy_thursday_url = f"https://api.shadiao.pro/kfc"
            response_crazy_thursday = requests.get(crazy_thursday_url)
            data_dict = response_crazy_thursday.json()
            send_compatible(msg=f"[CQ:at,qq={uid}]\n{data_dict["data"]["text"]}", uid=uid, gid=gid, mid=mid)
        if msg == "#.帮助":
            send_compatible(msg=f"[CQ:at,qq={uid}]\n{plugin_name}{plugin_viasion} 插件\n----------------\n命令：\n#今日运势 查看今日的运势（仅娱乐）\n#一言 获取一言\n#二次元图片 返回随机二次元图片\n#二次元头像 返回随机的二次元头像\n#疯狂星期四 获取疯狂星期四文案\n----------------", uid=uid, gid=gid, mid=mid)

def send_compatible(msg:str,gid:str|int,uid: str|int,mid:str|int=None):  #兼容性函数,用于兼容旧版本API(请直接调用本函数)
    if flora_api.get("FloraVersion") == 'v1.01': #旧版本API
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid)
    else:
        send_type=flora_api.get("ConnectionType")
        send_address=flora_api.get("FrameworkAddress")
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid,send_type=send_type,ws_client=ws_client,ws_server=ws_server)