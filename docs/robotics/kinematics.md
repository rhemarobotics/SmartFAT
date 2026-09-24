# 7.2. 機器人運動學

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

運動學 (Kinematics)，定義機械手臂在不考慮速度與扭力的前提下，讓機械手臂可以在卡氏座標系(Cartesian Coordinate)與關節坐標系(Joint Coordinate)之間自由轉換的數學描述式，通常使用D-H表示法建立此二者的轉換矩陣。

# 一、什麼是DH法則?

- D-H(Denavit- Harenberg)於1955年在ASME發表，用以描述一連桿到下一個連桿之間的關係，再藉由齊次轉換座標描述兩座標系之間的轉換關係，可適用於任何種類的機器手臂模型，目前大部分的機器手臂座標轉換推導都採取此方法，如下圖所示。
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image.png)
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%201.png)
    

# 二、機器人正運動學

- 正向運動學(Forward Kinematics)指的是利用機械手臂各關節所轉動的角度，去推導出其末端點在卡式座標上的位置(Position)及姿態(Posture)。智慧機器人機構尺寸及各關節伺服馬達旋轉角度，定義如下圖所示。
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%202.png)
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%203.png)
    
- 透過上述介紹的齊次座標轉換方程式與D-H表示法，可以建立D-H表格並推導出手臂的正向運動學，如下圖所示。
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%204.png)
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%205.png)
    

# 三、機器人逆運動學

- 逆向運動學(Inverse Kinematics)，利用末端點卡式座標位置及姿態，計算出各關節的轉動角度值，如下圖所示。
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%206.png)
    
- 機械手臂的逆向運動學求解通常是一個複雜和非線性的問題，有許多的問題需要列入考慮，包括逆向運動學是否可以解析(解的存在性)、多重解(解的多重性)和常用的求解方法。考量到執行效率的問題，此多軸機械手臂採用「幾何解」作為逆向運動學的求解方法，如圖所示。
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%207.png)
    
    ![image.png](../assets/7%20%E6%99%BA%E6%85%A7%E6%A9%9F%E5%99%A8%E4%BA%BA/7%202%20%E6%A9%9F%E5%99%A8%E4%BA%BA%E9%81%8B%E5%8B%95%E5%AD%B8/image%208.png)