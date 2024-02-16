import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger


@plugins.register(name="bagua",
                  desc="bagua插件",
                  version="1.0",
                  author="masterke",
                  desire_priority=100)
class bagua(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[bagua] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送八卦获取"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        content = e_context["context"].content.strip()
        
        if content == "八卦":
            logger.info(f"[bagua] 收到消息: {content}")   
            reply = Reply()
            result = self.bagua()
            if result != None:
                reply.type = ReplyType.IMAGE_URL
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
                json_data = response.json()
                if json_data.get('code',None) == 200 and json_data.get('data',None):
                    img_url = json_data['data']
                    return img_url
                else:
                    logger.info(f"错误信息：{json_data}")
                    return "周末不更新，请微博吃瓜"
            else:
                logger.error(f"请求失败:{response.status_code}")
                return "暂无明星八卦，吃瓜莫急"
        except Exception as e:
            logger.error(f"bagua接口抛出异常:{e}")

        logger.error("所有接口都挂了,无法获取")
        return None