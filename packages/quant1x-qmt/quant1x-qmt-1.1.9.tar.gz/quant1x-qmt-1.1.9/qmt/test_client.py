import base64

import requests

import qmt.trade_pb2 as tp


def test_protobuf():
    """
    test
    :return:
    """
    req = tp.Request()
    req.date = "2023-09-01"  # 1; // 时间戳
    req.code = "sh600105"  # 2; // 证券代码
    req.name = "永鼎股份"  # 3; // 证券名称
    req.strategy_id = "0"  # 4; // 策略id
    req.strategy_name = "0号策略"  # 5; // 策略名称
    req.phase = "head"  # 6; // 交易阶段, 早盘或者尾盘
    req.price = 1.23  # 7; // 价格, 单位元
    req.volume = int(10000.34)  # 8; // 数量, 单位股
    req.update_time = "2023-09-21 09:28:30"  # 9; // 时间戳
    req_bytes = req.SerializeToString()
    print('request =', req_bytes)
    data = {'pyload': base64.b64encode(req_bytes)}
    print(data)
    req1 = tp.Request()
    req1.ParseFromString(req_bytes)
    print(req1)
    response = requests.post("http://127.0.0.1:8899/protobuf", data=data)

    res = tp.Response()
    res.ParseFromString(response.content)
    print(res)


if __name__ == '__main__':
    test_protobuf()
