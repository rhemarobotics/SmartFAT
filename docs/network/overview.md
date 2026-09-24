# 5. 物聯網網路層

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

<aside>
💡 物聯網的網路層是連接感知層與應用層的中間層，負責傳輸來自感知層的數據到應用層，並將應用層的控制命令傳送到感知層中的設備。它在物聯網架構中起著至關重要的橋樑作用，確保數據在不同設備和系統之間的傳遞和通信。網路層的主要功能和技術如下：

</aside>

# **壹、無線通訊技術**

以下是幾個常見的網路層無線通訊技術：

## 一、Wi-Fi：

Wi-Fi是一種常見的無線局域網技術，它使用IEEE 802.11標準，廣泛應用於辦公環境和家庭網絡。在工業領域，Wi-Fi通常用於資料收集、設備監控和控制，特別是在需要高速數據傳輸的應用中，目前最新為WiFi 6。

![](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/image23.jpg)

## 二、藍牙（Bluetooth）：

藍牙技術提供了短距離通信，用於低功耗應用和設備之間的連接。在工業領域，藍牙通常應用於物聯網裝置之間的通信，例如嵌入式感測器和行動設備的互聯，在未來，藍牙5.0 因其優勢將會成為主流。

![image.png](../assets/5%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B6%B2%E8%B7%AF%E5%B1%A4/image.png)

## 三、Zigbee：

Zigbee是一種低功耗、自組織和自愈合的無線通信技術。它適用於需要節能和長期運行的工業自動化應用，如智能照明、監控系統和無線感測網絡。

## 四、Z-Wave：

Z-Wave是一種專門用於家庭自動化和工業控制的無線技術。它在工業環境中常用於建築監控系統、安全系統和能源管理等領域。

## 五、LoRaWAN：

LoRaWAN是一種遠距離低功耗的無線通信技術，適用於長距離的感測和監控應用。它被廣泛應用於智慧城市、農業監測和環境監測等場景。

## 六、NB-IOT：

NB-IoT，全稱窄帶物聯網（Narrowband Internet of Things），是一種專為物聯網（IoT）應用而設計的低功耗、低速率無線通信技術。NB-IoT基於現有的LTE（Long Term Evolution）網絡基礎設施，但對於小數據傳輸和節能方面做了優化，以支援大量低功耗、低帶寬的物聯網裝置。

# 貳**、通訊協議**

以下是幾個常見的通訊協議：

## 一、IPv6：

IPv6（Internet Protocol version 6）是一種網際網路協議，取代了IPv4，它擁有更大的IP地址空間，可支援更多的連接設備。這對於物聯網來說至關重要，因為預計將有數十億個裝置需要連接。

## 二、LoWPAN：

LoWPAN（IPv6 over Low-power Wireless Personal Area Networks），是一種將IPv6協議應用於低功耗無線個人區域網絡的技術。它允許物聯網中的低功耗裝置通過無線方式進行連接，同時保持高效能和節能。

## 三、RPL：

RPL（Routing Protocol for Low-power and Lossy Networks），是專為低功耗和丟包網絡設計的路由協議。它確保數據能夠以有效的方式從源節點路由到目標節點，同時考慮到物聯網中裝置的限制。

## 四、CoAP：

CoAP（Constrained Application Protocol）是一個輕量級的應用層協議，專為物聯網裝置設計。它提供了簡單的RESTful接口，使得裝置可以進行高效的數據交換。

## 五、MQTT：

MQTT（Message Queuing Telemetry Transport）是一種輕量級的消息通訊協議，它對於低帶寬和不穩定網絡環境非常適用。它支援發布/訂閱模型，可以使裝置之間進行高效的通信。

[5.1 物聯網網路層 - MQTT](mqtt.md)

[5.2 物聯網網路層 - MODBUS](modbus.md)