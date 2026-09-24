# 7.1. 機器人座標系統

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

# 機器人座標系定義

是爲了描述機器人當前的位置或姿態與其他空間座標系的相對應關係，一般都用笛卡爾坐標系來定義。機器人座標系比較常用的包括以下四種：

![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%201%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%BA%A7%E6%A8%99%E7%B3%BB%E7%B5%B1/image.png)

1. 機器人大地坐標系(World-Coordinate System)
    - 大地(世界)座標系是固定在空間上的標準直角座標系，它被固定在事先確定的位置。
2. 機器人基座坐標系(Base-Coordinate System)
    - 基座標系由機器人底座基點與座標方位組成，該座標系是機器人其它座標系的基礎。
3. 機器人工具坐標系(Tool-Coordinate System)
    - 機器人工具座標系是由工具中心點(TCP)與座標方位組成
4. 機器人工件坐標系(Workpiece-Coordinate System)
    - 機器人工件座標系是由工件原點與座標方位組成。

# 智慧機器人座標系統定義

本實驗平台的智慧機器人採用基座坐標系，手臂向前的方向定義為Y軸，根據右手定則可以定義X軸，向上定義為Z軸，如下圖所示。

![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%201%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%BA%A7%E6%A8%99%E7%B3%BB%E7%B5%B1/image%201.png)