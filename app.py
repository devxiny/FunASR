import random
import requests
import uuid
import os


def tts_request(text, output_file):
    # 定义请求的URL
    url = "http://127.0.0.1:8080/v1/tts"

    # 定义请求的JSON数据
    data = {
        "text": text,
        "chunk_length": 200,
        "format": "wav",
        "mp3_bitrate": 64,
        "references": [],
        "reference_id": None,
        "normalize": True,
        "opus_bitrate": -1000,
        "latency": "normal",
        "streaming": False,
        "emotion": None,
        "max_new_tokens": 1024,
        "top_p": 0.7,
        "repetition_penalty": 1.2,
        "temperature": 0.7,
    }

    # 发送POST请求
    response = requests.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        make_sure_directory_exit(output_file)
        # 保存响应内容为WAV文件
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"音频文件已保存为 {output_file}")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")


import re


def remove_special_characters(text):
    # 定义一个正则表达式模式，匹配所有非字母、非数字、非空格的字符
    pattern = r"[^a-zA-Z0-9\s]"
    # 使用 re.sub 替换所有匹配的字符为空字符串
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def make_sure_directory_exit(file_path):
    # 获取文件所在的目录
    directory = os.path.dirname(file_path)

    # 如果目录不存在，则创建目录
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def random_chinese_number():
    # 生成1到10之间的随机整数
    number = random.randint(1, 10)

    # 汉语数字字典
    chinese_numbers = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
        10: "十",
    }

    # 返回对应的汉语数字
    return chinese_numbers[number]


def append_to_file(file_path, content):
    """
    将指定内容追加到文件末尾。如果文件目录不存在，则自动创建目录。

    参数:
    file_path (str): 文件路径
    content (str): 要追加的内容
    """
    make_sure_directory_exit(file_path)

    # 打开文件并追加内容
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content + "\n")


def specification():
    return random_chinese_number() + "规格"


def near_expiry():
    return random_chinese_number() + "临期"


def shelf():
    return random_chinese_number() + "货架"


def pile_head():
    return random_chinese_number() + "堆头"


# if __name__ == "__main__":
#     directory = "train"
#     for index in range(10):
#         id = uuid.uuid4().hex
#         list = [specification(), near_expiry(), shelf(), pile_head()]
#         random.shuffle(list)
#         text = "".join(map(str, list))
#         tts_request(text, f"dataset/{directory}/{id}.wav")
#         append_to_file(
#             f"dataset/{directory}.scp",
#             id + " " + f"dataset/{directory}/{id}.wav",
#         )
#         append_to_file(f"dataset/{directory}.txt", id + " " + text)

if __name__ == "__main__":
    directory = "val"
    for index in range(100):
        id = uuid.uuid4().hex
        list = [
            "健仔" + random_chinese_number() + "个",
            "弱仔" + random_chinese_number() + "个",
            "畸形" + random_chinese_number() + "个",
            "白仔" + random_chinese_number() + "个",
            "黑仔" + random_chinese_number() + "个",
            "窝总重" + random_chinese_number() + "公斤",
        ]
        random.shuffle(list)
        text = "".join(map(str, list))
        tts_request(text, f"dataset/{directory}/{id}.wav")
        append_to_file(
            f"dataset/{directory}.scp",
            id + " " + f"dataset/{directory}/{id}.wav",
        )
        append_to_file(f"dataset/{directory}.txt", id + " " + text)
