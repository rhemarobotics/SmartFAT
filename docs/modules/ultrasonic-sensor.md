# 4.6. 超音波感測器實習

Owner: 耿良 王
Tags: tutorial documents
Date: March 15, 2024

# **壹、實習前準備**

<aside>
💡 物聯網感知層實務技術，本章節介紹智慧工廠教學實驗平台各感測器的功能原理與程式開發，透過實作練習，不僅能學習到感測器的基礎知識，也能了解如何將它們應用在物聯網的感知層，幫助同學深入地掌握智慧工廠相關技術，為未來的學習打下良好基礎。

</aside>

## 一、智慧工廠感測器元件

- 智慧工廠教學實驗平台提供豐富的感測器元件，可分為三大類，環境監控、感測/控制、燈號/數據顯示元件，共計16種，如下圖。
    
    ![](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image9.png)
    

## 二、連線至智慧工廠

- 請參考 🚩[**3.實驗平台開發環境**](../development/setup.md) 設置好本地端電腦與智慧工廠端之間的連線，透過VNC連線至智慧工廠，打開Arduino IDE並載入範例程式。

# **貳、超音波感測器**

<aside>
💡

超音波感測器（Ultrasonic Sensor）是一種利用**超音波**來檢測物體距離或移動的感測裝置，廣泛應用於許多領域。超音波感測器由於其可靠性和高精度，已廣泛應用於各種領域，特別是在需要精確距離測量和自動化控制的場景中。

- 高靈敏度：能夠精確測量距離，對於透明或反光物體的偵測效果也很好。
- 非接觸測量：不需要與物體直接接觸，因此不會對物體或感測器本身造成磨損。
- 適應各種環境：適用於各種光照條件下運作，不受灰塵、煙霧或霧氣的影響。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%206%20%E8%B6%85%E9%9F%B3%E6%B3%A2%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解超音波感測器的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- 超音波感測器
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%206%20%E8%B6%85%E9%9F%B3%E6%B3%A2%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    
    超音波感測器的工作原理基於超音波的反射。感測器發射超音波信號（通常頻率在20kHz到200kHz之間）到物體，然後接收從物體反射回來的聲波。透過計算超音波從發射到接收的時間，感測器能夠判斷物體的距離。
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%206%20%E8%B6%85%E9%9F%B3%E6%B3%A2%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%202.png)
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%206%20%E8%B6%85%E9%9F%B3%E6%B3%A2%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%203.png)
    
- 元件內部電路圖

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%206%20%E8%B6%85%E9%9F%B3%E6%B3%A2%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%204.png)

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/UltraSonicSensor/UltraSonicSensor.ino 檔案。
- 放置一物件於感測器前，並任意前後移動。

## 四、範例程式

```arduino
/*****************************************************
 * UltraSonicSensor.ino 
 * 目的:
 *  測試超音波感測器功能
 * 方法:
 *  超音波感測器
 * 步驟:
 *  放置一物件於感測器前,並任意前後移動
 * 結果:
 *  觀察序列埠監看視窗,顯示距離的變化
*****************************************************/

#define UR_TRIG_PIN   8 //定義超音波感測器發射腳位連接至8腳
#define UR_REV_PIN    9 //定義超音波感測器接收腳位連接至9腳

/************************* 初始設定 *********************/
void setup()
{
  Serial.begin(9600);
  
  pinMode(UR_TRIG_PIN, OUTPUT); //設定UR_TRIG_PIN為輸出接腳
  pinMode(UR_REV_PIN, INPUT);   //設定UR_REV_PIN 為輸入接腳
}

/************************* 主程式 ***********************/
void loop()
{
    int dis = CalculateDistUR(); //超音波距離計算函數
    Serial.println (dis);        //序列埠輸出偵測到的距離
    delay(1000);
}

/*********** 超音波距離計算函數(mm) ***********************/
int CalculateDistUR()
{
  long duration;
  
  digitalWrite(UR_TRIG_PIN, LOW);
  delayMicroseconds(5);
  digitalWrite(UR_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(UR_TRIG_PIN, LOW);
  
  duration = pulseIn(UR_REV_PIN, HIGH);
  
  return (duration/2) / 2.91;
}
```

## 四、實習結果

- 觀察序列埠監看視窗，顯示距離的變化。