import requests
from datetime import datetime
import json
import prettytable as pt
import time
import random

from check_ticket.city_code import get_city_code

city_dict, city_code_dict = get_city_code()
today = datetime.now().strftime("%Y-%m-%d")
seat_types = {
    "K": '1413',
    "G": 'O9MO',
    "D": 'OMO',
    "Z": '14163',
    "T": '1413'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Host': 'kyfw.12306.cn',
    'Cookie': 'JSESSIONID=648A5833BE78C4AE9233691E4F6CE215; RAIL_EXPIRATION=1577530593556; RAIL_DEVICEID=GKHGVambSz4ZgwCtUhNAnMEDsHv54o9Z-oOczHAsrRxkEk0scEIrzHF6kHE-kUCxsTLwZjmXcim5KbkN9V0UHW3XsaUR5_6XHo6BGW45HyonZHTho5wMNhJG2Xmzmj_Xts6bG5TT_6Fnua8JDjGVqUaX4E3-13qi; _jc_save_fromDate=2019-12-26; _jc_save_toDate=2019-12-25; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; BIGipServerpool_passport=367854090.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=837812746.24610.0000'
}
train_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'
price_url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={0}&from_station_no={1}&to_station_no={2}&seat_types={3}&train_date={4}'
station_list_url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={0}&from_station_telecode={1}&to_station_telecode={2}&depart_date={3}'
train_list = []


def get_user_input():
    while True:
        date = input("请输入您的出发日期(YY-mm-dd):")
        if date >= today:
            break
        else:
            print("查询日期不得早于当前日期，请重新输入")

    while True:
        departure = input("请输入您的出发地:")
        if departure in city_dict.keys():
            break
        else:
            print("输入错误，请重新输入")

    while True:
        destination = input("请输入您的到达地:")
        if destination in city_dict.keys():
            break
        else:
            print("输入错误，请重新输入")

    while True:
        print("1.全部     2.高铁、动车     3.火车")
        train_type = input("请输入要查询类型对应编号:")
        if train_type == "1" or train_type == "2" or train_type == "3":
            break
        else:
            print("输入错误，请重新输入")

    print("您将查询{0},{1} 至 {2}的 {3}类型 车次，请稍等...".format(date, departure, destination, train_type))
    return date, departure, destination, train_type


def search_train(date_time, from_station, to_station, train_type):
    departure_code = city_dict[from_station].upper()
    destination_code = city_dict[to_station].upper()
    url = train_url.format(date_time, departure_code, destination_code)

    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    for result in response_json['data']['result']:
        train_dict = {
            'train_status': '',
            'train_no': '',
            'train_number': '',
            'departure': '',
            'destination': '',
            'start_city': '',
            'arrive_city': '',
            'departure_time': '',
            'destination_time': '',
            'take_time': '',
            'business_class': '',
            'first_class': '',
            'second_class': '',
            'soft_sleeper': '',
            'hard_sleeper': '',
            'hard_seat': '',
            'without_seat': ''
        }
        result_list = result.split('|')
        train_dict['train_status'] = result_list[1]
        train_dict['train_no'] = result_list[2]
        train_dict['train_number'] = result_list[3]
        train_dict['departure'] = city_code_dict[result_list[4]]
        train_dict['destination'] = city_code_dict[result_list[5]]
        train_dict['start_station'] = city_code_dict[result_list[6]]
        train_dict['arrive_station'] = city_code_dict[result_list[7]]
        train_dict['departure_time'] = result_list[8]
        train_dict['destination_time'] = result_list[9]
        train_dict['take_time'] = result_list[10]
        train_dict['business_class'] = result_list[32]
        train_dict['first_class'] = result_list[31]
        train_dict['second_class'] = result_list[30]
        train_dict['soft_sleeper'] = result_list[23]
        train_dict['hard_sleeper'] = result_list[28]
        train_dict['hard_seat'] = result_list[29]
        train_dict['without_seat'] = result_list[26]

        if train_type == '1':
            train_list.append(train_dict)
        if train_type == '2':
            if train_dict['train_number'][0] == 'D' or train_dict['train_number'][0] == 'G':
                train_list.append(train_dict)
        if train_type == '3':
            if train_dict['train_number'][0] != 'D' and train_dict['train_number'][0] != 'G':
                train_list.append(train_dict)

    return train_list


def search_station_list(train_no, start_station, arrive_station, date_time):
    from_station_no = ""
    to_station_no = ""
    start_station_code = city_dict[start_station].upper()
    arrive_station_code = city_dict[arrive_station].upper()
    url = station_list_url.format(train_no, start_station_code, arrive_station_code, date_time)

    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    for each_station in response_json['data']['data']:
        if each_station['station_name'] == start_station:
            from_station_no = each_station['station_no']
        elif each_station['station_name'] == arrive_station:
            to_station_no = each_station['station_no']
    return from_station_no, to_station_no


def search_price(date_time, trainlist):
    for train in trainlist:
        train_no = train['train_no']
        start_station = train['start_station']
        arrive_station = train['arrive_station']
        from_station_no, to_station_no = search_station_list(train_no, start_station, arrive_station, date_time)
        train_type = train['train_number'][0]
        seat_type = seat_types[train_type]

        url = price_url.format(train_no, from_station_no, to_station_no, seat_type, date_time)
        while True:
            response = requests.get(url, headers=headers)
            if '"httpstatus":200' in response.text:
                print(response.text)
                time.sleep(5)
                break
            else:
                time.sleep(10)
                continue


def print_train_list(trainlist):
    tb = pt.PrettyTable()
    tb.field_names = ["车次状态", "车次", "始发站", "末尾站", "出发站", "到达站", "发车时间", "预计到达时间", "历时", "商务座", "一等座", "二等座", "软卧", "硬卧",
                      "硬座", "无座"]
    tb.align = 'c'
    tb.padding_width = 1
    for train in trainlist:
        tb.add_row([train['train_status'], train['train_number'], train['departure'], train['destination'],
                    train['start_station'], train['arrive_station'], train['departure_time'],
                    train['destination_time'], train['take_time'], train['business_class'], train['first_class'],
                    train['second_class'], train['soft_sleeper'], train['hard_sleeper'], train['hard_seat'],
                    train['without_seat']])
    return tb


if __name__ == '__main__':
    date, departure, destination, train_type = get_user_input()
    train_list = search_train(date, departure, destination, train_type)
    table = print_train_list(train_list)
    print(table)
    # search_price(date, train_list)

