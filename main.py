#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

import asyncio
import sys
import os

from pymongo import MongoClient

# RabbbitMQモジュール
from rabbitmq_client import RabbitmqClient

# AION共通モジュール
from aion.logger import lprint
from aion.microservice import main_decorator, Options, WITH_KANBAN

# 環境変数の取得
MODE = os.environ["MODE"]
MONGO_CLIENT = os.environ["MONGO_CLIENT"]
DB_NAME = os.environ["DB_NAME"]
RABBITMQ_CLIENT = os.environ.get("RABBITMQ_CLIENT","NO_SETTING")
SERVICE_NAME = os.environ.get("SERVICE_NAME","NO_SETTING")
RABBITMQ_CLIENT = os.environ.get("RABBITMQ_CLIENT","NO_SETTING")
RABBITMQ_QUEUE_NAME = os.environ.get("RABBITMQ_QUEUE_NAME","NO_SETTING")

class MongoDb(object):
    def __init__(self):
         self.clint = MongoClient(MONGO_CLIENT)
         self.db = self.clint[DB_NAME]

    def addDb(self,post):
        self.db.test.insert_one(post)

class RabbitMq():
    async def init(self, _):
        self.consumer = await RabbitmqClient.create(
            RABBITMQ_CLIENT,
            [RABBITMQ_QUEUE_NAME],
            []
        )
    
    async def setData(self,db):
        async for message in self.consumer.iterator():
            # 何らかの理由でメッセージを後から再処理したいとき等、
            # 再度キューに戻すときは、await message.requeue() を実行する
            try:
                print(f'received from {message.queue_name}')
                print('data:', message.data)
                
                db.addDb(message.data)
                print(message.data)

                # 処理成功
                await message.success()

            except Exception:
                # 処理失敗
                # メッセージがデッドレターという別のキューに入る (定義されている場合)
                await message.fail()
                print('failed!')

class Kanban():
    async def init(self,opt: Options):
        self.consumer = opt.get_conn()
        self.number = opt.get_number()

    async def setData(self,db):
        for kanban in self.consumer.get_kanban_itr():
            try:
                print(f'received from {SERVICE_NAME}')
                print('data:',kanban.get_metadata())

                # dbに書き込み
                db.addDb(kanban.get_metadata())
                print(kanban.get_metadata())

            except Exception:
                print(Exception)
                self.consumer.output_kanban(
                    process_number = self.number,
                    connection_key = "response",
                    result = False,
                    metadata = {
                        "microservice": SERVICE_NAME
                    }
                )

async def main(opt: Options):
    db = MongoDb()
    if MODE == "rabbitmq":
        engine = RabbitMq()
    elif MODE == "kanban":
        engine = Kanban()
    else:
        print("Error: MODE setting is incorrect. MODE There are two MODEs, 'rabbitmq' and 'kanban'",
            file=sys.stderr)
        return

    await engine.init(opt)
    await engine.setData(db)


# @main_decorator は aion-statuskan と接続・マイクロサービスが正常に立ち上がったことを通知する
@main_decorator(SERVICE_NAME, WITH_KANBAN)
def main_wrapper(opt: Options):
    asyncio.run(main(opt))

if __name__ == "__main__":
    main_wrapper()
