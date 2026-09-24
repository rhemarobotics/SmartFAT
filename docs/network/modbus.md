# 5.2 物聯網網路層 - MODBUS

Owner: 耿良 王
Tags: tutorial documents
Date: May 1, 2024

# 工業物聯網MODBUS通訊協定

## 一、認識Modbus

Modbus 是一種用於工業自動化系統的開放式通訊協定，最初由 Modicon 公司於 1979 年設計，主要用於可編程邏輯控制器（PLC）之間的通訊。它被廣泛應用於工業設備之間的數據傳輸，尤其是在分散式控制系統（DCS）、監控與數據採集系統（SCADA）中。

- 開放性：公開發表並且無著作權要求(無智慧財產權)
- 簡單性：協定框架格式簡單緊湊，易於開發和維護
- 多種傳輸協議(允許設備在不同類型的網路中通訊)
    - Modbus RTU、Modbus ASCII、Modbus TCP/IP
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image.png)
    

## 二、Modbus主從架構模式

Modbus 是一種需求-回應協定，採用主從架構模式。

- 主要裝置會是人機介面 (HMI) 或監控與資料擷取 (SCADA) 系統
- 附屬裝置則是感測器、程式化邏輯控制器 (PLC) 或程式化自動控制器 (PAC)

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image%201.png)

## 三、Modbus傳輸協議

Modbus 主要三種傳輸協議介紹 : 

- **Modbus RTU**（Remote Terminal Unit）是一種基於串行通訊的二進制通訊協定，常用於 RS-232 和 RS-485 這類串行通信介質。數據以緊湊的二進制格式傳輸，效率高，數據量小。
- **Modbus ASCII** 是 Modbus 通訊協定的另一種變體，與 RTU 不同，它以 ASCII 編碼的十六進制格式傳輸數據。
- **Modbus TCP/IP** 是基於以太網的通訊協定，允許 Modbus 協定在 TCP/IP 網絡上傳輸，適用於現代工業網絡和設備連接。

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image%202.png)

## 四、Modbus傳輸封包格式

Modbus 傳輸封包，分為PDU (Protocol Data Unit) 和 ADU (Application Data Unit) 兩個層級的訊息結構，分別處理不同階段的資料封裝與傳輸過程。

- PDU 是 Modbus 訊息的核心部分，它僅包含了功能碼和資料區，與具體的傳輸方式無關。無論是 RTU、ASCII 還是 TCP/IP，PDU 的結構都是相同的。
    - 功能碼 (Function Code): 用於指定操作類型（如讀取、寫入暫存器等）。
    - 數據區 (Data Field): 包含具體的操作參數和數據，如記憶體位址和數據值。
- ADU 是 Modbus 訊息的最外層封裝，包含了 PDU 以及與物理層和傳輸層相關的附加資訊。不同的 Modbus 變體（如 Modbus RTU、Modbus TCP）會在 PDU 的基礎上增加不同的附加資訊來組成 ADU。
    - 裝置位址 (Address Field): 指定 Modbus 網路中的從站設備位址。
    - PDU (Protocol Data Unit): 包含功能碼和數據區。
    - 誤差檢查碼 (Error Check Field): 用於確保數據在傳輸過程中未被損壞（如 CRC 檢查碼）。
- 三種不同的傳輸協議，皆由PDU與ADU組成。
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image%203.png)
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image%204.png)
    

## 五、Modbus Server資料存取配置

Modbus Server（也稱為從站，通常是PLC）的資料存取配置是指如何在設備內部組織和管理數據，以便能夠通過 Modbus 通訊協議進行存取。資料存取主要涉及四種不同的數據類型區塊，它們每個都有各自的地址範圍和功能。以下是常見的 Modbus Server 資料區塊以及其詳細的配置說明：

1. **離散輸入（Discrete Inputs）**
功能：表示只讀的數位量輸入，這些數據通常反映設備的狀態，例如開關的狀態。
地址範圍：從 10001 到 19999（在數據包中通常從 0 開始計數）。
操作：只能讀取，不能寫入。
範例：如果某設備的一個按鈕被按下，該離散輸入區域的對應位元會變為 1，否則為 0。
2. **線圈（Coils）**
功能：表示可讀寫的數位量輸出，可以用來控制設備的狀態，例如啟動或停止馬達。
地址範圍：從 00001 到 09999（在數據包中通常從 0 開始計數）。
操作：可讀取和寫入。
範例：如果 Modbus Master 發送指令來啟動設備，對應的線圈會被設置為 1，表示“啟動”。
3. **輸入暫存器（Input Registers）**
功能：表示只讀的類比量輸入，通常用於讀取感測器數據（例如溫度、壓力）。
地址範圍：從 30001 到 39999（在數據包中通常從 0 開始計數）。
操作：只能讀取，不能寫入。
範例：設備的溫度感測器測量到 25°C，對應的輸入暫存器將會存儲這個值。
4. **保持暫存器（Holding Registers）**
功能：表示可讀寫的類比量數據，通常用於讀取或寫入設定參數，這些參數可能影響設備運行。
地址範圍：從 40001 到 49999（在數據包中通常從 0 開始計數）。
操作：可讀取和寫入。
範例：Modbus Master 可以寫入一個目標速度到保持暫存器，控制設備馬達的旋轉速度。
    
    ![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/5%202%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4%20-%20MODBUS/image%205.png)