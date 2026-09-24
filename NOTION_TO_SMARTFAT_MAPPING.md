# NOTION_TO_SMARTFAT_MAPPING.md

本文件記錄由 Notion 匯出之 Markdown 教學文件對照至 SmartFAT MkDocs Material 文件庫（`docs/`）的完整搬移、重命名與路徑規劃對照表。

---

## 一、文件對照表 (47 個 Markdown 檔案)

| Original File | Original Location | New Location | Action | Reason |
| :--- | :--- | :--- | :--- | :--- |
| `智慧工廠教學實驗平台 fb2260ded710481e96b90ba4a067b0fd.md` | `.` | `docs/index.md` | move | 教學手冊首頁與教材總目錄導覽 |
| `產品與文件使用聲明書 1294a0cf79fe808d967ada6414bc2413.md` | `智慧工廠教學實驗平台` | `docs/product/disclaimer.md` | move | 產品與教材使用授權與聲明書 |
| `1 智慧工廠簡介 041d41d2034d4540b5a345d81f997b94.md` | `智慧工廠教學實驗平台` | `docs/product/smart-factory-intro.md` | move | 第1章 工業4.0與智慧工廠核心概念簡介 |
| `2 智慧工廠教學實驗平台 d93f7cec4bb74081a7f24de738327436.md` | `智慧工廠教學實驗平台` | `docs/product/overview.md` | move | 第2章 智慧工廠教學實驗平台硬體架構與概述 |
| `3 實驗平台開發環境 bd753aa1f67b430e9809916ced0927b2.md` | `智慧工廠教學實驗平台` | `docs/development/setup.md` | move | 第3章 實驗平台開發環境建置(樹莓派/Arduino/Node-RED) |
| `4 物聯網簡介 1274a0cf79fe80b58672c9512955d49c.md` | `智慧工廠教學實驗平台` | `docs/modules/overview.md` | move | 第4章 物聯網感測與致動模組實習概述 |
| `4 1 瓦斯氣體感測器實習 1274a0cf79fe80a989c8fc633cd402de.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/gas-sensor.md` | move | 4.1 瓦斯氣體感測器實習 |
| `4 2 火焰感測器實習 1274a0cf79fe80e0890ac830b68d699d.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/flame-sensor.md` | move | 4.2 火焰感測器實習 |
| `4 3 溫 溼度感測器實習 1274a0cf79fe80ffbd73c619a555d41c.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/dht-sensor.md` | move | 4.3 溫溼度感測器實習 |
| `4 4 環境光感測器實習 1284a0cf79fe807b815ce945cf6be3ac.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/ambient-light-sensor.md` | move | 4.4 環境光感測器實習 |
| `4 5 紅外線感測器實習 1284a0cf79fe8043a10be3b4f7529d09.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/ir-sensor.md` | move | 4.5 紅外線感測器實習 |
| `4 6 超音波感測器實習 1284a0cf79fe80398799c3208fa3d3ce.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/ultrasonic-sensor.md` | move | 4.6 超音波感測器實習 |
| `4 7 繼電器控制模組實習 1284a0cf79fe80fea300e140a5533a03.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/relay-module.md` | move | 4.7 繼電器控制模組實習 |
| `4 8 按鈕開關實習 1284a0cf79fe80e78c0fef126050616d.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/button-switch.md` | move | 4.8 按鈕開關實習 |
| `4 9 重量感測器實習 1274a0cf79fe8000b8fac07bb815b117.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/weight-sensor.md` | move | 4.9 重量感測器實習 |
| `4 10 無源蜂鳴器實習 1284a0cf79fe803c92d0cfb0a5ca6992.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/passive-buzzer.md` | move | 4.10 無源蜂鳴器實習 |
| `4 11 RGB LED燈實習 1284a0cf79fe80f89798e80405400e11.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/rgb-led.md` | move | 4.11 RGB LED燈實習 |
| `4 12 OLED模組實習 1284a0cf79fe809aa028fe0d96c6469d.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/oled-module.md` | move | 4.12 OLED模組實習 |
| `4 13 LED矩陣模組實習 1284a0cf79fe8063b33ae69401598436.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/led-matrix.md` | move | 4.13 LED矩陣模組實習 |
| `4 14 數字顯示器實習 1284a0cf79fe8038bb5bece499f52da6.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/digit-display.md` | move | 4.14 數字顯示器實習 |
| `4 15 旋轉電位器實習 1284a0cf79fe801286e1cbd00c874641.md` | `智慧工廠教學實驗平台/4 物聯網簡介` | `docs/modules/potentiometer.md` | move | 4.15 旋轉電位器實習 |
| `5 物聯網網路層 1284a0cf79fe80a89605f3e13f2d4be7.md` | `智慧工廠教學實驗平台` | `docs/network/overview.md` | move | 第5章 物聯網網路層概念概述 |
| `5 1 物聯網網路層 - MQTT 1284a0cf79fe80879ac6dd88e625c576.md` | `智慧工廠教學實驗平台/5 物聯網網路層` | `docs/network/mqtt.md` | move | 5.1 物聯網網路層 - MQTT 通訊協定 |
| `5 2 物聯網網路層 - MODBUS 1284a0cf79fe80dfbb25c696fa6018b1.md` | `智慧工廠教學實驗平台/5 物聯網網路層` | `docs/network/modbus.md` | move | 5.2 物聯網網路層 - MODBUS 通訊協定 |
| `6 物聯網應用層 12d4a0cf79fe802ab55dd7f78f88878f.md` | `智慧工廠教學實驗平台` | `docs/application/overview.md` | move | 第6章 物聯網應用層概念概述 |
| `6 1 第一個 Node-RED 程式 12a4a0cf79fe80c09e3bf6df50e10581.md` | `智慧工廠教學實驗平台/6 物聯網應用層` | `docs/application/first-node-red.md` | move | 6.1 第一個 Node-RED 程式 |
| `6 2 使用Node-RED Dashboard 09a6fecdd412421b8d6d32fc7c88d4a9.md` | `智慧工廠教學實驗平台/6 物聯網應用層` | `docs/application/node-red-dashboard.md` | move | 6.2 使用 Node-RED Dashboard |
| `6 3 使用Node-RED MQTT 16711563f7b0464fa5e604834b7471ea.md` | `智慧工廠教學實驗平台/6 物聯網應用層` | `docs/application/node-red-mqtt.md` | move | 6.3 使用 Node-RED MQTT 串接 |
| `6 4 使用Node-RED Modbus b8925ec09ce84c3b8752b801b7611b85.md` | `智慧工廠教學實驗平台/6 物聯網應用層` | `docs/application/node-red-modbus.md` | move | 6.4 使用 Node-RED Modbus 串接 |
| `6 5 打造 SCADA 監控系統儀表板 12d4a0cf79fe808c8582e86c20eacac9.md` | `智慧工廠教學實驗平台/6 物聯網應用層` | `docs/application/scada-dashboard.md` | move | 6.5 打造 SCADA 監控系統儀表板 |
| `7 智慧機器人 1424a0cf79fe804984fcce6465d9ae05.md` | `智慧工廠教學實驗平台` | `docs/robotics/overview.md` | move | 第7章 智慧機器人手臂系統概述 |
| `7 1 機器人座標系統 1424a0cf79fe8118b90de90360ef93f8.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/coordinate-system.md` | move | 7.1 機器人座標系統 |
| `7 2 機器人運動學 1424a0cf79fe812d9c06f659ce7c7dcb.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/kinematics.md` | move | 7.2 機器人正逆運動學 |
| `7 3 機器人硬體元件 1424a0cf79fe81eb82d9d48177d456a0.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/hardware-components.md` | move | 7.3 機器人硬體元件與機構 |
| `7 4 伺服馬達控制範例 1424a0cf79fe815aa84dfae9b6775fd2.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/servo-control.md` | move | 7.4 伺服馬達控制範例 |
| `7 5 伺服馬達監控範例 1424a0cf79fe8103acbdc3180b12aff2.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/servo-monitoring.md` | move | 7.5 伺服馬達狀態監控範例 |
| `7 6 智慧機器人堆棧範例 1424a0cf79fe8106a122f1962cb5d3fa.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/palletizing-example.md` | move | 7.6 智慧機器人堆棧範例 |
| `7 7 智慧機器人重量分檢範例 1424a0cf79fe81b3b15ae6fc97679bff.md` | `智慧工廠教學實驗平台/7 智慧機器人` | `docs/robotics/weight-sorting-example.md` | move | 7.7 智慧機器人重量分檢範例 |
| `8 機器視覺實務技術 1424a0cf79fe80039e5dfa6da7c80a3b.md` | `智慧工廠教學實驗平台` | `docs/vision/overview.md` | move | 第8章 機器視覺實務技術概述 |
| `8 1 機器視覺簡介 1424a0cf79fe80b88eefcd5aecf195d3.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/intro.md` | move | 8.1 機器視覺概念與應用簡介 |
| `8 2 OpenCV 簡介 1424a0cf79fe80109241ebc363097091.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/opencv-intro.md` | move | 8.2 OpenCV 視覺函式庫簡介 |
| `8 3 OpenCV 基礎操作實務 1424a0cf79fe803e9039ec37dfef63de.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/opencv-basics.md` | move | 8.3 OpenCV 影像處理基礎操作實務 |
| `8 4 色彩辨識實習 1424a0cf79fe80928f88e134c1adba85.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/color-recognition.md` | move | 8.4 色彩辨識實習 |
| `8 5 輪廓(Contour)辨識實習 1424a0cf79fe80f8beb2dced076d187e.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/contour-recognition.md` | move | 8.5 輪廓(Contour)辨識實習 |
| `8 6 計算目標物中心位置與座標轉換 1424a0cf79fe80eda049c6e807aeb641.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/coordinate-transformation.md` | move | 8.6 計算目標物中心位置與座標轉換 |
| `8 7 機器視覺與機器人協同作業 1424a0cf79fe80e78ab1c596df28c655.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/robot-collaboration.md` | move | 8.7 機器視覺與機器人協同作業 |
| `8 8 機器視覺與機器人協同實習總結 2d74a0cf79fe803599eaffa9f300c344.md` | `智慧工廠教學實驗平台/8 機器視覺實務技術` | `docs/vision/collaboration-summary.md` | move | 8.8 機器視覺與機器人協同實習總結 |

---

## 二、圖片與附件存放規則 (227 個圖片檔案)

為避免不同章節中常見檔名（如 `image.png`, `image 1.png`, `Untitled.png`）發生衝突，所有圖片依據章節與主題獨立存放在 `docs/assets/` 子目錄中：

| 來源目錄 (Notion) | 目標資產目錄 (MkDocs) | 圖片數量 |
| :--- | :--- | :--- |
| `1 智慧工廠簡介/` | `docs/assets/product/smart-factory-intro/` | 3 |
| `2 智慧工廠教學實驗平台/` | `docs/assets/product/overview/` | 11 |
| `3 實驗平台開發環境/` | `docs/assets/development/setup/` | 14 |
| `4 物聯網簡介/` (含4.1~4.15各子目錄) | `docs/assets/modules/<sensor-slug>/` | 46 |
| `5 物聯網網路層/` (含5.1 MQTT, 5.2 MODBUS) | `docs/assets/network/<proto-slug>/` | 15 |
| `6 物聯網應用層/` (含6.1~6.5各子目錄) | `docs/assets/application/<app-slug>/` | 78 |
| `7 智慧機器人/` (含7.1~7.7各子目錄) | `docs/assets/robotics/<robot-slug>/` | 19 |
| `8 機器視覺實務技術/` (含8.1~8.8各子目錄) | `docs/assets/vision/<vision-slug>/` | 41 |
| **總計** | | **227** |

---

## 三、內部超連結與圖片路徑修訂原則

1. **Markdown 內部導覽連結**：
   將所有原 Notion Page ID 連結（例如 `[1. 智慧工廠簡介](智慧工廠教學實驗平台/1%20智慧工廠簡介%20041d41d2034d4540b5a345d81f997b94.md)`）替換為新標準相對路徑（例如 `[1. 智慧工廠簡介](product/smart-factory-intro.md)`）。
2. **圖片引用路徑**：
   將相對路徑修正為對應的 `../assets/...` 或 `assets/...` 路徑，確保在 GitHub Web 與 MkDocs 渲染下均可正常顯示。

---

## 四、目錄層級說明

- `docs/index.md`：首頁與完整教材導覽。
- `docs/product/`：產品平台簡介、聲明書與工業 4.0 核心概念。
- `docs/development/`：開發環境建置與連線教學。
- `docs/modules/`：物聯網感測器、致動器與顯示器實習模組（共 15 個感測元件）。
- `docs/network/`：物聯網網路層教學（MQTT、MODBUS 通訊協定）。
- `docs/application/`：物聯網應用層教學（Node-RED 儀表板、SCADA 系統）。
- `docs/robotics/`：智慧機器人實務（座標系、運動學、伺服馬達、堆棧與分檢）。
- `docs/vision/`：機器視覺實務（OpenCV、色彩/輪廓辨識、視覺手臂協同作業）。
