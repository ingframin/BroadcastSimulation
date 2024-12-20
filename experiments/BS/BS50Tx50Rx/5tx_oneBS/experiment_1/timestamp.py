class TimeStamp:

    def __init__(self,usec=0,stamp=None,h=None,m=None,s=None):
        try:
            
            if stamp is not None:
                ss = stamp.split(':')
                self.days = 0
                self.hours = int(ss[0])
                self.minutes = int(ss[1])
                self.seconds = float(ss[2])
            elif h!=None and m!=None and s!=None:
                self.hours = h
                self.minutes = m
                self.seconds = s
            else:
                self.seconds = float(usec)/1E6
                self.minutes = int(self.seconds/60)
                self.hours = int(self.seconds/3600)
                self.seconds -= (self.minutes*60)
        except:
            print(stamp)
            print(usec)
            print(h)
            print(m)
            print(s)
            
            
            

    def __add__(self,ts):
        seconds = self.seconds + ts.seconds
        minutes = 0
        hours = 0
        while seconds > 60:
            minutes += 1
            seconds -= 60
            
        minutes += self.minutes-ts.minutes
        while minutes > 60:
            hours += 1
            minutes -= 60

        hours += self.hours + ts.hours
        while hours > 24:
            hours -= 24

        s = "%d:%d:%.8f"%(hours,minutes,seconds)
        return TimeStamp(h=hours,m=minutes,s=seconds)
        
    
    def __sub__(self,ts):
        
        hours = abs(self.hours -ts.hours)
        minutes = abs(self.minutes - ts.minutes)
        seconds = abs(self.seconds - ts.seconds)
        
        return TimeStamp(h=hours,m=minutes,s=seconds)

    def compareTo(self, ts):
        h = self.hours - ts.hours
        if h < 0:
            return -1
        if h > 0:
            return 1
        m = self.minutes - ts.minutes
        if m < 0:
            return -1
        if m > 0:
            return 1
        s = self.seconds - ts.seconds
        if s < 0:
            return -1
        if s > 0:
            return 1

        return 0
    def __lt__(self,ts):
        
        if self.hours < ts.hours:
            return True
        elif self.hours > ts.hours:
            return False
        
        if self.minutes < ts.minutes:
            return True
        elif self.minutes > ts.minutes:
            return False
        
        if self.seconds < ts.seconds:
            return True
        
        return False

    def __gt__(self,ts):
        return not self.__lt__(ts)

    def __eq__(self,ts):
        if self.hours == ts.hours and self.minutes == ts.minutes and self.seconds == ts.seconds:
            return True
        return False
        
        
    def __str__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)

    def __repr__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)
    
    def toSeconds(self):
        h = self.hours*3600
        m = self.minutes*60
        s = self.seconds
        return h+m+s
