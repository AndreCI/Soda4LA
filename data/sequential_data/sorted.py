
data = []
with open("tamago2014_sono_sorted.csv") as f:
    for line in f.readlines():
        data.append(line.split(";"))

def sort_k(row):
    return row[0]

data.sort(key=sort_k)
print(data)

with open("tamago2014_paragon_sorted.csv", "w") as f:
    for d in data:
        f.write(";".join(d))
