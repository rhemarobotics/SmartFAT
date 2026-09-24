# 8.3. OpenCV 基礎操作實務

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

本單元是機器視覺的起點。我們將從數位影像的底層邏輯（矩陣）出發，學習如何利用 OpenCV 對影像進行基礎的預處理與轉換，為後續的工業辨識任務奠定基礎。

## 📋 實習 8.3.1：影像載入與環境驗證 (Image Loading)

---

> 實驗情境：
> 
> 
> 在智慧工廠的視覺檢測系統中，第一步必須確保系統能正確讀取工業相機或本地端儲存的數位影像。本節將透過 OpenCV 基礎函式，練習影像的讀取、顯示與記憶體釋放。
> 

---

### ⚙️ 動作要求

1. **開啟終端機**：進入 Raspberry Pi 系統環境。
2. **定位路徑**：找到專案路徑 `/home/pi/RhemaRobotics/Vision/opencvFund/` 。
3. **執行程式**：執行 `chap1.py` 並觀察彈出的視窗影像。
4. **觀察結果**：確認視窗顯示標題為 `output` 且圖片內容正確，如下圖所示。

---

### 💻 範例程式：chap1.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：影像載入與視窗控制實作
說明：本程式演示如何將本地端圖片載入至 NumPy 矩陣並進行顯示。
執行：python3 chap1.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8

import sys

# 將雷瑪機器視覺函式庫路徑加入系統搜尋路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')

import cv2
import numpy as np

# 1. 影像讀取 (Read)
# 使用 imread 函式載入 Resource 資料夾中的 lena.png
# 注意：若路徑錯誤，img 將回傳為 None
img = cv2.imread('Resource/lena.png')

# 2. 影像顯示 (Show)
# 'output' 為顯示視窗的名稱，img 為要顯示的影像矩陣
cv2.imshow('output', img)

# 3. 視窗等待 (Wait)
# waitKey(0) 會讓程式暫停，直到使用者按下鍵盤上的任意鍵
# 若不加此行，視窗會因程式執行結束而瞬間關閉
cv2.waitKey(0)

# 4. 資源釋放 (Clean up)
# 釋放所有由 OpenCV 開啟的視窗，避免記憶體洩漏
cv2.destroyAllWindows()
```

---

### 📝 教學重點筆記 (University Level)

| **關鍵函式** | **功能說明** | **參數意義** |
| --- | --- | --- |
| `cv2.imread()` | 將圖檔解碼為多維矩陣 | 第一參數為圖片路徑 |
| `cv2.imshow()` | 建立視窗並繪製矩陣內容 | `'output'` 為視窗標題 |
| `cv2.waitKey(0)` | 阻塞程序運行，監聽按鍵事件 | `0` 表示無限等待 |
| `shape`屬性 | 可透過 `img.shape` 觀察解析度 | 回傳 (高度, 寬度, 通道數) |

> 💡 小提醒：
> 
> 
> 在工業現場，若 cv2.imread() 讀取失敗，通常是因為路徑不正確或檔案權限不足。在進行下一單元前，請務必確保你能看到視窗影像。
> 

---

### 📷 成果紀錄

- **截圖區域**：(請在此處貼上執行 `chap1.py` 後的畫面截圖)
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image.png)
    
- **心得筆記**：(紀錄你在執行過程中的觀察，例如視窗大小與圖片畫質)

## 📋 實習 8.3.2：影像進階處理 (Advanced Image Processing)

> 實驗情境：
> 
> 
> 在自動化流水線上，相機擷取的彩色影像資訊量過大且包含環境干擾。本實驗將模擬工業視覺的「特徵提取流水線」，將雜亂的影像轉化為乾淨的幾何輪廓，以便後續機械手臂進行精確定位。
> 

---

### ⚙️ 動作要求

1. **開啟程式**：開啟專案路徑下的範例程式 `chap2.py`。
2. **參數調整**：觀察高斯模糊的卷積核尺寸（Kernel Size）與 Canny 的高低閾值對結果的影響。
3. **執行並對比**：執行程式後，應同時出現三種處理階段的視窗。

---

### 💻 範例程式：chap2.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：影像預處理流水線實作 (灰階、模糊、邊緣偵測)
說明：演示如何將原始影像過濾雜訊並提取結構特徵。
執行：python3 chap2.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8

import sys
# 加入雷瑪視覺路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')

import cv2
import numpy as np

# 載入原始測試影像
img = cv2.imread('Resource/lena.png')

# 1. 灰階處理 (Grayscale)
# 將 BGR 三通道影像轉為單通道灰階影像，減少 2/3 的運算量
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 高斯模糊 (Gaussian Blur)
# 使用 11x11 的捲積核，標準差設為 11。用於消除影像細微雜訊(降噪)
img_gb = cv2.GaussianBlur(img_gray, (11, 11), 11)

# 3. Canny 邊緣偵測 (Edge Detection)
# 使用雙閾值法提取輪廓。20 為低閾值，80 為高閾值
# 低於 20 會被捨棄，高於 80 會被視為強邊緣
img_canny = cv2.Canny(img_gb, 20, 80)

# 4. 顯示各階段處理結果
cv2.imshow('Gray', img_gray)      # 顯示灰階圖
cv2.imshow('Blur', img_gb)        # 顯示模糊圖
cv2.imshow('Canny', img_canny)    # 顯示邊緣輪廓圖

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### 📝 技術深度解析 (University Level)

| **處理步驟** | **數學/技術原理** | **工業應用目的** |
| --- | --- | --- |
| **灰階轉換** | $Y = 0.299R + 0.587G + 0.114B$ | 簡化資料，加快後端演算法速度。 |
| **高斯模糊** | 對鄰域像素進行加權平均（正態分佈） | 濾除電子感測器產生的顆粒雜訊。 |
| **Canny 偵測** | 計算像素梯度強度與方向 | 鎖定零件物理邊界，準備進行尺寸測量。 |

> 💡 實作技巧：
> 
> 
> 如果 img_canny 出現太多破碎的線條，試著增加 GaussianBlur 的核尺寸（例如從 (11,11) 改為 (15,15)），或者調高 Canny 的低閾值。
> 

---

### 📷 實驗成果紀錄表

- **原始與灰階對比**：(請描述轉換後影像資訊量有何變化)
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%201.png)
    
- **模糊前後差異**：(觀察邊緣是否變得平滑？)
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%202.png)
    
- **Canny 執行截圖**：
    - [ ]  成功擷取邊緣輪廓。
    - [ ]  輪廓線條連續且清晰。
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%203.png)
    

---

**接下來，我們要進入 8.3.3「影像大小改變與裁切實習」嗎？這對於限制處理範圍（ROI）以節省硬體資源非常關鍵。**

---

## 📋 實習 8.3.3：影像大小改變與裁切 (Resize & Crop)

> 實驗情境：
> 
> 
> 智慧工廠的處理器（如 Raspberry Pi）資源有限。若直接處理高解析度影像會導致延遲。本實驗練習如何調整影像維度，並利用矩陣切片技術，精確地「裁切」出輸送帶上的工件區域（ROI）。
> 

---

### ⚙️ 動作要求

1. **開啟程式**：開啟路徑下的範例程式 `chap3.py`。
2. **座標定義**：理解 Python 矩陣中 `[y1:y2, x1:x2]` 的座標邏輯。
3. **執行觀察**：比較縮放後的解析度變化，以及裁切後影像保留的局部細節。

---

### 💻 範例程式：chap3.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：影像幾何變換實作 (縮放與局部裁切)
說明：學習如何調整影像尺寸並選取感興趣區域 (ROI)。
執行：python3 chap3.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8

import sys
# 加入雷瑪視覺函式庫路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')

import cv2
import numpy as np

# 載入原始測試影像
img = cv2.imread('Resource/lambo.png')

# 1. 改變影像大小 (Resize)
# 將影像強制縮放為 寬320 像素、高240 像素
# 注意：參數順序為 (寬, 高)
img_resize = cv2.resize(img, (320, 240))

# 2. 影像裁切 (Crop / ROI)
# 利用 NumPy 陣列切片：img[y_start:y_end, x_start:x_end]
# 這裡選取 y 座標 10~200 與 x 座標 10~200 的範圍
img_crop = img[10:200, 10:200]

# 顯示處理結果
cv2.imshow('Original', img)     # 原始影像
cv2.imshow('Resize', img_resize) # 縮放影像 (320x240)
cv2.imshow('Crop', img_crop)     # 裁切後的區域 (ROI)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### 📝 技術深度解析 (University Level)

| **技術術語** | **運作邏輯** | **工業應用目的** |
| --- | --- | --- |
| **Resize (縮放)** | 透過插值演算法（如雙線性插值）重新計算像素 | 降低資料量，確保即時控制系統的 FPS (每秒幀數)。 |
| **ROI (感興趣區域)** | 僅保留矩陣中特定的索引範圍 | 排除環境雜訊（如輸送帶邊框），專注辨識工件。 |
| **Array Slicing** | `img[y, x]` 矩陣切片 | OpenCV 與 NumPy 結合的高效記憶體操作方式。 |

> 💡 實作技巧：
> 
> 
> 在執行裁切時，必須確保 y_end 不超過影像的高度，x_end 不超過影像的寬度，否則程式會拋出「Index Out of Range」錯誤。你可以透過 img.shape 先確認原始影像的大小。
> 

---

### 📷 實驗成果紀錄表

- **縮放效果觀察**：(請描述縮放至 320x240 後，影像細節是否有明顯遺失？)
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%204.png)
    
- **ROI 座標紀錄**：
    - 左上角座標 $(x, y)$：__________
    - 右下角座標 $(x, y)$：__________
- **執行截圖**：
    - [ ]  成功產出三種尺寸不同的視窗。

---

**準備好進入 8.3.4「影像繪圖實習」了嗎？我們將學習如何在偵測到工件後，於畫面上繪製視覺化的標記資訊！**

---

## 📋 實習 8.3.4：影像繪圖標記 (Drawing on Images)

> 實驗情境：
> 
> 
> 當視覺系統成功定位到傳送帶上的零件後，我們需要在畫面上即時繪製「偵測框」或「分類標籤」。本實驗將練習如何利用 OpenCV 的繪圖函式，在影像矩陣上疊加直線、圓形、矩形以及文字資訊。
> 

---

### ⚙️ 動作要求

1. **開啟程式**：開啟專案路徑下的範例程式 `chap4.py`。
2. **座標控制**：學習 OpenCV 的 (x, y) 座標系統（原點在左上角）。
3. **顏色與粗細**：理解顏色參數為 `(B, G, R)` 格式，並觀察粗細參數對視覺效果的影響。

---

### 💻 範例程式：chap4.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：影像繪圖與標註實作
說明：學習在影像上繪製基礎幾何圖形與文字標記。
執行：python3 chap4.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8

import sys
# 加入雷瑪視覺函式庫路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')

import cv2
import numpy as np

# 載入原始測試影像
img = cv2.imread('Resource/lambo.png')

# 1. 畫直線 (Line)
# 參數：(影像, 起點座標, 終點座標, 顏色BGR, 粗細)
# 繪製一條藍色直線
cv2.line(img, (10, 10), (100, 10), (255, 0, 0), 5)

# 2. 畫圓形 (Circle)
# 參數：(影像, 圓心座標, 半徑, 顏色BGR, 粗細 -1表示填滿)
# 繪製一個綠色空心圓
cv2.circle(img, (100, 100), 50, (0, 255, 0), 2)

# 3. 畫矩形 (Rectangle) - 工業視覺中最常用於標記目標物
# 參數：(影像, 左上角座標, 右下角座標, 顏色BGR, 粗細)
# 繪製一個紅色矩形框
cv2.rectangle(img, (200, 50), (300, 150), (0, 0, 255), 3)

# 4. 加上文字 (Put Text)
# 參數：(影像, 內容, 座標, 字型, 大小, 顏色, 粗細)
cv2.putText(img, 'Rhema Robotics', (50, 250), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 顯示繪圖結果
cv2.imshow('Draw Result', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### 📝 技術深度解析 (University Level)

| **函式名稱** | **關鍵參數說明** | **工業實務應用** |
| --- | --- | --- |
| **`cv2.line`** | `(x, y)` 座標起終點 | 用於繪製基準線或量測路徑。 |
| **`cv2.circle`** | 半徑 (Radius) | 用於標記物件質心 (Centroid) 或圓孔定位。 |
| **`cv2.rectangle`** | `thickness` (若設為 -1 則為實心) | 用於物件偵測 (Object Detection) 的邊界框 (Bounding Box)。 |
| **`cv2.putText`** | `fontFace` (支援多種字型) | 即時顯示工件編號、信心度或分類結果。 |

> 💡 實作技巧：
> 
> 
> OpenCV 的顏色順序是 BGR (藍, 綠, 紅)，這與常見的 RGB 順序相反。例如 (255, 0, 0) 代表純藍色。在標記多個物件時，建議使用不同顏色來區分不同類別的產品。
> 

---

### 📷 實驗成果紀錄表

- **繪圖準確性**：(標記的位置是否符合預期座標？)
- **顏色對比度**：(觀察在不同的背景下，哪種顏色的文字最容易被肉眼辨識？)
- **執行截圖**：
    - [ ]  成功在影像上顯示矩形、圓形與 Rhema Robotics 字樣。
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%205.png)
    

---

## 📋 實習 8.3.5：影像投射轉換 (Perspective Transform)

> 實驗情境：
> 
> 
> 在自動化生產線上，相機往往無法正對工件拍攝。這會導致原本是矩形的工件在影像中變成不規則的四邊形。本實習透過「投射轉換（Perspective Transform）」，將歪斜的影像座標重新映射到標準的矩形平面上，實現精確的尺寸量測與辨識。
> 

---

### ⚙️ 動作要求

1. **開啟程式**：開啟專案路徑下的範例程式 `chap5.py`。
2. **座標對應**：理解原圖四個頂點座標（pts1）與轉換後目標座標（pts2）的對應關係。
3. **執行觀察**：觀察原本歪斜的圖片如何被「拉正」成一個標準的 400x500 矩形。

### 💻 範例程式碼與註解：chap5.py

python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：影像投射轉換 (Perspective Transform) 實作
說明：將斜向拍攝的影像座標重新映射，還原為正視平面圖。
執行：python3 chap5.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
# 將雷瑪機器視覺函式庫路徑加入系統搜尋路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')
import cv2
import numpy as np

# 1. 載入原始影像
img = cv2.imread('Resource/cards.png')

# 2. 定義輸出影像的維度 (寬, 高)
# 這代表您希望轉換後得到的標準矩形尺寸
wid, hgt = 400, 500

# 3. 定義原圖中的四個頂點座標 (來源點 pts1)
# 順序必須一致：[左上, 右上, 左下, 右下]
# 這些座標通常透過手動量測或自動輪廓偵測獲得
pts1 = np.float32([[591, 1], [1327, 192], [4, 937], [971, 1247]])

# 4. 定義輸出影像中的四個對應點 (目標點 pts2)
# 將來源點分別映射到輸出畫布的四個角落
pts2 = np.float32([[0, 0], [wid, 0], [0, hgt], [wid, hgt]])

# 5. 核心應用：計算轉換矩陣
# 使用 cv2.getPerspectiveTransform 計算 3x3 的變換矩陣
matrix = cv2.getPerspectiveTransform(pts1, pts2)

# 6. 核心應用：執行投影轉換
# 將原圖透過矩陣進行像素重組，生成指定大小的輸出影像
imgOut = cv2.warpPerspective(img, matrix, (wid, hgt))

# 顯示處理對比
cv2.imshow('original', img) # 原始歪斜圖
cv2.imshow('warp', imgOut)    # 轉換後正視圖

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### 🧠 投影函式應用方式解析

在 OpenCV 中，實現影像校正主要依賴以下兩個關鍵函式的協作：

### 1. `cv2.getPerspectiveTransform(src, dst)`

- **應用方式**：此函式負責「計算規律」。它需要兩組點：一組是影像中歪斜物體的四個角點（`src`），另一組是您希望這些角點在結果圖中出現的位置（`dst`）。
- **運算邏輯**：它會回傳一個 **3x3 的變換矩陣**。這個矩陣包含了所有旋轉、縮放與透視偏移的數學參數。

### 2. `cv2.warpPerspective(src, M, size)`

- **應用方式**：此函式負責「執行轉換」。它接收原始影像（`src`）與剛才算好的矩陣（`M`），並依照您指定的尺寸（`size`）重新繪製所有像素。
- **工業用途**：在 Rhema Robotics 的手臂校正中，當我們知道標誌物在空間中的真實比例，透過此函式就能將相機畫面轉換為「俯視地圖」，進而直接算出工件在輸送帶上的實際 (x, y) 毫米座標。

---

### 📝 教學小提醒

- **點的順序**：如果執行結果出現「交叉」或「翻轉」，通常是因為 `pts1` 與 `pts2` 的點順序不匹配。請務必檢查順序是否皆為：**左上 →右上 → 左下 → 右下**。
- **座標獲取**：在實務中，如果 `cards.png` 的背景複雜，建議先使用本手冊 **的輪廓偵測** 來自動抓取這四個頂點座標。

---

### 📷 實驗成果紀錄表

- **變換前後觀察**：(原本歪斜的圖像在轉換後是否變成了矩形？邊緣是否有失真？)
- **數學驗證**：觀察 `matrix` 矩陣的值（可在程式中加入 `print(matrix)`）。
- **執行截圖**：
    - [ ]  成功完成 Warp Perspective 轉換。
    
    ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%203%20OpenCV%20%E5%9F%BA%E7%A4%8E%E6%93%8D%E4%BD%9C%E5%AF%A6%E5%8B%99/image%206.png)
    

## 🏁 單元 8.3 實習小結

恭喜你完成了 **Rhema Robotics 機器視覺基礎單元**！在本單元的五個實驗中，你已經掌握了：

1. **載入與顯示** (8.3.1)
2. **預處理降噪** (8.3.2)
3. **區域裁切與縮放** (8.3.3)
4. **結果標註** (8.3.4)
5. **視角校正** (8.3.5)

這些技術是所有進階視覺專案的「地基」。下一步，我們將進入 **8.4 節：色彩辨識實務**，結合本章所學的技巧，讓機器人開始學會「分辨顏色」並進行分檢任務。