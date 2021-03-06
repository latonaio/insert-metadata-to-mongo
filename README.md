# insert-metadata-to-mongo  
insert-metadata-to-mongo は、RabbitMQ、またはkanbanから受け取ったデータをmongoに書き込みます。

## 利用方法
必要なパッケージのインストールを行います。
```
pip install -r requirements.txt
```

## 環境設定
kubenetesやaionを立ち上げる際に必要なservices.ymlに環境変数を設定します。

- MODE: rabbitmqとkanbanの二つのモードを指定することができます。データを受け取る際にどちらから受け取るかによって設定を変更してください。
- MONGO_CLIENT: データ吐き出し先であるMongoDBのホストとポートを指定してください。
- DB_NAME: データ吐き出し先のDBの名前を指定してください。
- RABBITMQ_CLIENT: rabbitMQのホストとポートを指定してください。
- SERVICE_NAME: aionのkanbanから受け取るサービス名を指定してください。
- RABBITMQ_QUEUE_NAME = rabbitMQから受け取るキューの名前を指定してください。 

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