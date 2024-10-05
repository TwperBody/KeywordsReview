from pkg.plugin.models import *
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext

import json

message_string = ""

file_path = 'plugins/KeywordsReview/keywords.json'

# 注册插件
@register(name="Keyword_active_review", description="关键词主动审查", version="1.0", author="TwperBody")
class KeywordActiveReviewPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    async def initialize(self):
        pass

    # 当收到user消息时触发
    @handler(PersonNormalMessageReceived)
    async def PersonNormalMessageReceived(self, ctx: EventContext):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        keywords = data.get('keywords', [])
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象

        for keyword_dict in keywords:
            message_string = keyword_dict.get('keyword', '')
            if message_string in msg:
                self.ap.logger.debug("{} is trigger keyword".format(ctx.event.sender_id))
                ctx.add_return("reply", ["客户端拒绝请求, {}!".format(ctx.event.sender_id)])
                # 阻止该事件默认行为（向接口获取回复）
                ctx.prevent_default()
                break


    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        keywords = data.get('keywords', [])
        if " " or "@" in msg:
            msg = ctx.event.text_message  # 这里的 event 即为 GroupMessageReceived 的对象
            for keyword_dict in keywords:
                message_string = keyword_dict.get('keyword', '')
                if message_string in msg:
                    self.ap.logger.debug("{} is trigger keyword".format(ctx.event.sender_id))
                    ctx.add_return("reply", ["客户端拒绝请求, {}!".format(ctx.event.sender_id)])
                    # 阻止该事件默认行为（向接口获取回复）
                    ctx.prevent_default()
                    break

    # 插件卸载时触发
    def __del__(self):
        pass
