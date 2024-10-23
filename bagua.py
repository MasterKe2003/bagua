import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger


@plugins.register(name="bagua",
                  desc="bagua插件",
                  version="1.1",
                  author="masterke",
                  desire_priority=100)
class bagua(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[bagua] inited")
    def on_handle_context(self, e_context: EventContext):
        # =======================只处理的消息==========================
        if e_context['context'].type != ContextType.TEXT:
            return
        self.message = e_context["context"].content.strip()
        if self.message != "八卦":
            return
        # =======================读取配置文件==========================
        logger.info(f"[{__class__.__name__}] 收到消息")
        # =======================插件处理流程==========================
        result, result_type = self.bagua()
        reply = Reply()
        if result != None:
            reply.type = result_type
            reply.content = result
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,等待修复⌛️"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def bagua(self):
        url = "https://dayu.qqsuu.cn/mingxingbagua/apis.php?type=json"
        payload = "format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            response = requests.post(url, headers=headers, data=payload)
            # 验证请求是否成功
            if response.status_code == 200:
                rjson = response.json()
                if rjson.get('data'):
                    return rjson['data'], ReplyType.IMAGE_URL
                else:
                    logger.info(f"bagua返回错误:{rjson}")
                    return "👏周末不更新，请微博吃瓜~", ReplyType.TEXT
            else:
                logger.error(f"请求失败:{response.status_code}")
                return "⌛️暂无明星八卦，吃瓜莫急~", ReplyType.TEXT
        except Exception as e:
            logger.error(f"bagua抛出异常:{e}")
    def get_help_text(self, **kwargs):
        help_text = f"【八卦】获取明星吃瓜榜"
        return help_text