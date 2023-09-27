from datetime import datetime, timedelta


class DS3231:
    
    def __init__(self):
        self.base_time = datetime.now()
        self.time_offset = timedelta(seconds=0)
        
    # get times functions -------------------------------------------------------------------------------------------------------
    
    def getYear(self):
        raise NotImplemented()
    
    def getMonth(self):
        raise NotImplemented()
    
    def getDay(self):
        raise NotImplemented()
            
    def getDayOfWeek(self):
        raise NotImplemented()
    
    def getHour(self):
        raise NotImplemented()
    
    def getMinutes(self):
        raise NotImplemented()
    
    def getSeconds(self):
        raise NotImplemented()
    
    def getDateTime(self): 
        dateTime = [0, 0, 0, 0, 0, 0, 0]
        current_time = datetime.now() - self.time_offset

        dateTime[0] = current_time.year
        dateTime[1] = current_time.month
        dateTime[2] = current_time.day
        dateTime[3] = current_time.weekday() 
        dateTime[4] = current_time.hour
        dateTime[5] = current_time.minute
        dateTime[6] = current_time.second

        return dateTime
    
    # set times functions -------------------------------------------------------------------------------------------------------
    
    def setYear(self, year): 
        raise NotImplemented()
        
    def setMonth(self, month):
        raise NotImplemented()
    
    def setDay(self, day):
        raise NotImplemented()
    
    def setDayOfWeek(self, dayOfWeek):
        raise NotImplemented()
        
    def setHour(self, hour):
        raise NotImplemented()
        
    def setMinutes(self, minutes):
        raise NotImplemented()
    
    def setSeconds(self, seconds):
        raise NotImplemented()
        
    def setDateTime(self, year, month, day, dayOfWeek, hour, minutes, seconds): 
        # set all the date and times (year is last two digits of year)
        self.base_time = datetime(year, month, day, hour, minutes, seconds)
        self.time_offset = datetime.now() - self.base_time

    def setCurrentTimeFromRTC(self):
        self.time_offset = timedelta(seconds=0)

    def setCurrentTimeToRTC(self):
        self.time_offset = timedelta(seconds=0)
        
    # get alarm functions ------------------------------------------------------------------------------------------------------
    
    def getAlarm1(self): 
        raise NotImplemented()
        
    def getAlarm2(self): 
        raise NotImplemented()
    
    def alarmTriggert(self, alarmNumber):
        raise NotImplemented()
        
    # set alarm functions -------------------------------------------------------------------------------------------------------
    
    def setAlarm1(self, day, hour, minutes, seconds = 0, alarmType = "everyDay"):
        raise NotImplemented()
        
    def setAlarm2(self, day, hour, minutes, alarmType = "everyDay"): 
        raise NotImplemented()
        
    def turnOnAlarmIR(self, alarmNumber):
        raise NotImplemented()
    
    def turnOffAlarmIR(self, alarmNumber):
        raise NotImplemented()
    
    def resetAlarmFlag(self, alarmNumber):
        raise NotImplemented()
        
