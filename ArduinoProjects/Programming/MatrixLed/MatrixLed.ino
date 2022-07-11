/*****************************************************
 * MatrixLed.ino 
 * 目的:
 *  測試8*8矩陣LED功能(模擬輸送帶物品往復運動)
 * 方法:
 *  8*8矩陣LED
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察8*8矩陣LED上是否有物件往復運動變化
*****************************************************/

#include <LedControl.h> //掛載矩陣LED標頭檔

#define LED_DIN    42   //定義矩陣LED資料腳位連接至42腳
#define LED_CS     44   //定義矩陣LED致能腳位連接至44腳
#define LED_CLK    46   //定義矩陣LED時序腳位連接至46腳

//矩陣LED圖形
const uint64_t IMAGES[] = {
  0xff000001010000ff, 0xff000003030000ff, 0xff000006060000ff,
  0xff00000c0c0000ff, 0xff000018180000ff, 0xff000030300000ff,
  0xff000060600000ff, 0xff0000c0c00000ff, 0xff000080800000ff,
  0xff0000c0c00000ff, 0xff000060600000ff, 0xff000018180000ff,
  0xff00000c0c0000ff, 0xff000006060000ff, 0xff000003030000ff,
  0xff000001010000ff
};
const int IMAGES_LEN = sizeof(IMAGES)/8;

//宣告矩陣LED物件
LedControl display = LedControl(LED_DIN, LED_CLK, LED_CS);
int k = 0;


/************************* 初始設定 *********************/
void setup() 
{
  display.clearDisplay(0);      //矩陣LED畫面清除
  display.shutdown(0, false);
  display.setIntensity(0, 5);   //設定矩陣LED亮度
}

/************************* 主程式 ***********************/
void loop() 
{
  displayImage(IMAGES[k]);
  
  if (++k >= IMAGES_LEN ) 
  {
    k = 0;
  }
  
  delay(100);
}

/*********** 矩陣LED顯示函數 ****************************/
void displayImage(uint64_t image) 
{
  for (int i = 0; i < 8; i++) 
  {
    byte row = (image >> i * 8) & 0xFF;
    
    for (int j = 0; j < 8; j++) 
    {
      display.setLed(0, i, j, bitRead(row, j));
    }
  }
}
