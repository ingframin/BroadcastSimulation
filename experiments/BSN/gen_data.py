from secrets import token_bytes

with open('data.bin','wb') as df:
    x = token_bytes(10485760)
    df.write(x)
    
        
        