import numpy as np

arr = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8",
       " 9", "10", "11", "12", "13", "14", "15", "16",
       "17", "18", "19", "20", "21", "22", "23", "24"]

rectW = 8
rectH = 3


npArr = np.array(arr)
npArr2D = np.reshape(npArr,(-1,8))

for i in range(len(npArr2D)):
    for j in range(len(npArr2D[i])):
        pMid = npArr2D[i][j]

        if (i == rectH // 2) and (j > 0) and (j < rectW-1):
            print(pMid)

print(rectH//2+1)