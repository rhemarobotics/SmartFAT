# 8.2. OpenCV 簡介

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

## OpenCV 核心指南：從基礎影像處理到機器視覺實務

OpenCV (Open Source Computer Vision Library) 是一套專為影像處理與電腦視覺開發的開源函式庫。本指南將引導你透過 Python 快速建立從「讀取影像」到「特徵提取」的開發能力。

![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%202%20OpenCV%20%E7%B0%A1%E4%BB%8B/image.png)

---

## 一、 OpenCV 概觀：賦予電腦視覺能力

OpenCV 不僅是工具包，更是電腦視覺領域的標準。

- **技術定位**：跨平台（Linux, Windows, Android）、多語言支持（C++, Python, Java）。
- **工業 4.0 應用**：
    - **智慧監控**：人臉偵測、行為分析。
    - **自動化生產**：物體定位、瑕疵檢測（AOI）、QR Code 讀取。
    - **移動平台**：自動駕駛中的車道線辨識與避障。
- **優勢**：社群龐大、運算速度快（基於 C++ 最佳化）、與人工智慧框架（PyTorch/TensorFlow）高度相容。

---

## 二、 環境建置與開發準備

在開始寫程式前，請確保開發環境已正確安裝。

### 1. 安裝步驟

在 Notion 中建議使用「程式碼區塊」記錄指令：

- **核心庫安裝**：Bash
    
    ```jsx
    pip install opencv-python
    ```
    
- **擴充庫安裝**（包含更多進階演算法）：Bash
    
    ```jsx
    pip install opencv-contrib-python
    ```
    

### 2. 環境驗證

開啟 Python 終端機執行以下指令：

Python

```jsx
import cv2
print(cv2.__version__) # 顯示當前版本即代表安裝成功
```

---

## 三、 核心操作：影像處理流水線 (Pipeline)

所有的視覺任務都遵循一個標準流程：**輸入 -> 預處理 -> 特徵提取 -> 輸出**。

### 1. 影像輸入與顯示 (Input & Output)

- **`cv2.imread()`**：讀取影像。注意 OpenCV 預設色彩空間為 **BGR**。
- **`cv2.imshow()`**：彈出視窗顯示影像。
- **`cv2.imwrite()`**：將處理結果儲存為檔案。

### 2. 影像預處理 (Pre-processing)

- **色彩空間轉換**：利用 `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` 將彩色轉灰階，降低計算複雜度。
- **影像平滑 (Smoothing)**：使用高斯模糊 `cv2.GaussianBlur()` 去除高頻雜訊。
- **尺寸調整 (Scaling)**：使用 `cv2.resize()` 調整影像大小以符合模型輸入要求。

### 3. 特徵提取與辨識 (Feature Extraction)

- **邊緣偵測 (Canny Edge)**：精確定位物體邊界。
- **形態學運算**：透過「膨脹 (Dilation)」與「侵蝕 (Erosion)」優化二值化影像，去除細小雜點。
- **輪廓搜尋 (Contours)**：尋找封閉區域，計算物體面積、周長與中心點座標。

---

## 四、 實習專案：即時影像捕捉

影像處理不限於靜態圖片，OpenCV 強大的地方在於處理**即時視訊串流**。

Python

```jsx
import cv2

# 開啟攝影機 (0 代表預設鏡頭)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() # 讀取每一幀畫面
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 即時轉灰階
    cv2.imshow('Live Video', gray)
    
    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 五、 總結：從視覺觀念邁向實務開發

透過這篇簡介，你已經掌握了 OpenCV 的基本核心——它不只是處理照片的工具，更是智慧製造與自動化系統的「大腦」。但電腦視覺是一門「實作先行」的技術，所有的演算法邏輯，都必須透過程式碼在真實影像中反覆驗證。

### 🚀 準備好進入實驗室了嗎？

在接下來的 **8.3 節：OpenCV 基礎操作實務** 中，我們將不再只談論理論，而是會進入實際的「工業影像處理流水線」。你將親手實作以下關鍵技術：

- **數位影像的拆解**：親自讀取並操控影像矩陣，觀察 BGR 色彩空間的奧秘。
- **工業級預處理**：練習如何透過灰階轉換與高斯模糊，把雜亂的原始畫面變成電腦容易辨識的數據。
- **特徵提取實戰**：使用 Canny 演算法精確抓取零件邊緣，並學習如何標記目標物體。

> 結語：電腦視覺的迷人之處在於「所見即所得」。現在，請開啟你的開發環境，讓我們從 8.3 節的第一個實驗開始，親眼見證電腦是如何一步步「看懂」這個世界的！
> 

---

### 💡 實作前的小提醒：

- 確保你的 **Python 環境**與 **opencv-python** 套件已依照第二章說明安裝完畢。
- 準備好一張你想要處理的測試圖檔（例如工件照片或 Lena 圖），我們在 **8.3.1 影像載入實驗** 見！