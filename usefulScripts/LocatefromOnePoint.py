import random
import string
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def get_address_from_coordinates(latitude, longitude, language="en"):
    """
    通过经纬度获取详细地址
    :param latitude: 纬度（浮点数，如 39.9042）
    :param longitude: 经度（浮点数，如 116.4074）
    :param language: 返回地址的语言（默认英文，中文可设置为 'zh'）
    :return: 详细地址字符串（如果失败返回错误信息）
    """

    # random user name 8 letters
    def randomword():
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(4))

    geopy.geocoders.options.default_user_agent = "my-application"
    # reverse the location (lan, lon) -> location detail
    g = Nominatim(
        user_agent=randomword(),
        proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"},
    )

    try:
        # 将经纬度组合成字符串（格式：纬度, 经度）
        coordinates = f"{latitude}, {longitude}"
        # 执行反向地理编码请求
        location = g.reverse(coordinates, language=language, exactly_one=True)

        if location:
            return location.address
        else:
            return "未找到地址信息"

    except GeocoderTimedOut:
        return "请求超时，请重试"
    except GeocoderServiceError as e:
        return f"服务错误：{str(e)}"
    except Exception as e:
        return f"未知错误：{str(e)}"


