# Earthake-SensorBox
#### 模擬情境:
利用 Raspberry Pi 連接三軸感測器(ADXL345)即時測出地震發生時當下區域的三軸偏移量，並帶入 Random Forest 機器學習預測出震級，將震級結果透過 NRF24L01 進行一對多的無線傳輸，以此控制連接於電器上的繼電器，實現分級控制，依據地震的震級關閉相應的電器，最後利用 MQTT 通知使用者，當下震級與關閉了什麼電器。
> 以下為成果圖:

> 物聯網研討會投稿:

***
## Step1. Raspberry Pi Update and install
```shell
$ sudo apt-get update 
$ sudo apt-get upgrade
$ sudo apt-get install python-pip python-dev
$ pip install selenium
$ sudo apt-get install pigpio python-pigpio python3-pigpio
$ sudo apt-get install python3-smbus
$ sudo apt-get install python-smbus
$ sudo pip3 install selenium
$ pip3 install paho-mqtt python-etcd
$ pip3 install adafruit-blinka
$ pip3 install adafruit-circuitpython-adxl34x
$ pip3 install joblib
$ pip3 install -U scikit-learn
$ pip3 install -U numpy
$ sudo apt install python3-matplotlib
$ sudo apt-get install python3-pandas
```
***
## Step2. Sensor 
* 將 ADXL345 連接上 Raspberry Pi
* Arduino 與繼電器連接，並接上 NRF24L01 (接收端)
* Raspberry Pi 端序列阜接上 Arduino 並連接 (發送端)

***
## Step3. Raspberry Pi-ADXL345 Data Collect
此步驟為三軸感測器資料收集的程式，若有要於地震屋或現實環境收集地震的數據，可用此程式，若不需可跳過此步驟

***
## Step4. Arduino 燒錄 NRF24L01 code
* Raspberry Pi 端的 Arduino 燒錄 NRF24L01_Sender_1007 的 code
* 繼電器端 Arduino 燒錄 NRF24L01_Receive_1007 的 code
***
## Step5. Random Forest ML training
訓練的 csv 檔為地震屋所收集的數據 (pig_earthquake.csv)
