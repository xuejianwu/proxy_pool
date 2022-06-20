from datetime import datetime, date, timedelta


def getDatetimeToday():

    t = date.today() #date类型

    dt = datetime.strptime(str(t),'%Y-%m-%d') #date转str再转datetime

    return dt


def getDatetimeYesterday():

        today = getDatetimeToday() #datetime类型当前日期

        yesterday = today + timedelta(days = -1) #减去一天
        yesterday = yesterday.strftime("%Y-%m-%d").split(("-"))


        if len(yesterday[1]) == 2:
            if yesterday[1][0] == "0":
                yesterday[1] = yesterday[1][1]
        if len(yesterday[2]) == 2:
            if yesterday[2][0] == "0":
                yesterday[2] = yesterday[2][1]
        yesterday = "-".join(yesterday)

        return yesterday


if __name__ == '__main__':
    print(getDatetimeYesterday())