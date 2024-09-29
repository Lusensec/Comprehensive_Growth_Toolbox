from openai import OpenAI
from fun import *

def kimi_ai(msg, ai_api):
    client = OpenAI(
        api_key=ai_api,
        base_url="https://api.moonshot.cn/v1",
    )

    history = [
        {"role": "system", "content": "您是 Kimi，由 Moonshot AI 提供的人工智能助手……"}
    ]

    def chat(query, history):
        try:
            history.append({"role": "user", "content": query})
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=history,
                temperature=0.3,
            )
            result = completion.choices[0].message.content
            history.append({"role": "assistant", "content": result})
            return result
        except Exception as e:
            print(f"发生错误：{e}")
            return None

    return chat(msg, history)

def ai_main(ai_name,msg):
    global ai_json

    for ai_names in get_ai_json_name_all():
        if ai_name == ai_names:
            # 获取当前ai的api
            return kimi_ai(msg=msg,ai_api=get_ai_json_one_api(ai_name=ai_name))
