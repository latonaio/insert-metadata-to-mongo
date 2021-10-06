## 概要
insert-metadata-to-mongoはkanban(RabbitMQ)から受け取ったデータをMongoDBに書き込みます。

## 利用方法
必要なパッケージのインストール
```
pip install -r requirements.txt
```

## 環境設定
サービスを立ち上げるためにservices.ymlに環境変数を設定します。

- MODE: rabbitmqとkanbanの二つのモードを指定することができます。データを受け取る際にどちらから受け取るかによって設定を変更してください。
- MONGO_CLIENT: データ吐き出し先であるMongoDBのホストとポートを指定してください。
- DB_NAME: データ吐き出し先のDBの名前を指定してください。
- RABBITMQ_CLIENT: rabbitmqのホストとポートを指定してください。
- SERVICE_NAME: aionのkanbanから受け取るサービス名を指定してください。
- RABBITMQ_QUEUE_NAME = rabbitmqから受け取るキューの名前を指定してください。 

```yml
xxx-service:
    scale: 1
    startup: yes
    always: yes
    network: NodePort
    ports:
      - name: xxx-service
        protocol: TCP
        port: xxxx
        nodePort: xxxxx
    env:
      MODE: rabbitmq
      MONGO_CLIENT: mongodb://${MONGODB_SERVER_HOST}:xxxx/
      DB_NAME: hogehoge
      RABBITMQ_CLIENT: amqp://${name}:${name}@IP_ADDRESS:xxxxxx/
      SERVICE_NAME: AION_SERVICE_NAME
      RABBITMQ_QUEUE_NAME: xxxx
```