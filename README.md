# Earthquake-SensorBox
#### 模擬情境:
利用 Raspberry Pi 連接三軸感測器(ADXL345)即時測出地震發生時當下區域的三軸偏移量，並帶入 Random Forest 機器學習預測出震級，將震級結果透過 NRF24L01 進行一對多的無線傳輸，以此控制連接於電器上的繼電器，實現分級控制，依據地震的震級關閉相應的電器，最後利用 MQTT 通知使用者，當下震級與關閉了什麼電器。
> 以下為成果圖:
![image](https://github.com/ChuJacky0327/Earthquake-SensorBox/blob/main/image/SensorBox.png)


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
1. Raspberry-ADXL345 接線 :
![image](https://github.com/ChuJacky0327/Earthake-SensorBox/blob/main/image/ADXL345.png)
> 參考來源 : [https://www.labno3.com/2021/03/20/raspberry-pi-accelerometer-using-the-adxl345/](https://www.labno3.com/2021/03/20/raspberry-pi-accelerometer-using-the-adxl345/)  
2. Arduino 與繼電器連接 :
![image](https://github.com/ChuJacky0327/Earthake-SensorBox/blob/main/image/%E7%B9%BC%E9%9B%BB%E5%99%A8%E6%8E%A5%E7%B7%9A.jpg)
> 參考來源 : [https://tutorials.webduino.io/zh-tw/docs/useful/example/smart-socket.html](https://tutorials.webduino.io/zh-tw/docs/useful/example/smart-socket.html)  
3. Arduino 與 NRF24L01 接線 :
![image](https://github.com/ChuJacky0327/Earthake-SensorBox/blob/main/image/NRF24L01%E6%8E%A5%E7%B7%9A.jpg)
> 參考來源 : [https://micro.rohm.com/tw/deviceplus/inspire/interviews/nrf24l01-rf-module-tutorial-1/](https://micro.rohm.com/tw/deviceplus/inspire/interviews/nrf24l01-rf-module-tutorial-1/)
***
## Step3. Raspberry Pi-ADXL345 Data Collect
此步驟為三軸感測器資料收集的程式，若有要於地震屋或現實環境收集地震的數據，可用此程式，若不需可跳過此步驟  
收集資料前要先針對三軸感測器進行校正，因此會有兩種收集方式 : 
### 1. 每次都扣掉初始位置進行校正 :
#### 傳送端 :
```shell
$ cd /ADXL345_collect
$ python3 adxl345_collect.py
```
#### 接收端 : (可由另外的電腦執行，達到遠端接收資料，會寫成 csv 檔)
```shell
$ cd /ADXL345_collect/adxl345data_original
$ python3 adxl345data_originalSub.py
```
### 2. 每次都扣掉上一筆資料的位置進行校正 :
#### 傳送端 :
```shell
$ cd /ADXL345_collect
$ python3 adxl345_collect.py
```
#### 接收端 : (可由另外的電腦執行，達到遠端接收資料，會寫成 csv 檔)
```shell
$ cd /ADXL345_collect/adxl345data_last
$ python3 adxl345data_lastSub.py
```
***
## Step4. Arduino 燒錄 NRF24L01 code
* Raspberry Pi 端的 Arduino 燒錄 NRF24L01_Sender_1007 的 code
* 繼電器端 Arduino 燒錄 NRF24L01_Receive_1007 的 code
***
## Step5. Random Forest ML training
訓練的 csv 檔為地震屋所收集的數據 (pig_earthquake.csv)，並利用 Random Forest 機器學習進行模型的訓練
```shell
$ python3 RandomForest_predict.py
```
> 運行此程式後，會產生出一個 model 檔及訓練的收斂圖
***
## Step6. DEMO
### 使用最大地動加速度值 (PGA) 算法計算震級，並利用 MQTT 通知
```shell
$ python3 adxl345_NRF24L01_mqtt.py
```
### 使用機器學習 Random Forest 算法計算震級，並利用 MQTT 通知
```shell
$ python3 RF_adxl345_final.py 
```
***
運行```python3 RF_adxl345_final.py```後，當有地震發生時會依據當下三軸感測器的值，進行 Random Forest 模型的預測，並隨即利用 NRF24L01 進行無線傳輸，即時的依據震度關閉家電，並利用 MQTT 通知使用者

本專案投稿至 2022智慧物聯網產學研討會  

