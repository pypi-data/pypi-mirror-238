import glob
import hashlib
import io
import json
import multiprocessing
import os
import tarfile
import threading
import time
import urllib
import warnings
from pathlib import Path
from datetime import datetime
import re

import jsonlines
from tqdm import tqdm


def load_list_file(path: str):
    with open(path, 'r', encoding='utf=8') as f:
        cat_to_name: list = f.readlines()
        print("数据总条数为:", len(cat_to_name))
    return cat_to_name


def write_list_to_file(data_list: list, path: str):
    makedir_for_file(path)
    with open(path, 'w', encoding='utf=8') as f:
        for data in data_list:
            f.write(data + '\n')


def load_json_file(path):
    with open(path, 'r', encoding='utf=8') as f:
        cat_to_name: dict = json.load(f)
        print("数据总条数为:", len(cat_to_name))
    return cat_to_name


def load_jsonl_file(jsonl_file_path):
    """"""
    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("数据总条数为:", len(lines))
        lines = [json.loads(x) for x in lines]
        return lines


def write_dict_to_json(dic, json_file_path):
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)


def write_dictlist_to_jsonl(dict_list, jsonl_file_path):
    os.makedirs(os.path.dirname(jsonl_file_path), exist_ok=True)
    if os.path.exists(jsonl_file_path):
        os.remove(jsonl_file_path)
    for dic in dict_list:
        with jsonlines.open(jsonl_file_path, mode='a') as f:
            f.write(dic)


def write_single_dict_to_jsonl(dic, jsonl_file_path):
    with jsonlines.open(jsonl_file_path, mode='a') as f:
        f.write(dic)


def write_dic_to_scp(dic: dict, scp_file_path: str):
    os.makedirs(os.path.dirname(scp_file_path), exist_ok=True)
    with open(scp_file_path, 'w', encoding='utf-8') as f:
        for k, v in dic.items():
            f.write(f"{k} {v}\n")


def makedir(path: Path | str):
    if isinstance(path, str):
        path = Path(path)
        # os.makedirs(path)
    if not path.exists():
        print(f'路径{path.absolute()}不存在,现创建')
        path.mkdir(parents=True, exist_ok=True)
    else:
        print(f'路径{path.absolute()}已存在,不用创建')


def makedir_sil(path: Path | str):
    if isinstance(path, str):
        os.makedirs(path, exist_ok=True)
        return
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def makedir_for_file(filepath: Path | str):
    # dirpath = os.path.dirname(filepath)
    if isinstance(filepath, str):
        filepath = Path(filepath)
    dirpath = filepath.parent
    makedir_sil(dirpath)


def makedir_for_file_or_dir(filepath: Path | str):
    def ends_with_dot_and_non_slash_backslash(text):
        pattern = r'\.[^/\\]+$'
        return re.search(pattern, text) is not None

    # dirpath = os.path.dirname(filepath)
    if ends_with_dot_and_non_slash_backslash(filepath):
        makedir_for_file(filepath)
    else:
        makedir_sil(filepath)


def get_now(format='%Y-%m-%d_%H-%M-%S'):
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化日期为字符串
    formatted_date = current_datetime.strftime(format)
    return formatted_date


def _join_path(path1, path2):
    if path1 is None or path2 is None or len(path1) == 0 or len(path2) == 0:
        return ""
    while path1[-1] == '/' or path1[-1] == '\\':
        path1 = path1[:-1]
    while path2[0] == '/' or path2[0] == '\\':
        path2 = path2[1:]
    return f'{path1}/{path2}'


def join_path(*args):
    """
    安全拼接若干路径, 再也不用担心分路径结尾和开头的分隔符的困扰了
    """
    lens = len(args)
    if lens == 0:
        return ""
    path = args[0]
    for i in range(1, lens):
        path = _join_path(path, args[i])
    return path


def get_now_str():
    """
    获取当前时间
    格式为： 2023_10_14_16_18_16
    """
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    return now_time


def load_dic_from_scp(label_scp_file):
    res = {}
    with open(label_scp_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            items = line.split()
            if len(items) < 2:
                print('warning_gxl:, this row not conform to the regulation of scp(key content) and skip it:', line)
                continue
            elif len(items) == 2:
                res[items[0]] = items[1]
            else:
                print(
                    'warning_gxl:, this row not conform to the regulation of'
                    ' scp(key content) and no skip it,第一个为key,剩下的都是value:',
                    line)
                res[items[0]] = ' '.join(items[1:])
    return res


def convert_wav_text_scp_to_jsonl(wav_scp_file_path: str, text_scp_file_path, target_jsonl_file_path: str):
    """
    convert wav text scp to jsonl
    """
    makedir_for_file(target_jsonl_file_path)
    wav_dic = load_dic_from_scp(wav_scp_file_path)
    text_dic = load_dic_from_scp(text_scp_file_path)
    if len(wav_dic) != len(text_dic):
        print("warning: wav_scp文件和text_scp文件长度不一致")
    os.remove(target_jsonl_file_path)
    for k, v in wav_dic.items():
        if k not in text_dic:
            print('warning: {} not in text_dic'.format(k))
            continue
        text = text_dic[k]
        write_single_dict_to_jsonl({k: {'wav': v, 'text': text}}, target_jsonl_file_path)


def convert_wav_text_scp_to_json(wav_scp_file_path: str, text_scp_file_path, target_json_file_path: str):
    """
    convert wav text scp to json
    """
    makedir_for_file(target_json_file_path)
    wav_dic = load_dic_from_scp(wav_scp_file_path)
    text_dic = load_dic_from_scp(text_scp_file_path)
    if len(wav_dic) != len(text_dic):
        print("warning: wav_scp文件和text_scp文件长度不一致")
    os.remove(target_json_file_path)
    res_dic = {}
    for k, v in wav_dic.items():
        if k not in text_dic:
            print('warning: {} not in text_dic'.format(k))
            continue
        text = text_dic[k]
        res_dic[k] = {'wav': v, 'text': text}
    write_dict_to_json(res_dic, target_json_file_path)


def get_file_pure_name_from_path(path: str):
    return os.path.splitext(os.path.basename(path))[0]


def get_scp_for_wav_dir(wav_dir: str, wav_scp_file_path: str):
    makedir_for_file(wav_scp_file_path)
    wav_path_list = glob.glob(join_path(wav_dir, "*.wav"))
    with open(wav_scp_file_path, 'w', encoding='utf-8') as f:
        for wav_path in wav_path_list:
            f.write(f"{get_file_pure_name_from_path(wav_path)} {wav_path}\n")


def get_clean_filename(filename: str):
    """
    将一个字符串转为一个可以作为文件名的形式, 将非法字符替换为-
    """
    # 移除非法字符
    cleaned_filename = re.sub(r'[\/:*?"<>|]', '-', filename)
    # 截断文件名，以确保它在不同系统下都有效, 本来是255, 但实验表明在windows下还是因为长度报错了,所有索性改为25
    cleaned_filename = cleaned_filename[:25]
    return cleaned_filename


class GxlDownloader:
    encrypted_hash_file_name = 'encrypted_hash.json'
    encrypted_dict = {}

    def __init__(self, root_dir: str):
        """"""
        makedir_sil(root_dir)
        self.root = root_dir
        self.suffix = 'gxlfile'
        # self.file_lock = threading.Lock()
        if os.path.exists(os.path.join(self.root, self.encrypted_hash_file_name)):
            self.encrypted_dict = load_json_file(os.path.join(self.root, self.encrypted_hash_file_name))

    def __del__(self):
        print(f"Object {self} is being destroyed")
        write_dict_to_json(self.encrypted_dict, os.path.join(self.root, self.encrypted_hash_file_name))

    @classmethod
    def generate_hash(cls, input_file: bytes | str, hash_algorithm='sha256'):
        """
        读取一个文件的数据， 并生成其对应的hash值
        """
        # 读取文件的字节数据
        if isinstance(input_file, str):
            with open(input_file, 'rb') as file:
                data = file.read()
        else:
            data = input_file
        # 使用指定哈希算法计算哈希值
        hash_function = hashlib.new(hash_algorithm)
        hash_function.update(data)
        hash_value = hash_function.hexdigest()

        return hash_value

    def get_expected_encrypted_for_filename(self, filename):
        """"""
        return self.encrypted_dict.get(filename, None)

    def add_encrypted_hash_item(self, filename: str):
        """"""
        self.encrypted_dict[filename] = self.generate_hash(os.path.join(self.root, filename))

    def set_suffix(self, suffix: str):
        self.suffix = suffix

    def download(self, url: str, suffix: str = None, filename: str = None):
        if filename is None:
            filename = get_clean_filename(os.path.basename(url))
        if suffix is None:
            suffix = self.suffix
        filename = filename + "." + suffix
        print(f'开始下载:{filename},url:{url}')
        download_target = os.path.join(self.root, filename)
        expected_sha256 = self.get_expected_encrypted_for_filename(filename)
        if os.path.exists(download_target) and os.path.isfile(download_target):
            if self.generate_hash(download_target) == expected_sha256:
                print('文件已经存在')
                return download_target
            else:
                warnings.warn(
                    f"{download_target} exists, but the SHA256 checksum does not match; re-downloading the file"
                )

        with urllib.request.urlopen(url) as source, open(download_target, "wb") as output:
            with tqdm(
                    total=int(source.info().get("Content-Length", -1)),
                    ncols=80,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
            ) as loop:
                while True:
                    buffer = source.read(8192)
                    if not buffer:
                        break
                    output.write(buffer)
                    loop.update(len(buffer))
        self.add_encrypted_hash_item(filename)
        print(f'下载完成:{filename},url:{url}')
        return download_target
