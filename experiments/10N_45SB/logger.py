import sqlite3


class Logger:
    
    def __init__(self,filename,schema):
        self.db = filename
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        with open(schema) as sf:
            sch = sf.read()
        try:
            c.execute(sch)
        except:
            print('schema already exists')
        conn.commit()

        conn.close()
        
    
    def log(self,data,table):
        '''data is a list of tuples, table is a string with the table name'''
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.executemany('INSERT INTO '+table+' VALUES ('+('?,'*len(data[0]))[:-1]+')', data)
        
        conn.commit()

        conn.close()
    
    def log_one(self,data,table):
        '''data is a list of tuples, table is a string with the table name'''
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('INSERT INTO '+table+' VALUES '+str(data))
        
        conn.commit()

        conn.close()
        
        
        
        
