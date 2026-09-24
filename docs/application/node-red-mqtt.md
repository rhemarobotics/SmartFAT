# 6.3. 使用Node-RED MQTT

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

<aside>
📢 還記得在上一篇"智慧工廠教學實驗平台系列(三)：工業物聯網應用層實務技術 - 使用Node-Red-Dashboard"，實作了一個Node-Red-Dashboard，用以顯示智慧工廠裡面多感測器的即時數據。如果想要把此數據傳輸至多個使用者端(可能是10台，甚至是100台以上的電腦或是手機用戶端)，該怎麼做呢? 本篇將繼續透過上一篇的範例程式，說明物聯網常用的MQTT通訊協定及應用層的相關實務應用技術。

</aside>

# 壹、認識MQTT原理與通訊協定

- 請參閱章節 [**5.1 物聯網網路層 - MQTT**](../5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/../network/mqtt.md)

# 貳、安裝與設置MQTT Broker(智慧工廠端)

## 2.1 Mosquitto介紹

- Eclipse Mosquitto是一個開源的**輕量級MQTT消息代理(Broker)**，實現 **MQTT 協議版本 5.0、3.1.1 和 3.1**，提供可靠的消息傳遞，並允許裝置間的高效通信，適用於低功耗單板電腦(SBC)與大型服務器(Server)等所有設備。
- Mosquitto易於配置和部署，適用於多種平台(Linux、Windowns)，並提供豐富的功能，使其成為連接物聯網設備的理想選擇。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled.png)
    
    > 開源專案[GitHub連結](https://github.com/eclipse/mosquitto) :
    > 

## 2.2 Mosquitto安裝

- 於Mosquitto官網[下載連結](https://mosquitto.org/download/)，並根據本地端的電腦選擇系統，選擇對應的系統，下載程式並一鍵安裝。
- 在樹莓派的 Shell 裡，我們可以使用 apt 指令直接安裝 mosquitto 套件和 mosquitto-clients 套件，方便之後的功能測試。
    
    ```bash
    sudo apt update
    sudo apt upgrade
    apt-get install mosquitto mosquitto-clients
    ```
    
- 安裝完成後，輸入下列指令，檢查一下目前 mosquitto 安裝版本。
    
    ```bash
    mosquitto -v
    ```
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/image.png)
    

## 2.3 Mosquitto啟動

- 安裝完成後，mosquitto服務會自動啟動，可以使用service指令確認mosquitto目前運行狀態。
    
    ```bash
    service mosquitto status
    ```
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/image%201.png)
    

# 叁、安裝MQTT Subscriber(本地電腦端)

## MQTT X介紹與下載

- 電腦端MQTT訂閱者，我們使用MQTT X，它是EMQ開源的一款的跨平臺MQTT5.0桌面用戶端，支援macOS, Linux, Windows。
- MQTT X的UI採用了聊天介面形式，簡化了頁面操作邏輯，使用者可以快速創建連接，允許保存多個用戶端，方便用戶快速測試MQTT/MQTTS連接，及MQTT消息的訂閱和發佈。

![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%201.png)

> 下載網址如下：[https://mqttx.app/](https://mqttx.app/)
> 

# 肆、MQTT應用範例實作

此範例程式將示範如何建立MQTT通訊協定的物聯網程式，將Node-RED、Mosquitto和MQTT X作一完整的系統整合，讓您更深入了解物聯網技術的實際應用方式和優勢。

1. 智慧工廠端，透過Node-RED發布和訂閱MQTT主題，並進行數據可視化分析。
2. MQTT X客戶端，發布和訂閱MQTT主題，與智慧工廠端交換數據。

## 4.1 智慧工廠端 - 發布與訂閱主題

透過Node-RED發布主題(感測器數據)並進行數據可視化分析，並訂閱來自MQTT X客戶端的燈號主題。將透過下列步驟，依序說明實作內容。

### 4.1.1 Node-RED程式開發

- 打開瀏覽器頁面並輸入 : **127.0.0.1:1880**，進入Node_RED編輯頁面。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%202.png)
    
- 從**network工具欄**中，拖拉一個mqtt in和九個mqtt out節點，進入程式流程編輯區。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%203.png)
    
- 編輯**mqtt in節點**，點選「服務端」欄位右邊的鉛筆，編輯「mqtt-broker」節點，服務端內容改成【node-red@localhost】或是智慧工廠IP位址，埠內容改成【1883】，Protocol內容改成【MQTT V3.1.1】，如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%204.png)
    
- 修改完成後，服務端變成【node-red@localhost:1883】或是智慧工廠IP位址，主題改成【outTopic】，QoS改成【2】，名稱改成mqtt in，結果如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%205.png)
    
- 拖拉並編輯一個「text」節點，Label內容改成【接收到的字串】，Value format內容改成【{{msg.payload}}】，結果如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%206.png)
    
- 拖拉並編輯「button」節點，Label內容改成【LED_ON】，Payload內容改成【1】，結果如圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%207.png)
    
- 拖拉並編輯第二個「button」節點，Label內容改成【LED_OFF】，Payload內容改成【0】，Color內容改成【black】，結果如圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%208.png)
    
- 編輯第一個「mqtt out」節點，服務端內容改成【node-red@localhost:1883】或是智慧工廠IP位址，主題內容改成【inTopic/Led】，名稱內容改成【mqtt_Led】。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%209.png)
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2010.png)
    
- 依序編輯其餘八個「**mqtt out**」節點，主題內容改成【inTopic/Temp】、【inTopic/Humid】、【inTopic/Light】、【inTopic/Flame】、【inTopic/Mq4】、【inTopic/Btn】、【inTopic/Knob】及【inTopic/Ird】。
- 透過前面的步驟，已經完成所有節點的內容修正。現在只需把修改過後的節點，正確的相連在一起即可，結果如圖所示。點選右上角的「部署」按鈕，即可完成MQTT通訊協定的連線。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2011.png)
    
- 部署成功後，mqtt in節點下方出現綠色燈號，代表MQTT設定成功。若mqtt in節點沒有出現【**已連接】**，請再次檢查樹莓派網路通訊是否正常，網路設定或是mqtt broker網路設定是否正確。

### 4.1.2 Node-RED程式測試

打開瀏覽器並輸入 [http://127.0.0.1:1880/ui/](http://127.0.0.1:1880/ui/)，觀察Node-RED Dashboard上感測器數值的變化。

![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2012.png)

### 4.1.3 Node-RED程式備份

以下是一般情況下如何進行Node-RED工作流程的備份的步驟：在Node-RED中，程式是以工作流程（flows）的形式存在的。要備份工作流程，請按照以下步驟進行：

- 在Node-RED編輯器中，點擊右上角的選單圖示（三條橫線）。
- 選擇 "Export"（匯出）選項。
- 選擇要匯出的工作流程，您可以選擇全部工作流程或僅選擇特定的工作流程。
- 點擊 "Download"（下載）按鈕來保存工作流程的JSON文件。

![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2013.png)

## 4.2 MQTT X客戶端 - 發布與訂閱主題

透過MQTT X建立電腦客戶端與智慧工廠之間的MQTT通訊連線測試。將透過下列步驟，依序說明實作內容。

### 4.2.1 MQTT X連線設置

- 建立快速連接，如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2014.png)
    
- 連接設定，Name欄位【使用者自行設定】，Client ID欄位【系統自動產生】，Host欄位填入【目前智慧工廠的IP位址】，Port欄位填入【1883】，其他設定採預設值即可，結果如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2015.png)
    

### 4.2.2 MQTT X測試

- 當連線至智慧工廠的MQTT Broker成功後，接著設定MQTT X的訂閱主題(Topic)，開始接收來自智慧工廠端的感測器訊息(Message)。訂閱智慧工廠端溫/溼度感測器的溫度值(°C)，開啟一個New Subscription，Topic欄位填入【inTopic/Temp】，QoS欄位填入【2】，Color欄位【選一色彩】，Alias欄位填入【Temp】，設定如下圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2016.png)
    
- MQTT X接收到的數據值。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2017.png)
    
- 依序新增其他訂閱主題(Topic)，當完成相關主題訂閱之後，MQTT X就開始接收從智慧工廠傳來的感測器資訊，結果如下圖所示。透過觀察不同的訂閱主題(分別以不同的顏色表示)，得知感測器目前的數據值。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2018.png)
    
- 測試MQTT X客戶端發布訊息至智慧工廠的MQTT Broker。設定發布主題為【outTopic】，要發送的文字字串為【”Hello Pi”】，按下旁邊的綠色按鈕，發送訊息出去，如圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2019.png)
    
- 智慧工廠端的MQTT Broker接收到文字訊息，將會顯示於Node-RED Dashboard上的【接收到的字串】，結果於圖所示。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2020.png)
    
- 最後，透過智慧工廠端 Node-RED Dashboard上的LED按鈕發布訊息(0/1)至MQTT X客戶端，結果如下圖。
    
    ![Untitled](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%203%20%E4%BD%BF%E7%94%A8Node-RED%20MQTT/Untitled%2021.png)
    

# 伍、結論

這次的分享就到這邊，想要了解更多智慧工廠的內容嗎？歡迎持續追蹤並支持我們唷！