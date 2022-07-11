/*****************************************************
 * GasSensor.ino 
 * 目的:
 *  測試氣體感測器偵測功能(主要是甲烷)
 * 方法:
 *  氣體感測器 + 蜂鳴器
 * 步驟:
 *  可用打火機輸出瓦斯(甲烷)至感測器測試
 * 結果:
 * 1. 觀察氣體感測器上的LED是否亮起
 * 2. 當偵測到瓦斯氣體濃度過高時,蜂鳴器會發出警報聲
*****************************************************/

#define MQ4AnalogPin  A4    //定義氣體感測器接腳
#define BuzzerPin     36    //定義無源蜂鳴器接腳

const int R_0 = 945;        //自訂義RO測量值

/************************* 初始設定 *********************/
void setup() 
{
  Serial.begin(9600);
  
  pinMode(MQ4AnalogPin, INPUT); //設置氣體感測器接腳為輸入
  pinMode(BuzzerPin,    OUTPUT);//设置無源蜂鳴器接腳為輸出
}

/************************* 主程式 ***********************/
void loop() 
{
  float mq4ppm = getMethanePPM(); //計算甲烷濃度PPM值
  Serial.println(mq4ppm);         //序列埠輸出甲烷濃度PPM值
  
  //判斷氣體感測器濃度，若大於1000ppm，則蜂鳴器發出警報聲
  if (mq4ppm > 1000) 
  {
    //蜂鳴器音頻由低到高 200HZ ~ 800HZ  
    for(int i = 200; i <= 800; i++)  
    {  
        tone(BuzzerPin, i);
    }  
    
    delay(1000); //延遲1秒 

    //蜂鳴器音頻由高到低 800HZ ~ 200HZ
    for(int i= 800; i >= 200; i--) 
    {  
        tone(BuzzerPin, i);  
        delay(10);  
    }  
  }
  else
  {
    noTone(BuzzerPin); //關閉蜂鳴器
    delay(10);
  }
}

/*********** 計算甲烷濃度PPM值 **************************/
float getMethanePPM()
{
   float a0 = analogRead(MQ4AnalogPin);
   float v_o = a0 * 5 / 1023;
   float R_S = (5-v_o) * 1000 / v_o;
   float PPM = pow(R_S/R_0,-2.95) * 1000;
   delay(100);
   return PPM;
}
