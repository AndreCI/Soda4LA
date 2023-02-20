

file = "Tamagocours"
data = []
grps = {}
grps2 = {}
focus = 24
writegroup="20"
blockid = []
def sorter(s):
    if(s.split("\n")[0].isnumeric()):
        return int(s.split("\n")[0])
    else:
        return -1
with open("tamago_group"+writegroup+".csv", "w") as f2:
    with open(file+'.csv') as f:
        for line in f.readlines():
            data.append(line.split(","))
            if(len(data)==1):
                f2.write(",".join(data[0]))
            line = line.split(",")
            userid = sorter(line[24])
            grpid = line[6]
            if(not userid in grps2):
                grps2[userid] = 1
            else:
                grps2[userid] += 1
            if(grpid.isnumeric()):
                if(grpid not in grps):
                    grps[grpid] = {}
                if(str(userid) not in grps[grpid]):
                    grps[grpid][str(userid)] = 1
                else:
                    grps[grpid][str(userid)] += 1
                if(grpid == writegroup and str(userid) not in blockid):
                    f2.write(",".join(line))
            else:
                pass #print(line)
header = data[0]

print(grps2)
listed2 = list(grps2.keys())
#listed2.sort(key=sorter)
print(listed2)
print("---------")
print(grps)
print(len(grps.keys()))
print(list(grps.keys()))
listed = list(grps.keys())
#listed.sort(key=lambda x: int(x))
print(listed)
for i, h in enumerate(header):
    print(i, h)

exit()

file = "tamago2014_paragon_sorted2"
data = []
with open(file+'.csv') as f:
    for line in f.readlines():
        data.append(line.split(";"))

header = data[0]

def sort_k(row):
    return row[0]

data.sort(key=sort_k)
print(data)
dd = {}
for d in data:
    parangon = d[7]
    if parangon not in dd:
        dd[parangon] = []
    dd[parangon].append(d)

print(dd)
for k in dd:
    print(k)
    print(len(dd[k]))
    for a in dd[k]:
        print(a[1])

for k in dd:
    with open("sliced/"+file + "_" + k + ".csv", "w") as f:
        f.write(";".join(header))
        for d in dd[k]:
            print(d)
            f.write(";".join(d))
exit()


with open("tamago2014_paragon_sorted.csv", "w") as f:
    for d in data:
        f.write(";".join(d))
