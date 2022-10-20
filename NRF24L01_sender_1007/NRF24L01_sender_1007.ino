#include <SPI.h>;
#include "RF24.h"
String str;
RF24 rf24(7, 8); // CE腳, CSN腳

 
const byte addr[] = "1Node";
const char msg2[] = "off2";
const char msg3[] = "off4";
const char msg4[] = "off6";

 
void setup() {
  Serial.begin(9600);
  rf24.begin();
  rf24.setChannel(83);       // 設定頻道編號
  rf24.openWritingPipe(addr); // 設定通道位址
  rf24.setPALevel(RF24_PA_MIN);   // 設定廣播功率
  rf24.setDataRate(RF24_250KBPS); // 設定傳輸速率
  rf24.stopListening();       // 停止偵聽；設定成發射模式
}
 
void loop() {
  if (Serial.available()){
    str = Serial.readStringUntil('\n');
    if (str == "earthquake2"){
      rf24.write(&msg2, sizeof(msg2));  // 傳送資料
      delay(1000);
    }
    else if (str == "earthquake4"){
      //rf24.write(&msg2, sizeof(msg2));  // 傳送資料
      rf24.write(&msg3, sizeof(msg3));  // 傳送資料
      Serial.println("nRF24L01 ready!");
      delay(1000);
    }
    else if (str == "earthquake6"){
      //rf24.write(&msg2, sizeof(msg2));  // 傳送資料
      rf24.write(&msg4, sizeof(msg4));  // 傳送資料
      delay(1000);
    }

    
  }

}
