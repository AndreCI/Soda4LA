import os
import random
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt


def get_datetime(d, additional_format: str="") -> datetime:
    """
    :param
        d: str,
            date to convert
        additional_format: str,
            format to try
    :return:
        date: str,
            converted date
    """

    formats = ['%d/%m/%Y %H:%M:%S',
               '%d/%m/%y %H:%M:%S',
               '%H:%M:%S PM'  # 1:20:21 PM
               ]
    if additional_format != "":
        formats.insert(0, additional_format)
    for f in formats:
        try:
            date = datetime.strptime(d, f)
            if (date.year == 1900):  # years before 1970-01-02 02:00:00 or beyond 3001-01-19 07:59:59 will raise oserror
                date = date.replace(year=1986)
            return date
        except ValueError:
            pass
    raise ValueError("No format found for this timestamp {}.".format(d))


path = "sliced"

def anon_date(d1, dif, datenum = 1, splitc=";"):
    t1 = get_datetime(d1.split(splitc)[datenum]).timestamp() - dif
    return str(datetime.fromtimestamp(t1))

headeroff_2015 = "Codage;_id;actionType;creationDate;date;game_id;group_id;grpus_id;help;id;isWon;item_id;item_size;level_id;logType;message;mode_of_use;reason;resourceType;resourceTypeMoU;resource_id;resource_size;resource_title;rightsAgreements;user_id"
print(headeroff_2015)
headeroff = headeroff_2015#"id;date;logtype;actiontype;groupid;user_id;grpusid;parangon;paranon;resourcetypemou;code;message;codage_chat_message;help;resource_id;item_id;resourcetype;mode_of_use;resource_title;creationdate;rightsagreements;resource_size;item_size;reason;game_id;level_id;iswon"
i=0
for h in headeroff.split(";"):
    print("{} to {}".format(i, h))
    i+=1

#keepheadername= id;date;actiontype;groupid;user_id;resourcetypemou;help;resource_id
keepheader2015 = 1, 4, 2, 6, 24, 19, 8, 20
delheaders2015 = [0, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23]
delheaders = delheaders2015#[2, 6, 7, 8, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
delheaders.sort(reverse=True)
print(delheaders)

'''0 to id
1 to date
2 to logtype
3 to actiontype
4 to groupid
5 to user_id
6 to grpusid
7 to parangon
8 to paranon
9 to resourcetypemou
10 to code
11 to message
12 to codage_chat_message
13 to help
14 to resource_id
15 to item_id
16 to resourcetype
17 to mode_of_use
18 to resource_title
19 to creationdate
20 to rightsagreements
21 to resource_size
22 to item_size
23 to reason
24 to game_id
25 to level_id
26 to iswon'''

def anon(path, f):
    datecol = 4#1
    newf = f.split("_")
    print(newf)
    del newf[1]
    newf = ("_".join(newf))
    with open(os.path.join(path, f), "r") as f1:
        d1 = f1.readlines()
        print(d1[datecol])
        f1_timestamp = get_datetime(d1[datecol].split(",")[datecol]).timestamp()
        f2_timestamp = get_datetime("01/01/2000 00:02:00").timestamp()
        dif = abs(f1_timestamp - f2_timestamp)

        #pname = d1[1].split(";")[7]
        with open(os.path.join(path + "/annoned", f), 'w') as f:
            header = d1[0].split(",")
            for h in delheaders:
                del header[h]
            nheader = ";".join(['id', 'date', 'actiontype', 'groupid', 'user_id', 'resourcetypemou', 'help', 'resource_id\n'])
            f.write(nheader)
            for i in range(1, len(d1) - 1):
                line = d1[i].strip("\n").split(",")
                line[datecol] = anon_date(d1[i], dif, datecol, splitc=",")
                for h in delheaders:
                    del line[h]
                if(len(line) == len(header)):
                    line = [str(i), line[2], line[1], line[3], line[7], line[5], line[4], line[6]]
                    nline = ";".join(line) + "\n"
                    f.write(nline)

anon(path, "tamago_group20.csv")
exit()

for f in os.listdir(path):
    if os.path.isfile(os.path.join(path, f)):
        if "tamago" in f:
            anon(path, f)
exit()



path = "data/sequential_data/sliced"

pkeys = ["p1", "p2", "p3", "p4", "p5"]
parangons = {}
for k in pkeys:
    parangons[k] = []
for f in os.listdir(path):
    if os.path.isfile(os.path.join(path, f)):
        if "paragon" in f and False:
            nn = "tamago2014_" + f.split("_")[3] + "_" + f.split("_")[4]
            os.rename(os.path.join(path, f), os.path.join(path, nn))
        for key in parangons.keys():
            if key in f:
                parangons[key].append(f)

def combine(k1, k2, parangons, path):
    for alpha in range(len(parangons[k1])):
        for beta in range(len(parangons[k2])):
            p1 = parangons[k1][alpha]
            p2 = parangons[k2][beta]
            nfile = "tamago2014_" + k1 + "_" + p1.split("_")[2].split(".")[0] + "-" + k2 + "_" + p2.split("_")[2].split(".")[0] + ".csv"
            d1 = []
            d2 = []
            with open(os.path.join(path, p1), "r") as f1:
                d1 = f1.readlines()
            with open(os.path.join(path, p2), "r") as f2:
                d2 = f2.readlines()

            print(d1)
            f1_timestamp = get_datetime(d1[1].split(";")[1]).timestamp()
            f2_timestamp = get_datetime(d2[1].split(";")[1]).timestamp()
            dif = abs(f1_timestamp-f2_timestamp)
            # print(datetime.fromtimestamp(f1_timestamp))
            # print(datetime.fromtimestamp(f1_timestamp - dif))
            # print(datetime.fromtimestamp(f2_timestamp))
            # print(datetime.fromtimestamp(f2_timestamp - dif))

            dif1 = dif if f1_timestamp > f2_timestamp else 0
            dif2 = dif if f2_timestamp > f1_timestamp else 0
            times1=[]
            times2=[]
            i = 1
            j = 1
            print(d2)

            # print(datetime.fromtimestamp(f1_timestamp))
            # print(datetime.fromtimestamp(f1_timestamp - dif1))
            # print(datetime.fromtimestamp(f2_timestamp))
            # print(datetime.fromtimestamp(f2_timestamp - dif2))
            # print(f1_timestamp - dif1)
            # print(f2_timestamp - dif2)
            with open(os.path.join(path + "/combined", nfile), 'w') as f:
                f.write(d1[0])
                while(i < len(d1)-1 or j < len(d2)-1):
                    t1 = get_datetime(d1[i].split(";")[1]).timestamp() - dif1
                    t2 = get_datetime(d2[j].split(";")[1]).timestamp() - dif2
                    if(t1<=t2 and i < len(d1)-1 or j >= len(d2) - 1):
                        line = d1[i].split(";")
                        line[1] = str(datetime.fromtimestamp(t1))
                        f.write(";".join(line))
                        i+=1
                    elif j < len(d2)-1:
                        line = d2[j].split(";")
                        line[1] = str(datetime.fromtimestamp(t2))
                        f.write(";".join(line))
                        j+=1
                    else:
                        print("ERROR")
                        print("{} to {} / {} to {} ({} - {})".format(t1, t2, i, j, len(d1), len(d2)))

                        exit()
                    print("{} to {} / {} to {} ({} - {})".format(t1, t2, i, j, len(d1), len(d2)))

                for i in range(1, len(d1)):
                    #for j in range(1, len(d2)):
                    t = datetime.fromtimestamp(get_datetime(d1[i].split(";")[1]).timestamp() - dif1)
                    times1.append(t)
                for j in range(1, len(d2)):
                    t = datetime.fromtimestamp(get_datetime(d2[j].split(";")[1]).timestamp() - dif2)
                    times2.append(t)

            # fig, ax = plt.subplots(1)
            # fig.autofmt_xdate()
            # plt.plot(times1, range(len(times1)))
            # plt.plot(times2, range(len(times2)))
            # plt.show()

for i, k in enumerate(pkeys):
    for j in range(i+1, len(pkeys)):
        combine(k, pkeys[j], parangons, path)