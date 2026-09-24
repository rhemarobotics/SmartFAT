# 6.2. 使用Node-RED Dashboard

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

<aside>
💡 數據可視化是將數據轉換為圖表、地圖等視覺形式，以便更清楚地理解其中的意義。由於觀察單純的數字或統計數據難以快速得出清晰結論，而人類大腦對視覺信息的處理遠勝於文字，所以透過使用圖表、圖形和設計元素進行數據可視化，可以更直觀地解析數據模式、趨勢、統計規律及其關聯性，幫助發現其他方式難以察覺的細節。

![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image.png)

</aside>

Node-RED Dashboard 有直觀界面和高彈性的組件，使其成為物聯網系統或智慧工廠中常用的工具之一，幫助使用者快速實現數據的視覺化展示與管理。主要功能和用途 : 

- 即時數據展示：從傳感器、API、資料庫等來源獲取數據，並即時顯示。
- 多種視覺化元件：提供圖表、儀表、表單、開關、按鈕等多種元件，便於設計視覺化界面。
- 數據分析：透過折線圖或條形圖等圖表監控趨勢，利於分析數據變化。
- 互動控制：可以加入開關、滑塊等元件，實現即時數據的調整和控制。
- 遠端監控與管理：Dashboard 是基於網頁的，使用者可以在任何設備上遠程訪問，便於對設備進行遠程監控。

# 智慧工廠大數據可視化實習

## 一、實習目標：

- 學習如何在 Dashboard 上顯示動態更新的數據（例如溫濕度數據），並加入用戶控制元件（如按鈕和開關），使使用者可以即時互動並控制連接設備。

## 二、實驗步驟：

### 1. 必須先完成 [**6. 物聯網應用層 - 使用Node-RED**](first-node-red.md) 的實習

- 透過此結果，把數據可視化。

### 2. Node-RED Dashboard(raspberry端)

Node-RED Dashboard 是一個用於**數據視覺化**和**監控界面**的擴展套件，它讓開發者可以快速建立圖形化的儀表板，以即時顯示物聯網（IoT）裝置或其他數據來源的數據。這個視覺化工具能夠輕鬆將資料以圖表、儀表、數字顯示等多種格式展示在網頁上，並且提供豐富的互動功能。

1. Node-RED 安裝『node-red-dashboard』功能節點和『node-red-contrib-ui-artless-gauge』。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image20.png)
    
2. Node-RED Dashboard提供以下的功能節點，用以快速創建數據儀表板。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image4.png)
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image21.png)
    
3. 分別建立八個artless gauge節點與二個chart節點。
    - 編輯artless gauge節點 : DHT-Temp
        
        ![2024-03-14-071950_441x845_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-071950_441x845_scrot.png)
        
    - 編輯artless gauge節點 : DHT-Humid
        
        ![2024-03-14-072024_438x848_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072024_438x848_scrot.png)
        
    - 編輯artless gauge節點 : Light
        
        ![2024-03-14-072041_441x852_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072041_441x852_scrot.png)
        
    - 編輯artless gauge節點 : FlameSensor
        
        ![2024-03-14-072058_440x843_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072058_440x843_scrot.png)
        
    - 編輯artless gauge節點 : Mq4Sensor
        
        ![2024-03-14-072114_438x854_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072114_438x854_scrot.png)
        
    - 編輯artless gauge節點 : emgbtn
        
        ![2024-03-14-072133_438x842_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072133_438x842_scrot.png)
        
    - 編輯artless gauge節點 : knob
        
        ![2024-03-14-072148_440x843_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072148_440x843_scrot.png)
        
    - 編輯artless gauge節點 : irdetect
        
        ![2024-03-14-072205_437x839_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072205_437x839_scrot.png)
        
    - 編輯chart節點 : DHT-Temp範例
        
        ![2024-03-14-072229_449x690_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072229_449x690_scrot.png)
        
    - 編輯chart節點 : DHT-Humid範例
        
        ![2024-03-14-072244_448x693_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-072244_448x693_scrot.png)
        
4. 新建一個『function』節點並命名為『Split Data』，把數據字串分配到對應的感測器，之後可以在 Dashboard 顯示元件。
    
    ```jsx
    var msgTemp  = {payload: msg.payload.Temp};
    var msgHumid = {payload: msg.payload.Humid};
    var msgLight = {payload: msg.payload.Light};
    var msgFlame = {payload: msg.payload.Flame};
    var msgMq4   = {payload: msg.payload.Mq4};
    var msgBtn   = {payload: msg.payload.Btn};
    var msgOhm   = {payload: msg.payload.Ohm};
    var msgIrdet = {payload: msg.payload.Irdet};
    var msgTim   = {payload: msg.payload.Time};
    
    //set the values as the global variables
    global.set("TEMP_GL",     msg.payload.Temp);  // 設置溫度全域變數
    global.set("HUMID_GL",    msg.payload.Humid); // 設置濕度全域變數
    global.set("LUX_GL",      msg.payload.Light); // 設置亮度全域變數
    global.set("IRDETECT_GL", msg.payload.Irdet); // 設置物件全域變數
    
    return [msgTemp, msgHumid, msgLight, msgFlame, msgMq4, msgBtn, msgOhm, msgIrdet, msgTim];
    ```
    
5. 把設定好的這些節點，連接起來。
    
    ![2024-03-14-071900_1342x475_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/2024-03-14-071900_1342x475_scrot.png)
    
6. 部署Node-RED訂閱/發布程式，點選右上角的【部署】按鈕，即可完成Dashboard儀表板顯示。
7. 透過以下URL，訪問設計好的Dashboard介面。
    
    > [http://localhost:1880/ui](http://localhost:1880/ui%EF%BC%8C%E8%A8%AA%E5%95%8F%E8%A8%AD%E8%A8%88%E5%A5%BD%E7%9A%84Dashboard%E4%BB%8B%E9%9D%A2%E3%80%82)
    > 

## 三、實驗結果

- 在瀏覽器端輸入網址 http://localhost:1880/ui，觀看大數據可視化的顯示效果，儀表板上的各元件分別對應到不同的感測器，例如 : 透過手電筒打光進入光敏感測器，看看工廠照明度的值是否急速增加。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image10.png)
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image19.png)
    
- 例如 : 當按下智慧工廠的按鈕開關模組，儀表板上的緊急開關由0變1，外圈也變為紅色，代表緊急開關被按下。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%202%20%E4%BD%BF%E7%94%A8Node-RED%20Dashboard/image22.png)