# 与API交互的函数
# 由于这个只是一个聊天程序，只考虑/v1/chat/completions这个断点
import json
import requests
import datetime
def stream_response(url,api_key,model,messages,temperature,proxy_url,max_tokens):
    """
    params:
        url: api的url(方便使用第三方API的用户)
        api_key: api的key(从openai/第三方提供商获取)
        model: 模型名称
        messages: 对话内容
        temperature: 温度(随机性，越高越随机)
        proxy_url: 代理地址(接受socks,http,https)
        max_tokens: 最大生成长度
    return:
        content: 生成的内容
        created_time: 生成的时间(标准日期格式)     
    """
    if not url:
        url="https://api.openai.com/v1/chat/completions"
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True, proxies=proxies)
    for line in response.iter_lines():
        decoded_line = line.decode('utf-8')
        # 删除"data:"前缀
        json_line_str = decoded_line.split("data:", 1)[-1].strip()
        if not json_line_str:
            continue
        json_line_dic = json.loads(json_line_str)
        if json_line_dic["choices"][0]["finish_reason"] == "stop" :
            break
        content = json_line_dic["choices"][0]["delta"]["content"]
        yield content
        # 由于API不返回我又懒得做，所以流式回答没算token数
def single_response(url,api_key,model,messages,temperature,proxy_url,max_tokens): 
    """
    params:
        url: api的url(方便使用第三方API的用户)
        api_key: api的key(从openai/第三方提供商获取)
        model: 模型名称
        messages: 对话内容
        temperature: 温度(随机性，越高越随机)
        proxy_url: 代理地址(接受socks,http,https)
        max_tokens: 最大生成长度
    return:
        return_content: 生成的内容
        tokens_cost_total: 生成的token数(提问+回答)  
        created_time: 生成的时间(标准日期格式)     
    """
    if not url:
        url="https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,

    }
    response = requests.post(url, headers=headers, data=json.dumps(payload),proxies=proxies)
    return_content = response.json()["choices"][0]["message"]["content"]
    tokens_cost_total = response.json()["usage"]["total_tokens"]
    created_time = datetime.fromtimestamp(int(response.json()["created"]))
    return return_content,tokens_cost_total,created_time

