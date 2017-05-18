import os
import sys, getopt
#pathProg = 'C:\\Users\\gugu\\Desktop'
#os.chdir(pathProg)
import pandas as pd
empty = object()

def list_time_calculate(filename='D:\\TBrain_time.csv', date1=20170406, date2=20170428, output=empty, timemerge='m'):
    cd = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(os.path.join(cd, filename), index_col=0)
    data.columns = ['account', 'date', 'time']

    data.date = pd.DatetimeIndex(data.date).normalize()
    # print(data['date'])
    data['year'], data['month'], data['day'] = data['date'].dt.year, data['date'].dt.month, data['date'].dt.day

    # data['time'] = data['time'].str.replace('\d+', '')#remove number
    data['time'] = data['time'].map(lambda x: str(x)[:-3])
    # print(data['time'])
    data['time'] = data['time'].astype(int)
    # print(data)

    table = []

    for i in range(len(data['account'].value_counts())):
        k = data['account'].value_counts().index[i]
        new = data[data["account"] == k]
        a = pd.to_datetime(date1, format='%Y%m%d')  # date form
        b = pd.to_datetime(date2, format='%Y%m%d')
        in_range = new.date[new["date"].isin(pd.date_range(a, b))]  # iloc[0] stand for no index
        #print(k)
        # print(in_range.value_counts() * 600)

        for j in range(len(in_range.value_counts())):
            t2 = in_range.value_counts().index[j]
            #print(t2)
            s2 = new.loc[new.date == t2, 'time'].sum()
            #print(k, t2.strftime('%Y-%m-%d'), s2)
            cc= (k, t2.strftime('%Y-%m-%d'), s2/600.0)
            table = list(cc) + table
    headers = ['Member', 'Date', 'Time']
    #print(table)
    temp = zip(*(iter(table),) * 3) # three items as a group
    #print zip(*(iter(table),) * 3)

    out = pd.DataFrame(temp, columns= ['Member', 'Date', 'Time(hr)'])
    #print out
    outnew = out.sort_values(['Member', 'Date'], ascending=[True, True])

    #print out
    outnew['Date'] = pd.to_datetime(outnew["Date"])
    outnew['year'], outnew['month'], outnew['day'] = outnew['Date'].dt.year, outnew['Date'].dt.month, outnew['Date'].dt.day
    #print outnew
    if timemerge=='y':
        t = outnew.groupby(['Member', 'year'])['Time(hr)'].sum().reset_index(name='Time(hr)')

    elif timemerge=='m':
        t = outnew.groupby(['Member', 'year', 'month'])['Time(hr)'].sum().reset_index(name='Time(hr)')

    elif timemerge=='d':
        t = out.sort_values(['Member', 'Date'], ascending=[True, True])


    #print t
    if output is not empty:
        #print t
        t.to_csv(output, index=False)
    else:
        t.index = map(lambda x:x+1, range(len(t.index)))
        print t


def main(argv):
    #print(sys.argv[1])
    import sys, getopt
    # Store input and output file names
    datapath = ''
    startdate = ''
    enddate = ''
    outfile = ''
    data_frame = ''
    # Read command line args
    try:
        myopts, args = getopt.getopt(sys.argv[1:], "f:s:e:o:t:")
        #print(myopts)
    except getopt.GetoptError:
        print("Usage: _filename_.py -f datapath -s startdate -e enddate -o outputfile -t timemerge")
        print("timemerge can be y(year),m(month) and d(day)")
        print("EX: TBrain_time.py -f d:/TBrain_time2.csv -s 20170407 -e 20170505 -o output.csv -t m")
        sys.exit(2)

    total = []
    for i in myopts:
        total += i
    items = '-f', '-s', '-e', '-o', '-t'
    #print total

    #print (args)
    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in myopts:
        if o == '-f':
            datapath = a
            #print(a)
        elif o == '-s':
            startdate = a
        elif o == '-e':
            enddate = a
        elif o == '-o':
            outfile = a
        elif o == '-t':
            data_frame = a
            #print(a)

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
