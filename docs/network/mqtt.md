# 5.1 物聯網網路層 - MQTT

Owner: 耿良 王
Tags: tutorial documents
Date: May 1, 2024

# 工業物聯網MQTT通訊協定

## 一、認識MQTT

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image.png)

MQTT（Message Queuing Telemetry Transport）訊息序列遙測傳輸，是一種基於發佈/訂閱（publish/subscribe）模式的"羽量級"通訊協定，該協定構建於TCP/IP協定上，作為一種**低開銷、低頻寬**佔用的即時通訊協定，使其在**物聯網、小型設備、移動應用**等方面有較廣泛的應用。

- 1999年 IBM發明
- 2014年MQTT 3.1 正式變成開放的 OASIS 國際標準
- 2019年MQTT 5.0 正式變成開放的 OASIS 國際標準
- MQTT 3.1規範—>MQTT 3.1.1規範—>MQTT 5規範

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image%201.png)

## 二、MQTT訊息傳遞原理

MQTT使用發佈(Publish) / 訂閱(Subscribe)的消息傳遞機制，主要由四種元件構成。

- 發佈者 (Publisher)
- 訂閱者 (Subscriber)
- 主題 (Topic)
- 轉訊站 (Broker)
    
    <aside>
    💡 範例 : 溫度感測器(Publisher)，發布一特定主題(Topic，例如溫度值)至代理人(Broker)。發布後，手機用戶或電腦端使用者(Subscriber)，可以訂閱此主題，然後從代理人那邊接收訊息(溫度值)。
    
    ![Untitled](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/Untitled.png)
    
    </aside>
    

## 三、MQTT的訊息格式

MQTT訊息格式組成架構

- Fix Header (固定格式封包)
- Variable Header (變動格式封包，存放”主題”值)
- Payload (訊息內文，存放”數據”值)

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image%202.png)

## 四、MQTT 傳輸品質(QoS)

MQTT 定義了三個層級的傳輸品質設定(Quality of Service)，QoS 等級從低到高，不僅意味著消息可靠性的提升，也意味著傳輸複雜程度的提升

- QoS0 (只發一次)，可能丟失消息。
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image%203.png)
    
- QoS1 (重發一次)，保證收到消息，但消息可能重複。
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image%204.png)
    
- QoS2 (保證一次)，保證消息既不丟失也不重複。
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%201%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MQTT/image%205.png)
    

## 五、MQTT優點

MQTT與HTTP是兩種不同的通訊協定，用於在不同的場景下進行數據交換和通訊。以下是它們的比較 : 

1. 數據量和協議頭部(Header)：
    - MQTT是一個**輕量級的協議**，協議頭部較小，佔用較少的數據，這對於資源受限的設備和低頻寬環境非常有利。
    - HTTP的協議頭部相對較大，每次通訊都需要攜帶完整的頭部信息，大量數據傳輸不利低頻寬的網路環境。
2. 通訊方式：
    - MQTT基於**發布/訂閱（Publish/Subscribe）模式**，只有訂閱相應主題的設備才會收到消息，**減少了不必要的通訊流量**。
    - HTTP是請求-響應（Request-Response）模式，每次通訊都需要客戶端主動發送請求，伺服器才能返回響應，會增加通訊延遲。
3. 長連接和狀態管理：
    - MQTT**支援長連接**，即客戶端和伺服器之間的連接在一段時間內保持打開狀態，這有助於減少建立和斷開連接的開銷，同時節省網路帶寬。
    - HTTP通常是無狀態協議，每次請求和響應都是獨立的，需要在每次通訊中重新建立連接，這可能會增加效能開銷。
4. 頻寬和效能：
    - 由於MQTT的輕量級特性和有效的通訊模式，它在資源受限的設備和網路環境中表現出色，尤其是在大量設備之間需要快速、低延遲通訊的情況下。
    - HTTP在一般互聯網應用中表現良好，但在**資源受限的嵌入式設備或低頻寬要求的物聯網應用中不如MQTT**。