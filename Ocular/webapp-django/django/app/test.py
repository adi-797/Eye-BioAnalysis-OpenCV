myCsvRow = "last"
with open('log.csv','a') as fd:
    for i in range(5):
        fd.write(myCsvRow)
