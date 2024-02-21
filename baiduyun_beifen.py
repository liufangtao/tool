import argparse
import requests
import json
import os
import hashlib
from urllib.parse import urlencode
import datetime

app_name = '中转'
# apps对应百度云盘我的应用数据文件夹
remote_path_prefix = '/apps/' + app_name
json_path = './token.json'
# access_token获取地址
access_token_api = 'https://openapi.baidu.com/oauth/2.0/token'
# 预创建文件接口
precreate_api = 'https://pan.baidu.com/rest/2.0/xpan/file?'
# 分片上传api
upload_api = 'https://d.pcs.baidu.com/rest/2.0/pcs/superfile2?'
# 创建文件api
create_api = 'https://pan.baidu.com/rest/2.0/xpan/file?'
app_key = 'q9ZaCn2BGCsBl4UmkcDrsR3ZZtXGa7tS'
secret_key = 'BcMBMU9p56PUVuKogZz2olgTYBGs8QIA'

class BaiduPanHelper:
    def __init__(self, code):
        self.code = code
        # self.refresh_token = ''
        # self.access_token = ''

    # 创建文件
    def create(self, remote_path, size, uploadid, block_list):
        params = {
            'method': 'create',
            'access_token': self.access_token,
        }
        api = create_api + urlencode(params)
        data = {
            'path': remote_path,
            'size': size,
            'isdir': 0,
            'uploadid': uploadid,
            'block_list': block_list
        }
        response = requests.post(api, data=data)

    # 分片上传
    def upload(self, remote_path, uploadid, partseq, file_path):
        data = {}
        files = [
            ('file', open(file_path, 'rb'))
        ]
        params = {
            'method': 'upload',
            'access_token': self.access_token,
            'path': remote_path,
            'type': 'tmpfile',
            'uploadid': uploadid,
            'partseq': partseq
        }
        api = upload_api + urlencode(params)
        res = requests.post(api, data=data, files=files)

    # 预上传
    def precreate(self, file_path):
        remote_path = remote_path_prefix
        size = os.path.getsize(file_path)
        arr = file_path.split('/')
        for item in arr[-2::]:
            remote_path = os.path.join(remote_path, item)
        block_list = []
        with open(file_path, 'rb') as f:
            data = f.read()
            file_md5 = hashlib.md5(data).hexdigest()
            block_list.append(file_md5)
            f.close()
        block_list = json.dumps(block_list)
        params = {
            'method': 'precreate',
            'access_token': self.access_token,
        }
        data = {
            'path': remote_path,
            'size': size,
            'isdir': 0,
            'autoinit': 1,
            'block_list': block_list
        }
        api = precreate_api + urlencode(params)
        res = requests.post(api, data=data)
        json_resp = json.loads(res.content)
        if "path" in json_resp:
            return json_resp['uploadid'], remote_path, size, block_list
        else:
            return '', remote_path, size, block_list

    # 取得缓存的token
    def get_cache_token(self):
        with open(json_path, 'r') as f:
            data = json.load(f)
            self.refresh_token = data['refresh_token']
            self.access_token = data['access_token']
            print(self.refresh_token)
            print(self.access_token)
            f.close()

    # 根据授权码获取token
    def get_access_token(self):
        data = {
            'grant_type': 'authorization_code',
            'code': self.code,
            'client_id': app_key,
            'client_secret': secret_key,
            'redirect_uri': 'oob'
        }
        res = requests.post(access_token_api, data=data)
        json_resp = json.loads(res.content)
        self.refresh_token = json_resp['refresh_token']
        self.access_token = json_resp['access_token']
        with open(json_path, 'wb') as f:
            f.write(res.content)
            f.close()

    def update_file(self, file_path):
        # 1. 预上传
        uploadid, remote_path, size, block_list = self.precreate(file_path)
        # 2. 分片上传（文件切片这里没有做，超级会员单文件最大20G）
        self.upload(remote_path, uploadid, 0, file_path)
        # 3. 创建文件
        self.create(remote_path, size, uploadid, block_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='百度云盘api测试')
    parser.add_argument('--code', type=str, default='', help='授权码')
    args = parser.parse_args()
    bdpan = BaiduPanHelper(args.code)
    if bdpan.code is '':
        print('CODE is null')
        bdpan.get_cache_token()
    else:
        print('CODE:' + args.code)
        bdpan.get_access_token()

    # 批量上传某个目录下的所有文件
    for root, dirs, files in os.walk('/1T/liufangtao/ultralytics_cx'):
        for file in files:
            file_path = os.path.join(root, file)
            bdpan.update_file(file_path)
            print(file_path)



def get_yesterday(include_time=False):
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    if include_time:
        return yesterday.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return yesterday.strftime('%Y-%m-%d')

# 获取昨天的日期
print(get_yesterday())  # 输出：2022-07-29

# 获取昨天的时间
print(get_yesterday(True))