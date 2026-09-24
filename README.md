# SmartFAT - 智慧工廠教學實驗平台

> **Industry 4.0 Smart Factory Teaching & Experimentation Platform**
> 
> 由雷瑪機器人（Rhema Robotics）研發，專為工業 4.0 打造的全方位智慧工廠教學實驗套件與實作教材。

---

## 📖 線上技術手冊與教材

本專案之完整教學實驗手冊已建立於 [`docs/`](docs/) 目錄，並支援透過 **GitHub Pages (MkDocs Material)** 進行線上閱讀：

* 🌐 **線上文件網址**：[https://rhemarobotics.github.io/SmartFAT/](https://rhemarobotics.github.io/SmartFAT/)
* 📚 **教材導覽首頁**：[docs/index.md](docs/index.md)
* 📋 **Notion 搬移對照表記錄**：[NOTION_TO_SMARTFAT_MAPPING.md](NOTION_TO_SMARTFAT_MAPPING.md)

---

## 📑 教材章節目錄

1. **產品與平台**
   * [產品與文件使用聲明書](docs/product/disclaimer.md)
   * [1. 智慧工廠簡介](docs/product/smart-factory-intro.md)：工業 4.0、CPS 與智慧製造核心概念
   * [2. 智慧工廠教學實驗平台](docs/product/overview.md)：平台機構設計、控制器與感測器配置
2. **開發環境建置**
   * [3. 實驗平台開發環境](docs/development/setup.md)：樹莓派網路連線、Arduino IDE 與 Node-RED 環境
3. **物聯網感測模組實習**
   * [4. 物聯網簡介與 15 項模組實習](docs/modules/overview.md)：氣體、火焰、溫溼度、環境光、超音波、重量、OLED、矩陣顯示等
4. **物聯網網路層**
   * [5. 物聯網網路層](docs/network/overview.md)：MQTT 與 MODBUS 工業通訊協定
5. **物聯網應用層**
   * [6. 物聯網應用層](docs/application/overview.md)：Node-RED 流程設計、儀表板與 SCADA 監控系統
6. **智慧機器人**
   * [7. 智慧機器人](docs/robotics/overview.md)：手臂座標系、運動學推導、伺服馬達監控、堆棧與分檢
7. **機器視覺實務技術**
   * [8. 機器視覺實務技術](docs/vision/overview.md)：OpenCV 影像處理、色彩/輪廓特徵辨識、視覺與手臂協同實務

---

## 📁 專案目錄結構

```text
SmartFAT/
├── Arduino/              # Arduino 韌體與驅動函式庫
├── ArduinoProjects/      # Arduino 範例專案
├── NodeRedProjects/      # Node-RED 儀表板與流程設定檔
├── RhemaRobotics/        # 雷瑪機器人整合程式模組
├── docs/                 # MkDocs 官方技術與實驗文件
│   ├── assets/           # 圖片與圖表資產
│   ├── product/          # 產品概念與平台說明
│   ├── development/      # 環境建置指南
│   ├── modules/          # 物聯網感測模組實驗
│   ├── network/          # 工業網路通訊 (MQTT / MODBUS)
│   ├── application/      # 應用層與 SCADA 儀表板
│   ├── robotics/         # 機器人手臂控制實務
│   └── vision/           # 機器視覺與手臂整合
├── mkdocs.yml            # MkDocs 網站設定檔
└── NOTION_TO_SMARTFAT_MAPPING.md
```

---

## 🛠 本地預覽文件網站

若欲於本機即時預覽 MkDocs 文件網站，請執行：

```bash
# 安裝 MkDocs Material
pip install mkdocs-material

# 啟動本地開發伺服器
mkdocs serve
```

開啟瀏覽器造訪 `http://127.0.0.1:8000/` 即可即時預覽。
