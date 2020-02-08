12306车票查询
其中包含了车次获取和票价获取

可以根据出发地和目的地，分别查询全部车次信息，动车、高铁车次信息，火车车次信息

通过查找分析请求信息可以获取到四个关键url

1.12306城市代码URL:https://www.12306.cn/index/script/core/common/station_name_v10066.js

2.车次信息URL:https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT

3.列车途经站点URL:https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={0}&from_station_telecode={1}&to_station_telecode={2}&depart_date={3}

4.票价URL:https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={0}&from_station_no={1}&to_station_no={2}&seat_types={3}&train_date={4}


如果只需要查询车次信息，那么只需要城市代码URL和车次信息URL就够了

进一步获取车票价信息，则需要票价URL，其中参数则需要列车途经站点的URL

查询票价时，如爬取速度太快，则会返回错误信息。所以在这里，每次获取后都暂停5秒。


但是在prettytable这个库的运用上，还不太行，中文输出时排版不是很美观。