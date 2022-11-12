import pandas as pd
import xlsxwriter

#mengiport tabel training data
dataMain = pd.ExcelFile("traintest.xlsx")
dataTrain = pd.read_excel(dataMain, 'train')
dataTest = pd.read_excel(dataMain, 'test')

idTrain = dataTrain["id"]
x1Train = dataTrain["x1"]
x2Train = dataTrain["x2"]
x3Train = dataTrain["x3"]
yTrain = dataTrain["y"]

idTest = dataTest["id"]
x1Test = dataTest["x1"]
x2Test = dataTest["x2"]
x3Test = dataTest["x3"]
yTest = dataTest["y"]

#data knn
arrSebagian = []
arrayAll = []
arrayIdTest = []
arrHasilY = []
nilaiK = 13

#data evaluasi
arrTrain = [] #data yang dibagi 75 persen dari actual train
arrTest = [] #data yang dibgai 25 persen dari actual train
arrAllEvaluasi = [] #data yang memiliki jarak antar train dan test
arrIdTestEvaluasi = []
arrHalfEvaluasi = []
hasilSalahEval = 0


#menghitung jarak
def hitungJarak(x):
    for i in range(10): #perulangan pada data test
        for j in range(296): #perulangan pada data train
            if x == idTest[i]: #cek apakah x sama dengan data ke idTest[i] jika sama maka akan melakukan aksi
                rumus = (((x1Test[i]-x1Train[j])**2) + ((x2Test[i]-x2Train[j])**2) + ((x3Test[i]-x3Train[j])**2)**1/2)
                hasil = {
                "id test" : idTest[i],
                "x1 train" : x1Train[j],
                "x2 train" : x2Train[j],
                "x3 train" : x3Train[j],
                "y train" : yTrain[j],
                "jarak" : rumus
                }
                arrayAll.append(hasil)

def sort(data):
    hasil = sorted(data, key=lambda x: x["jarak"])
    return hasil

def nearestNeighbour(k, arrJarak, arrAllData):
    hasil1 = 0
    hasil0 = 0
    for i in range(k):
        hasil = arrAllData[i]
        arrJarak.append(hasil)
    for i in range(k):
        if arrJarak[i]["y train"] == 0:
            hasil0 = hasil0 + 1
        else:
            hasil1 = hasil1 + 1

    if hasil1 > hasil0:
        return 1
    else:
        return 0


#algoritma evaluasi
nDataTrain = int((75/100) * 296) #222
nDataTest = int((25/100) * 296)  #74

def splitData():
    for i in range(0,nDataTrain):
        hasilTrain = {
            "id train": idTrain[i],
            "x1 train": x1Train[i],
            "x2 train": x2Train[i],
            "x3 train": x3Train[i],
            "y train": yTrain[i],
        }
        arrTrain.append(hasilTrain)

    for j in range(nDataTrain,222+nDataTest):
        hasilTest = {
            "id test": idTrain[j],
            "x1 test": x1Train[j],
            "x2 test": x2Train[j],
            "x3 test": x3Train[j],
            "y test": yTrain[j],
        }
        arrTest.append(hasilTest)


def hitungJarakEvaluasi(x):
    for i in range(nDataTest):
        for j in range(nDataTrain):
            if x == arrTest[i]["id test"]:
                rumus = (((arrTrain[j]["x1 train"]-arrTest[i]["x1 test"])**2) + ((arrTrain[j]["x2 train"]-arrTest[i]["x2 test"])**2) + ((arrTrain[j]["x3 train"]-arrTest[i]["x3 test"])**2)**1/2)
                hasil = {
                    "iterasi" : j+1,
                    "id test" : arrTest[i]["id test"],
                    "x1 train" : arrTrain[j]["x1 train"],
                    "x2 train" : arrTrain[j]["x2 train"],
                    "x3 train" : arrTrain[j]["x3 train"],
                    "y train" : arrTrain[j]["y train"],
                    "jarak" : rumus
                }
                arrAllEvaluasi.append(hasil)

#MAIN EVALUASI
splitData() #mengisi data pemisalah
for i in range(74): #untuk memasukkan id data test untuk perulangan nantinya
    arrIdTestEvaluasi.append(arrTest[i]["id test"])

for i in arrIdTestEvaluasi:
    hitungJarakEvaluasi(i)
    arrAllEvaluasi = sort(arrAllEvaluasi)
    hasil = nearestNeighbour(nilaiK, arrHalfEvaluasi, arrAllEvaluasi)
    for j in range(74):
        if arrTest[j]["id test"] == arrHalfEvaluasi[1]["id test"]:
            if hasil != arrTest[j]["y test"]:
                hasilSalahEval += 1
    arrAllEvaluasi = []
    arrHalfEvaluasi = []

accuracy = ((nDataTest-hasilSalahEval)/nDataTest) * 100
hasilAkhir = round(accuracy,2)
print("{} %".format(hasilAkhir))

#MAIN KNN
for i in range(10):
    arrayIdTest.append(idTest[i])

for i in arrayIdTest:
    hitungJarak(i)
    arrayAll = sort(arrayAll)
    hasil = nearestNeighbour(nilaiK, arrSebagian, arrayAll)
    arrHasilY.append(hasil)

    # array dikosongkan lagi untuk data selanjutnya
    arrSebagian = []
    arrayAll = []

#prose output
rawData = []
for i in range(10):
    hasil = {
        "id": idTest[i],
        "x1": x1Test[i],
        "x2": x2Test[i],
        "x3": x3Test[i],
        "y": arrHasilY[i],
    }
    rawData.append(hasil)

df = pd.DataFrame(rawData)
df.to_excel("output.xlsx")