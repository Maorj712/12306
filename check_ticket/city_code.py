import requests
import re


def get_city_code():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    city_dict = {}
    city_code_dict = {}

    url = 'https://www.12306.cn/index/script/core/common/station_name_v10066.js'
    response = requests.get(url, headers=headers)
    mystr = response.text
    pattern = re.compile(r'@(.*?)\|(.*?)\|(.*?)\|')
    result = pattern.findall(mystr)
    for each_city in result:
        city = each_city[1]
        city_code = each_city[2]
        city_dict[city] = city_code
    for each_city_code in result:
        city = each_city_code[1]
        city_code = each_city_code[2]
        city_code_dict[city_code] = city
    return city_dict, city_code_dict




