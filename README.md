# Photom-Web
画像管理と家電操作を目的とした簡易ローカル Web アプリケーション。

## 開発環境
### ハード
- RaspberryPi Zero WH
- [RPZ-IR-Sensor Rev.2.0](https://www.indoorcorgielec.com/products/rpz-ir-sensor/)

### OS
- Raspberry Pi OS Lite
  - Release date: May 7th 2021
  - Kernel version: 5.10

### ソフト
- Docker
- Python 3.7.3（Docker image）

### ライブラリ

| 名前 | 用途 |
|:----|:----|
| docopt | RPZ-IR-Sensor 依存 |
| flask | Webアプリフレームワーク |
| flask-marshmallow | ORM |
| flask_sqlalchemy | ORM |
| marshmallow | ORM |
| marshmallow-sqlalchemy | ORM |
| smbus | RPZ-IR-Sensor 依存 |
| Pillow | 画像処理 |
| requests | 通信 |

requirements.txt 参照

## 初期設定
1. プロジェクト直下に private_config.py というファイルを作成
2. 以下の内容を追加し、値をそれぞれ設定

```python
OPEN_WEATHER_API_KEY = 'ここに OpenWeather API Key を入力'
SWITCH_BOT_TOKEN = 'ここに Switch bot Token を入力'
SECRET_KEY = '任意文字列'
```

## 起動方法
```
# cd photom-web
# docker-compose up
```

## 注意事項
main ブランチでは RaspberryPi ではなく、PC 上での動作を目的としています。RaspberryPi での動作は raspberrypi_zero ブランチで確認できます。アプリ上で RPZ-IR-Sensor から各種センサーの値を表示している箇所がありますが、main ブランチの方ではモックで起動します。

## スクリーンショット
<img src="screenshot/screenshot1.png" width="500">
<img src="screenshot/screenshot2.png" width="500">
<img src="screenshot/screenshot3.png" width="500">
<img src="screenshot/screenshot4.png" width="500">
<img src="screenshot/screenshot5.png" width="500">
