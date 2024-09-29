import requests
import hashlib
import random

def translate_text(text, from_lang='zh', to_lang='en'):
    app_id = '20240824002131633'  # 替换为你的百度翻译API应用ID
    secret_key = 'cyHyuMGfdHlIZTHXRFIS'  # 替换为你的百度翻译API密钥
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    salt = random.randint(32768, 65536)
    sign = app_id + text + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()

    params = {
        'q': text,
        'from': from_lang,
        'to': to_lang,
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(url, params=params)
    result = response.json()
    if 'trans_result' in result:
        return result['trans_result'][0]['dst']
    else:
        return "Error: Translation failed or response format changed."

if __name__ == "__main__":
    text_to_translate = "Hello, world"
    translated_text = translate_text(text_to_translate, from_lang='en', to_lang='zh')
    print(f"Translated Text: {translated_text}")
