




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
