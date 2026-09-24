# 3. 實驗平台開發環境

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

# **壹**、樹莓派網路通訊設置

智慧工廠教學實驗平台的操作環境，主要有兩種方式 : 

## 一、遠端連線操控

- 遠端連線操控，就是不用另外連接螢幕和鍵盤，單單以遠端連線工具(如vnc viewer)，連至智慧工廠進行程式開發或測試等應用。
    
    <aside>
    📌 VNC (Virtual Network Computing) 一種使用 RFB 協定的遠端操作軟體，藉由網路，傳送鍵盤與滑鼠的動作及即時的螢幕畫面。VNC 可跨平台使用，可用 Windows 連線到 Linux 電腦，反之亦同。
    
    官網下載 : [https://www.realvnc.com/en/connect/download/viewer/windows/](https://www.realvnc.com/en/connect/download/viewer/windows/)
    
    </aside>
    
1. 網路線連接(**👍**)：
    
    個人電腦透過網路線直接連至智慧工廠上樹莓派的Ethernet 埠口，連線較為穩定，遠端操作速度也較靈敏(因為樹莓派的Ethernet 埠口是True Gigabit Ethernet，網路頻寬足夠大，**推薦此方式**)。
    
2. 設定乙太網路介面卡(個人電腦端)：
    
    更改【TCP/IPv4】內容，如下圖所示，主要是把個人電腦端的IP 位址更改至與智慧工廠同一網域空間【192.168.0.x】，彼此才能進行通訊。
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled.png)
    
3. 執行VNC Viewer 軟體(個人電腦端)：
    
    輸入智慧工廠端的IP 位址【192.168.0.1】，如下圖所示。
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%201.png)
    
    待成功連線後，會出現要求使用者輸入遠端登入名稱和密碼，預設的帳號/密碼如下，接著繼續按下**Continute**按鍵，就會進入遠端桌面操控環境。
    
    <aside>
    🔒 user name : pi
    password : raspberry
    
    </aside>
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%202.png)
    
4. 遠端桌面操控環境 - 包含程式範例實習會用的軟體捷徑
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%203.png)
    

## 二、樹莓派本地端操控

- 把智慧工廠實驗平台當作本地端的電腦來操作，需另加上螢幕和鍵盤滑鼠，使用方式與一般的電腦相同(皆為圖形化操作介面)。

## 三、樹莓派連上外部網路

- 原本在樹莓派的 Ethernet 接口設置為靜態 IP，但如果需要連接到外部網路，可以參考以下方法將其更改為動態分配 IP。
1. 編輯 /etc/network/interfaces.d/eth0 文件
    
    ```bash
    sudo nano /etc/network/interfaces.d/eth0
    ```
    
2. 註解原本內容，設置接口為 DHCP，保存並退出
    
    ```bash
    #auto eth0
    #iface eth0 inet static
    #        address 192.168.0.1
    #        netmask 255.255.255.0
    #        dns-nameservers 168.95.1.1 8.8.8.8
    
    auto eth0
    iface eth0 inet dhcp
    ```
    
3. 重啟網絡服務，並重新確認新ip位址
    
    ```bash
    sudo systemctl restart networking
    ```
    

# **貳、實驗平台檔案管理系統**

- 探索智慧工廠教學實驗平台開發的範例程式，了解其存放位置及內容，有助於深入了解平台功能和應用。
    
    <aside>
    📌 **/home/pi/Arduino**             - Arduino範例程式所需的程式庫
    **/home/pi/ArduinoProject**  - Arduino範例程式
    **/home/pi/NodeProject**      - Node Red範例程式
    **/home/pi/RhemaRobotics** - 智慧工廠範例程式
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%204.png)
    
    </aside>
    

## 一、📁 ArduinoProject 資料夾內容

- 放置實驗平台所有感測器的Arduino範例程式，共計17個。
- 另外四個(SmartFactoryEx1、SmartFactoryEx2、SmartFactoryEx3和VisualData_pt)，則是整合於**智慧工廠堆棧系統、智慧工廠視覺分檢系統、智慧工廠重量分檢系統及智慧工廠雲端大數據可視化系統**的應用裏。
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%205.png)
    

## 二、📁 NodeRedProject 資料夾內容

- 放置實驗平台Node Red範例程式(json文件)。
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%206.png)
    

## 三、📁 RhemaRobotics 資料夾內容

- 放置智慧工廠整合應用範例程式。
    
    <aside>
    📌 Demo - 範例主程式
    Documents - 樹莓派初學者使用文件(參考用)
    Robot - 智慧機器人控制API模組(module)
    Sdk - 智慧語音/播報API模組、智慧馬達通訊API模組及運動學轉換API模組
    Vision - 機器視覺API模組
    
    </aside>
    
    ![Untitled](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/Untitled%207.png)
    

# **叁、VS CODE 遠端程式開發**

- 遠端開發 (remote develop) 是 VSCode 的一個非常酷且實用的功能。它讓你在遠端的樹莓派上開發時，感覺就像在本地開發一樣，二者之間的通信原理，如圖所示。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image.png)
    

## 一、🖥本地電腦端安裝 VS Extension工具 – Remote_SSH

- 在 VS Code 中，搜尋並安裝 Remote - SSH 和 C/C++ 擴充套件。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image%201.png)
    

## 二、智慧工廠端 : 啟動 ssh-server

- 檢查 SSH (Secure Shell) 服務狀態的指令。
    
    ```bash
    sudo systemctl status ssh 
    ```
    
- Active (running) : SSH 服務正常運行中，可以接受連線。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image%202.png)
    

## 三、🖥透過 VS Code Remote - SSH 連線至遠端主機

- 本地電腦端安裝完擴展後，按F1鍵或者Ctrl+Shift+P組合鍵調出命令面板，然後選擇 Remote-SSH: Connect to Host 命令。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image%203.png)
    

## 四、🖥VS Code 開啟遠端專案資料夾

- 成功連線後，你可以選擇遠端主機上的資料夾作為工作目錄。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image%204.png)
    

## 五、🖥開始遠端開發程式

- 同步與編譯。
    - 在 VS Code 中使用 Ctrl+Shift+B 執行 build 任務。
    - 編譯完成後，直接在遠端啟動與測試，或透過 Debugger 進行遠端調試。
    
    ![image.png](../assets/3%20%E5%AF%A6%E9%A9%97%E5%B9%B3%E5%8F%B0%E9%96%8B%E7%99%BC%E7%92%B0%E5%A2%83/image%205.png)