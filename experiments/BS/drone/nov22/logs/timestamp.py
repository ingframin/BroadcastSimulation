class TimeStamp:

    def __init__(self,usec=0,stamp=None,h=-1,m=-1,s=-1):
        if stamp is not None:
            ss = stamp.split(':')
            self.days = 0
            self.hours = int(ss[0])
            self.minutes = int(ss[1])
            self.seconds = float(ss[2])
        elif h>0 and m>0 and s>0:
            self.hours = h
            self.minutes = m
            self.seconds = s
        else:
            self.seconds = usec/1E6
            self.minutes = int(self.seconds/60)
            self.hours = int(self.seconds/3600)
            self.seconds -= (self.minutes*60)
            
            
            

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
        return TimeStamp(s)
        
    
    def __sub__(self,ts):
        
        hours = abs(self.hours -ts.hours)
        minutes = abs(self.minutes - ts.minutes)
        seconds = abs(self.seconds - ts.seconds)
        s = "%d:%d:%.8f"%(hours,minutes,seconds)
        return TimeStamp(s)

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

    def __str__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)

    def __repr__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)
    
    def toSeconds(self):
        h = self.hours*3600
        m = self.minutes*60
        s = self.seconds
        return h+m+s
