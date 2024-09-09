# Taiwan AQI - Home Assistant 自訂整合

這個 Home Assistant 的自訂整合可以讓你監控台灣各地的空氣品質資料，並提供即時的 AQI（空氣品質指標）數據。此整合會從台灣的各個監測站擷取資料，並且為每個空氣品質指標（如 PM2.5、PM10、O3、NO2、SO2、CO 以及 AQI）建立獨立的感測器實體。此外，它還支援透過 Home Assistant 服務手動更新 AQI 資料。

## 功能
- 擷取中華民國環境部各監測站的空氣品質資料。
- 提供以下獨立的感測器實體：
  - AQI（空氣品質指數）
  - PM2.5（細懸浮微粒）
  - PM10（懸浮微粒）
  - O3（臭氧）
  - NO2（二氧化氮）
  - SO2（二氧化硫）
  - CO（一氧化碳）
- 支援協調器進行的定期更新，更新間隔可配置。
- 提供 Home Assistant 服務，手動更新所有 AQI 感測器資料。
- 顯示額外屬性（如測站名稱和上次更新時間），提供更好的上下文資訊。

## 安裝

### 手動安裝
1. 下載此專案，並將 `taiwan_aqi` 資料夾放置到 Home Assistant 的 `custom_components` 資料夾中。
2. 重啟 Home Assistant。

### 設定
1. 在 Home Assistant 中，導航至 **設定** > **設備與服務** > **新增整合**。
2. 搜尋 **Taiwan AQI**，並按照螢幕上的指示進行設定。
3. 你需要提供：
   - **API 金鑰**：存取空氣品質資料的 API 金鑰。
   - **監測站**：選擇你想要監控的台灣空氣品質監測站。

## 使用方式
- 安裝完成後，你將會看到各個空氣品質指標的感測器實體。

## Lovelace 卡片範例

```yaml
type: entities
entities:
  - entity: sensor.aqi_sensor
  - entity: sensor.pm2_5_sensor
  - entity: sensor.pm10_sensor
  - entity: sensor.o3_sensor
  - entity: sensor.no2_sensor
  - entity: sensor.so2_sensor
  - entity: sensor.co_sensor
title: 台灣 AQI
```

## 貢獻
歡迎 fork 此專案、提交問題、並建立 pull requests。任何貢獻都十分歡迎！

## 授權
此專案採用 MIT 授權條款。

---

# Taiwan AQI - Home Assistant Integration

This custom integration for [Home Assistant](https://www.home-assistant.io/) allows you to monitor air quality from various stations in Taiwan. It fetches real-time AQI (Air Quality Index) data and provides individual sensor entities for key air quality indicators such as PM2.5, PM10, O3, NO2, SO2, CO, and AQI. Additionally, it supports manual updates through a Home Assistant service.

## Features
- Fetches air quality data for selected stations across Taiwan.
- Provides separate sensor entities for:
  - AQI (Air Quality Index)
  - PM2.5 (Fine Particulate Matter)
  - PM10 (Particulate Matter)
  - O3 (Ozone)
  - NO2 (Nitrogen Dioxide)
  - SO2 (Sulfur Dioxide)
  - CO (Carbon Monoxide)
- Supports periodic updates through a coordinator with a configurable interval.
- Includes a service to manually update AQI data across all sensors.
- Displays additional attributes such as the station name and last update time for better context.

## Installation

### Manual Installation
1. Download the repository and place the `taiwan_aqi` folder inside your Home Assistant `custom_components` directory.
2. Restart Home Assistant.

### Configuration
1. In Home Assistant, navigate to **Configuration** > **Devices & Services** > **Add Integration**.
2. Search for **Taiwan AQI** and follow the on-screen instructions.
3. You will need to provide:
   - **API Key**: An API key to access the air quality data.
   - **Monitoring Station**: Select your preferred air quality monitoring station in Taiwan.

## Usage
- After installation, you will see sensor entities created for each air quality indicator.

## Example Lovelace Card

```yaml
type: entities
entities:
  - entity: sensor.aqi_sensor
  - entity: sensor.pm2_5_sensor
  - entity: sensor.pm10_sensor
  - entity: sensor.o3_sensor
  - entity: sensor.no2_sensor
  - entity: sensor.so2_sensor
  - entity: sensor.co_sensor
title: Taiwan AQI
```

## Contributions
Feel free to fork this project, submit issues, and create pull requests. Contributions are welcome!

## License
This project is licensed under the MIT License.
