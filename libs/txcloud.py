from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
from swiper import config
import requests


def upload_to_tx(filename, filepath):
    # 设置用户属性, 包括secret_id, secret_key, region
    # appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
    token = None  # 使用临时密钥需要传入Token，默认为空,可不填
    cfg = CosConfig(Region=config.region, SecretId=config.secret_id, SecretKey=config.secret_key, Token=token)  # 获取配置对象
    client = CosS3Client(cfg)
    #### 高级上传接口（推荐）
    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    response = client.upload_file(
        Bucket='avatar-1259234619',
        LocalFilePath=filepath,
        Key=filename,
        PartSize=config.PartSize,
        MAXThread=config.MAXThread,
        EnableMD5=config.EnableMD5
    )
    print(response['ETag'])
    file_url = '%s/%s' % (config.BaseUrl, filename)
    print(file_url)
    return file_url