print("Hello World")

treeLength = 500
for i in range(treeLength):
    if (i < (10/100)*treeLength):
        print("leaf")
    elif (i > (90/100)*treeLength):
        print("stump")
    else:
        print("neck")