import openai
import json
import requests
def stream_response(url,headers,data):
    if not url:
        url="https://api.openai.com/v1/chat/completions"
    
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
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
        if json_line_dic["choices"][0]["finish_reason"] == "stop":
            print(content, end="\n")
        else:
            print(content, end="", flush=True)

