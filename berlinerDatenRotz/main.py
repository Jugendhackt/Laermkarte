import requests, cv2, numpy, math

from PIL import Image

def getBoxData(x, y):
    r = requests.get('https://fbinter.stadt-berlin.de/fb/wms/senstadt/wmsk_07_05_01str_vbusDEN?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&CACHEID=888282&LAYERS=1&WIDTH=512&HEIGHT=512&CRS=EPSG:4326&STYLES=&BBOX={}, {}, {}, {}'.format(x, y, x+0.002, y+0.002))
    
    with open(r'image.png','wb') as f:
        f.write(r.content)

    myimg = cv2.imread('image.png')

    imgSlices = []

    for x in range(4):
        for y in range(4):
            imgSlices.append(myimg[x*128:x*128+128, y*128:y*128+128])

    for x in range(16):
        cv2.imwrite("filename{}.png".format(x), imgSlices[x])
        

    finalSize = 16
    # 128 pixels each

    resultArray = []


    for i in range(16):
        count = {}
        for x in imgSlices[i]:
            for y in x:
                text = translateToDB(str('{:03}'.format(y[2]))+str('{:03}'.format(y[1]))+str('{:03}'.format(y[0])))
                if text in count:
                    count[text] = count[text] + 1
                else:
                    count[text] = 1
        #count.pop(0)
        countedPixels = sum(count.values())
        result = 0.0
        for x in count.keys():
            result += x * (count[x] / countedPixels)
        resultArray.insert(i,result)
    #print(avg_color)
    # rgb
    # 55<   => (255, 255, 255) ignore
    # 55-60 => (255, 99, 54) 58
    # 60-65 => (199, 23, 18) 63
    # 65-70 => (138, 18, 20) 68
    # 70-75 => (145, 15, 102) 73
    # >75   => (41, 115, 184) 75
    return resultArray

def translateToDB(var):
    if var == "255255255":
        return 0
    elif var == "255099054":
        return 58
    elif var == "199023018":
        return 63
    elif var == "138018020":
        return 68
    elif var == "145015102":
        return 73
    elif var == "041115184":
        return 75


startValueX = 52.537791
startValueY = 13.343777
endValueX = 52.566129
endValueY = 13.392601

dbDict = {}

for x in range(5):
    for y in range(5):
        data = getBoxData(startValueX+x*0.004, startValueY+y*0.004)
        i = 0
        for dat in data:
            dbDict[(startValueX+x*0.004+math.ceil(i/4)*0.0005, startValueY+y*0.004+(i%4)*0.0005)] = dat
            i = i + 1




string = "["
for key in dbDict.keys():
    string = string + "{"+"lat: {}, lng: {}, count: {}".format(key[0], key[1], dbDict[key])+"},"

string = string + "]"

print (string)
