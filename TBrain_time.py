import os
import sys, getopt
#  pathProg = 'C:\\Users\\gugu\\Desktop'
#  os.chdir(pathProg)
import pandas as pd
empty = object()

def list_time_calculate(filename='D:\\TBrain_time.csv', date1=20170406, date2=20170428, output=empty, timemerge='m'):
    """"list_time_calculate
   
    Note:
        Output default is object(). Without entering the output value the result will print on the screen. 
        
    Args:
        filename(str): location of reading data
        date1 (int): start date
        date2 (int): end date
        output (str): location of storing data
        timemerge(str): data merge by  year , month or day
        
    Returns:
        member's usage time 

    """
    cd = os.path.dirname(os.path.abspath(__file__))#path
    data = pd.read_csv(os.path.join(cd, filename), index_col=0) #  read data
    data.columns = ['account', 'date', 'time']

    data.date = pd.DatetimeIndex(data.date).normalize()#  show the date without time
    #  print(data['date'])
    data['year'], data['month'], data['day'] = data['date'].dt.year, data['date'].dt.month, data['date'].dt.day

    #  data['time'] = data['time'].str.replace('\d+', '')#  remove number
    data['time'] = data['time'].map(lambda x: str(x)[:-3])#  delete Chinese
    #  print(data['time'])
    data['time'] = data['time'].astype(int)
    #  print(data)

    table = []

    for i in range(len(data['account'].value_counts())):
        k = data['account'].value_counts().index[i]
        new = data[data["account"] == k]
        a = pd.to_datetime(date1, format='%Y%m%d')  #  date form
        b = pd.to_datetime(date2, format='%Y%m%d')
        in_range = new.date[new["date"].isin(pd.date_range(a, b))]
        #  iloc[0] stand for no index
        #  print(k)
        #  print(in_range.value_counts() * 600)

        for j in range(len(in_range.value_counts())):
            t2 = in_range.value_counts().index[j]
            #  print(t2)
            s2 = new.loc[new.date == t2, 'time'].sum()
            #  print(k, t2.strftime('%Y-%m-%d'), s2)
            cc= (k, t2.strftime('%Y-%m-%d'), s2/3600.0)
            table = list(cc) + table # a list
    #  print(table)
    temp = zip(*(iter(table),) * 3) #  three items as a group
    #  print zip(*(iter(table),) * 3)

    out = pd.DataFrame(temp, columns= ['Member', 'Date', 'Time(hr)'])
    #  print out
    outnew = out.sort_values(['Member', 'Date'], ascending=[True, True])#  sort dataframe

    #  print out
    outnew['Date'] = pd.to_datetime(outnew["Date"])
    outnew['Year'], outnew['Month'], outnew['Day'] = outnew['Date'].dt.year, outnew['Date'].dt.month, outnew['Date'].dt.day
    #  print outnew



    if timemerge=='y':
        t = outnew.groupby(['Member', 'Year'])['Time(hr)'].sum().reset_index(name='Time(hr)')#  group by year

    elif timemerge=='m':
        t = outnew.groupby(['Member', 'Year', 'Month'])['Time(hr)'].sum().reset_index(name='Time(hr)')#  group by month

    elif timemerge=='d':
        t = out.sort_values(['Member', 'Date'], ascending=[True, True])

    """Three options(y,m,d)
        It means data merge by year, month or day
    """

    #  print t
    if output is not empty:#  save to csv
        #  print t
        t.to_csv(output, index=False)
    else:                 #print n the screen
        t.index = map(lambda x:x+1, range(len(t.index)))
        print t

    """Two options
    If argument of output is empty, the data will show on the screen.
    If argument of output is not empty, it will save to csv to your typing location.
    """

def main(argv):
    #  print(sys.argv[1])
    import sys, getopt
    #  Store five parameters
    datapath = ''
    startdate = ''
    enddate = ''
    outfile = ''
    data_frame = ''
    #  Read command line args
    try:
        myopts, args = getopt.getopt(sys.argv[1:], "f:s:e:o:t:")
        #  print(myopts)
    except getopt.GetoptError:
        print("Usage: _filename_.py -f datapath -s startdate -e enddate -o outputfile -t timemerge")
        print("timemerge can be y(year),m(month) and d(day)")
        print("EX: TBrain_time.py -f d:/TBrain_time2.csv -s 20170407 -e 20170505 -o output.csv -t m")
        sys.exit(2)

    total = []
    #  Doing this is for complete typing arguments of function list_time_calculate.
    for i in myopts:
        total += i
    items = '-f', '-s', '-e', '-o', '-t'
    #  print total

    #  print (args)
    ###############################
    #  o == option
    #  a == argument passed to the o
    ###############################
    for o, a in myopts:
        if o == '-f':
            datapath = a
            #  print(a)
        elif o == '-s':
            startdate = a
        elif o == '-e':
            enddate = a
        elif o == '-o':
            outfile = a
        elif o == '-t':
            data_frame = a
            #  print(a)

    """Three options
    If types exact four arguments and no 'o' argument, show the result on the screen. 
    If types arguments less than five, it will tell us error.
    If types exact five arguments, save to csv.
    """
    if (len(myopts)==4) and (('-o' not in total)==True):
        list_time_calculate(filename=datapath, date1=startdate, date2=enddate, timemerge=data_frame)

    elif len(myopts) < 5:
        print("Usage: _filename_.py -f datapath -s startdate -e enddate -o outputfile -t timemerge")
        print("timemerge can be y(year),m(month) and d(day)")
        print("EX: TBrain_time.py -f d:/TBrain_time2.csv -s 20170407 -e 20170505 -o output.csv -t m")
        sys.exit(2)

    elif all(i in total for i in items):
        list_time_calculate(datapath, startdate, enddate, outfile, data_frame)




if __name__ == "__main__":
    main(sys.argv[1:])
