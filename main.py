import json
import os
import random
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register

# 定义一个函数，用于从 JSON 文件中读取列表
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("data", [])

@register("helloworld", "Your Name", "一个简单的 Hello World 插件", "1.0.0", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        
        # 获取当前文件的绝对路径
        path = os.path.abspath(os.path.dirname(__file__))
        json_file_path = os.path.join(path, "resources", "food.json")
        
        # 从 JSON 文件中加载数据
        self.responses = load_data_from_json(json_file_path)

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令'''
        user_name = event.get_sender_name()  # 获取用户昵称
        message_str = event.message_str  # 获取消息的纯文本内容
        
        # 从列表中随机选择一条消息
        response = random.choice(self.responses)
        
        # 发送回复消息
        yield event.plain_result(f"Hello, {user_name}! {response}")
