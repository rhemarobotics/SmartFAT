# 6.4. 使用Node-RED Modbus

Owner: 耿良 王
Tags: tutorial documents
Date: April 2, 2024

<aside>
💡 Node-RED 是一款適合物聯網和工業自動化的圖形化開發工具。通過 node-red-contrib-modbus 節點包，Node-RED 可以輕鬆實現與 Modbus 設備的數據交換。本文將介紹如何在 Node-RED 中設置 Modbus 通訊，包括基本配置、數據讀寫以及數據監控，以便用戶能夠快速建立有效的 Modbus 通訊流程。

</aside>

# 壹、認識Modbus原理與通訊協定

- 請參閱章節 [**5.2 物聯網網路層 - MODBUS**](../5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/../network/modbus.md)

# 貳、安裝與設置Modbus

## **1. 安裝 Modbus 節點包**

在 Node-RED 的管理面板中選擇 Manage Palette，搜索並安裝 **node-red-contrib-modbus** 節點包，這會添加 Modbus 節點（包括 Modbus Read、Modbus Write 等）到 Node-RED 中。

![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image.png)

![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%201.png)

## **2. 配置 Modbus 節點**

- 選擇 Modbus 協議：
根據使用的協議選擇 Modbus TCP（以太網）或 Modbus RTU（串口）模式。
- 設置 Modbus 通訊參數：
在節點配置中設置設備的 IP 地址和端口（TCP）或串口參數（RTU），以及 Modbus ID、通訊速率等。

## **3.  建立 Modbus 讀取流程**

- 添加 Modbus Read 節點：
在工作區中添加 Modbus Read 節點，設置讀取的參數，如開始地址、數據長度和頻率。
- 週期性讀取：
可以設置讀取的頻率，定期獲取數據，以便實時監控設備狀態。

## **4. 建立 Modbus 寫入流程**

- 添加 Modbus Write 節點：
在工作區中添加 Modbus Write 節點，設置寫入的目標地址和數據值。
- 注入數據：
使用 Inject 節點或 Function 節點生成寫入數據，並將其連接到 Modbus Write 節點以進行寫入操作。

# 叁、Modbus應用範例實作

此範例是透過 Node-RED 實現 Modbus TCP 功能，可以使用以下四個節點來設置並模擬 Modbus 通信：Modbus Server、Modbus Flex Write、Modbus Flex Getter 和 Modbus Response。以下是具體步驟：

## 1. 建立Modbus Server連線

- 首先建立一個 Modbus Server 節點，設定一個 TCP 伺服器。
- 配置伺服器的 IP 地址、端口（10502）和 Modbus 寄存器範圍等。
- 部署伺服器後，Modbus Server 節點會等待來自其他節點的請求。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%202.png)
    

## 2. 建立Modbus Flex Write節點

- 建立一Modbus Flex Write節點，用來寫入 Modbus 寄存器值。
- 在 Modbus Flex Write 節點的配置中，選擇 Modbus Server 作為目標伺服器。
    - Server的值設成本機位址加埠口號碼『modbus-tcp@localhost:10502』
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%203.png)
    

## 3. 建立Exec 和 Function Node

- 為了實現讀取智慧型機器人各伺服馬達的脈波位置，內部溫度及內部電壓值，我們先建立一個Exec節點，透過執行『[ReadServoStatus.py](http://readservostatus.py/)』此程式，得到各伺服馬達的內部參數，如下圖所示。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%204.png)
    
- 加入一Function節點，針對程式所傳的資訊，轉換成Modbus的數據格式，設定如下圖所示。
    
    <aside>
    💡
    
    msg.payload數據格式定義：
    ‘fc’ : Modbus定義的功能碼(詳見Modbus手冊)
    FC 1: Read Coil Status
    FC 2: Read Input Status
    FC 3: Read Holding Registers
    FC 4: Read Input Registers
    FC 16: Write Multiple Holding Registers on Modbus
    ‘unitid’ : 硬體I/O的位置
    ‘address’ : 寄存器(Register)的位置
    ‘quantity’ : 待寫入參數值數目
    
    </aside>
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%205.png)
    
- 最後，再把新增的這幾個節點串接起來至Modbus Flex Write節點，即完成對Modbus Server寫入參數的設定。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%206.png)
    

## 4. 建立Modbus Flex Getter和Modbus Response節點

- 建立Modbus Flex Read節點，用於從伺服器讀取 Modbus 寄存器值。
    - Server的值設成本機位址加埠口號碼『modbus-tcp@localhost:10502』
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%207.png)
    

## 5. 建立Function節點

- 設計Modbus數據格式，給Modbus Flex Read節點使用。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%208.png)
    

## 6. 建立Modbus Response節點

- 建立Modbus Response節點，用於接收並處理來自伺服器的讀取或寫入結果。
- 在 Debug 面板中查看結果，確認通信是否成功以及數據是否正確。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%209.png)
    
- 結果顯示。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%2010.png)
    

## 7. 完整範例

- 把以上這些建立好的節點依序串接一起，即可完成對Modbus Server讀取和寫入資訊的設定。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%2011.png)
    

# 肆、**部署和測試**

1. 總結，我們的流程已經設計完成，接下來可以進行部署了。只需點擊螢幕右上角的紅色部署按鈕，頂部會彈出一條訊息，提示「**已成功部署**」。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%204%20%E4%BD%BF%E7%94%A8Node-RED%20Modbus/image%2012.png)