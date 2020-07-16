import re

msg = "labtek v rusak"
gdg_kuliah = ['labtek','lfm', 'oktagon', 'tvst', 'gku', 'gku barat', 'gku timur', 'labtek v', 'labtek 5', 'labtek vi', 'labtek 6', 'labtek i', 'labtek 1', 'bsc', 'gedung doping', 'doping', 'crcs', 'cas', 'cadl']
a = ["0"]
for i in range(len(gdg_kuliah)):
    x = re.search(gdg_kuliah[i], msg)
    if x == None:
        pass
    else:
        a[0] = (gdg_kuliah[i])
print(a[0])
