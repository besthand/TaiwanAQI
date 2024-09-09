from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN

# 整合後的縣市與測站名稱
CITY_STATION_OPTIONS = {
    "屏東縣-屏東(枋山)": "屏東(枋山)",
    "臺中市-大甲（日南國小）": "大甲（日南國小）",
    "新北市-新北(樹林)": "新北(樹林)",
    "屏東縣-屏東（琉球）": "屏東（琉球）",
    "臺南市-臺南（麻豆）": "臺南（麻豆）",
    "高雄市-高雄（湖內）": "高雄（湖內）",
    "彰化縣-彰化（員林）": "彰化（員林）",
    "彰化縣-大城": "大城",
    "新北市-富貴角": "富貴角",
    "雲林縣-麥寮": "麥寮",
    "臺東縣-關山": "關山",
    "澎湖縣-馬公": "馬公",
    "金門縣-金門": "金門",
    "連江縣-馬祖": "馬祖",
    "南投縣-埔里": "埔里",
    "高雄市-復興": "復興",
    "新北市-永和": "永和",
    "南投縣-竹山": "竹山",
    "桃園市-中壢": "中壢",
    "新北市-三重": "三重",
    "宜蘭縣-冬山": "冬山",
    "臺北市-陽明": "陽明",
    "花蓮縣-花蓮": "花蓮",
    "臺東縣-臺東": "臺東",
    "屏東縣-恆春": "恆春",
    "屏東縣-潮州": "潮州",
    "屏東縣-屏東": "屏東",
    "高雄市-小港": "小港",
    "高雄市-前鎮": "前鎮",
    "高雄市-前金": "前金",
    "高雄市-左營": "左營",
    "高雄市-楠梓": "楠梓",
    "高雄市-林園": "林園",
    "高雄市-大寮": "大寮",
    "高雄市-鳳山": "鳳山",
    "高雄市-仁武": "仁武",
    "高雄市-橋頭": "橋頭",
    "高雄市-美濃": "美濃",
    "臺南市-臺南": "臺南",
    "臺南市-安南": "安南",
    "臺南市-善化": "善化",
    "臺南市-新營": "新營",
    "嘉義市-嘉義": "嘉義",
    "雲林縣-臺西": "臺西",
    "嘉義縣-朴子": "朴子",
    "嘉義縣-新港": "新港",
    "雲林縣-崙背": "崙背",
    "雲林縣-斗六": "斗六",
    "南投縣-南投": "南投",
    "彰化縣-二林": "二林",
    "彰化縣-線西": "線西",
    "彰化縣-彰化": "彰化",
    "臺中市-西屯": "西屯",
    "臺中市-忠明": "忠明",
    "臺中市-大里": "大里",
    "臺中市-沙鹿": "沙鹿",
    "臺中市-豐原": "豐原",
    "苗栗縣-三義": "三義",
    "苗栗縣-苗栗": "苗栗",
    "苗栗縣-頭份": "頭份",
    "新竹市-新竹": "新竹",
    "新竹縣-竹東": "竹東",
    "新竹縣-湖口": "湖口",
    "桃園市-龍潭": "龍潭",
    "桃園市-平鎮": "平鎮",
    "桃園市-觀音": "觀音",
    "桃園市-大園": "大園",
    "桃園市-桃園": "桃園",
    "臺北市-大同": "大同",
    "臺北市-松山": "松山",
    "臺北市-古亭": "古亭",
    "臺北市-萬華": "萬華",
    "臺北市-中山": "中山",
    "臺北市-士林": "士林",
    "新北市-淡水": "淡水",
    "新北市-林口": "林口",
    "新北市-菜寮": "菜寮",
    "新北市-新莊": "新莊",
    "新北市-板橋": "板橋",
    "新北市-土城": "土城",
    "新北市-新店": "新店",
    "新北市-萬里": "萬里",
    "新北市-汐止": "汐止",
    "基隆市-基隆": "基隆"
}


class TaiwanAQIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Taiwan AQI."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # 當使用者輸入 API Key 和選擇了測站後，將測站名稱和 API Key 存入 config_entry
            selected_station = CITY_STATION_OPTIONS[user_input["station"]]  # 取得實際存檔的測站名稱
            api_key = user_input["api_key"]
            return self.async_create_entry(
                title=selected_station, 
                data={"station": selected_station, "api_key": api_key}
            )

        # 顯示縣市-測站選項和 API Key 輸入框
        schema = vol.Schema({
            vol.Required("api_key"): str,  # 請使用者輸入 API Key
            vol.Required("station"): vol.In(list(CITY_STATION_OPTIONS.keys()))  # 讓使用者選擇測站
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @callback
    def async_get_options_flow(self, config_entry):
        """Return the options flow handler."""
        return TaiwanAQIOptionsFlowHandler(config_entry)


class TaiwanAQIOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Taiwan AQI options."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # 可以根據需求設置選項邏輯，例如修改測站或其他配置
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))