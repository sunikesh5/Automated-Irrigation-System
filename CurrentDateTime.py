import utime

class CurrentDateTime:

    #######################
    ### aktuelles Datum ###
    #######################
    def getCurrentDateTime(self):
        year = utime.localtime()[0]
        month = utime.localtime()[1]
        day = utime.localtime()[2]
        hour = utime.localtime()[3]
        minute = utime.localtime()[4]
        second = utime.localtime()[5]
        currentDateTime = "{}-{}-{}, {}:{}:{}"
        return currentDateTime.format(year,month,day,hour,minute,second)