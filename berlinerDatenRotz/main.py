import requests, cv2, numpy, math, json, time

from progress.bar import Bar

def getBoxData(x, y):
    try:
        r = requests.get('https://fbinter.stadt-berlin.de/fb/wms/senstadt/wmsk_07_05_01str_vbusDEN?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&CACHEID=888282&LAYERS=1&WIDTH=128&HEIGHT=128&CRS=EPSG:4326&STYLES=&BBOX={}, {}, {}, {}'.format(x, y, x+0.004, y+0.004))
    except requests.exceptions.ConnectionError:
        time.sleep(30.0)
        r = requests.get('https://fbinter.stadt-berlin.de/fb/wms/senstadt/wmsk_07_05_01str_vbusDEN?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&CACHEID=888282&LAYERS=1&WIDTH=128&HEIGHT=128&CRS=EPSG:4326&STYLES=&BBOX={}, {}, {}, {}'.format(x, y, x+0.004, y+0.004))
    with open(r'image.png','wb') as f:
        f.write(r.content)

    myimg = cv2.imread('image.png')

    imgSlices = []
    imgSize = 16

    for x in range(8):
        for y in range(8):
            imgSlices.append(myimg[x*imgSize:x*imgSize+imgSize, y*imgSize:y*imgSize+imgSize])

    # finalSize = 16
    # 128 pixels each
    # 32 pixels each

    resultArray = []


    for i in range(64):
        count = {}
        for x in imgSlices[i]:
            for y in x:
                key = translateToDB(str('{:03}'.format(y[2]))+str('{:03}'.format(y[1]))+str('{:03}'.format(y[0])))
                if key in count:
                    count[key] = count[key] + 1
                else:
                    count[key] = 1
        #count.pop(0)
        countedPixels = 256 # sum(count.values())
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
    return resultArray #[::-1]

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


startValueX = 52.411607
startValueY = 13.206281

dbDict = {}

xMax = 100
yMax = 100

class FancyBar(Bar):
    suffix = '%(percent).1f%% - %(eta)ds'

bar = FancyBar('Fetching', max=xMax*yMax)

for x in range(xMax):
    for y in range(yMax):
        data = getBoxData(startValueX+x*0.004, startValueY+y*0.004)
        i = 0
        xStart = startValueX+0.004+x*0.004
        yStart = startValueY+y*0.004
        for xi in range(8):
            xStart = xStart - 0.0005
            for yi in range(8):
                dbDict[(xStart,yStart+yi*0.0005)] = data[i]
                i = i+1
        bar.next()
bar.finish()

string = "["
for key in dbDict.keys():
    string = string + "{"+"lat: {}, lng: {}, count: {}".format(key[0], key[1], dbDict[key])+"},"

string = string.rstrip(',')

string = string + "]"


with open("Output.txt", "w") as text_file:
    text_file.write(string)

list = []

for key in dbDict.keys():
    list.append({"lat": key[0], "lng": key[1], "count": dbDict[key]})

with open('result.json', 'w') as fp:
    json.dump(list, fp)
