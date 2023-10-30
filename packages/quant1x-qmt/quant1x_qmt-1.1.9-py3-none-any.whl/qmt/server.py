# 创建策略
# coding=utf-8

import base64

import uvicorn
from fastapi import FastAPI
from fastapi import Form as HttpForm
from fastapi import Response as HttpResponse
from path import Path

import qmt.trade_pb2 as tp

app = FastAPI()


@app.post('/protobuf')
async def _protobuf(pyload: bytes = HttpForm(...)):
    pyload = base64.b64decode(pyload)
    print(pyload)
    # 解析请求
    req = tp.Request()
    req.ParseFromString(pyload)
    print(req)

    # 编写响应
    res = tp.Response()
    res.status = 0
    res.message = 'success'
    print(res.SerializeToString())
    return HttpResponse(res.SerializeToString())


if __name__ == '__main__':
    uvicorn.run(
        app=f'{Path(__file__).stem}:app',
        host="0.0.0.0",
        port=8899,
        workers=4,
        reload=True,
        debug=True)
