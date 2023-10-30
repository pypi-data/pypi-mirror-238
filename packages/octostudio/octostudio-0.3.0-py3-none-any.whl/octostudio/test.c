#include <BLEDevice.h>
#include <BLEServer.h>

BLEServer* pServer = NULL;
BLEAdvertising* pAdvertising = NULL;
String deviceName = "0000000000000000";
BLEUUID serviceUUID("2540B6B0-0002-4538-BCD7-7ECFB51297C1"); // 2540b6b000024538bcd77ecfb51297c1

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE work!");

  startBLE();
}

void loop() {
  // 此处添加代码，根据需要修改 deviceName 和 serviceUUID
  // 例如，你可以通过某种触发器或条件来修改设备名称和服务UUID
  if (Serial.available()) {
    deviceName = Serial.readStringUntil('\n');
    deviceName.trim(); // 移除末尾的换行符
    startBLE(); // 重新启动BLE以应用新的设置
    Serial.println("Device name and service UUID updated!");
  }

  delay(3000);
}

void startBLE() {
  BLEDevice::deinit(false);  // 关闭BLE，保留内存数据
  BLEDevice::init(deviceName.c_str());  // 使用新的设备名称重新初始化BLE

  pServer = BLEDevice::createServer();
  pAdvertising = pServer->getAdvertising();
  pAdvertising->addServiceUUID(serviceUUID);

  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // 设置广播间隔，单位为毫秒。函数参数是以16进制表示的。
  pAdvertising->setMinPreferred(0x12);
  
  BLEDevice::startAdvertising();
  Serial.println("BLE advertising...");
}
