global clat, clon, ww, hh, zoom, mapimg, counter, testcounter

# Utrecht
clat = 52.092876
clon = 5.104480

ww = 512
hh = 512

zoom = 6

counter = 1986

def mapx(lon):
    delta =  lon - clon
    asdf = map(delta, -ratiox, ratiox, - height / 2, height / 2)

    return int(asdf)

def mapy(lat):
    delta = clat - lat
    asdf = map(delta, -ratioy, ratioy, - width / 2, width / 2)

    return int(asdf)

def preload():
    global clat, clon, ww, hh, zoom, mapimg, quakes, ratioy, ratiox, quakesdict
    
    imgurl = 'https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/' + str(clon) + ',' + str(clat) + ',' + str(zoom) + '/' + str(ww + 100) + 'x' + str(hh + 100) + '?access_token=pk.eyJ1IjoiY29kaW5ndHJhaW4iLCJhIjoiY2l6MGl4bXhsMDRpNzJxcDh0a2NhNDExbCJ9.awIfnl6ngyHoB3Xztkzarw'
    mapimg = loadImage(imgurl, "png")
    
    # quakes looks like this:
    # YYMMDD,TIME,LOCATION,LAT,LON,DEPTH,MAG,EVALMODE
    # 20180419,093307.59,Tjuchem,53.271,6.868,3.0,0.5,manual
    
    quakes = loadTable("http://cdn.knmi.nl/knmi/map/page/seismologie/all_induced.csv", "header")
    
    # ratio only works for square wwxhh from 2 ** zoom
    ratioy = 217.216 / (2 ** zoom) / ( float( 1024 / ww ) )
    ratiox = 354.048 / (2 ** zoom) / ( float( 1024 / hh ) )
    
    quakesdict = {}
    
    numrows = quakes.getRowCount()
    
    for i in range(numrows):        
        timestamp = quakes.getInt(i, "YYMMDD")
        yearstamp = int(str(timestamp)[:4])
        
        if not yearstamp in quakesdict:
            quakesdict[yearstamp] = []
        
        x = mapx(quakes.getFloat(i, "LON"))
        y = mapy(quakes.getFloat(i, "LAT"))
        
        quakesdict[yearstamp].append((x, y))

def setup():
    global ratiox, pg
    
    preload()
    #make them move
    frameRate(1)
        
    size(ww, hh)
    
    translate(width / 2, height / 2)
    
    imageMode(CENTER)     
    
    shapeMode(CENTER)
    
    image(mapimg, 0, 0)

def draw():
    global counter, testcounter
        
    image(mapimg, 0 + ww / 2, 0 + hh / 2)
    
    todraw = []
    
    try:
        todraw = quakesdict[counter]    
    except KeyError:
        print 'No earthquake this year'
            
    counter += 1

    for el in todraw:
        fill(255, 255, 255, 100)
        noStroke()
        ellipse(el[0] + ww / 2, el[1] + hh / 2, 50, 50)
    
    #yeartext
    fill(255)
    textSize(24)
    text(counter, 0 + 50, 0 + 50)
    
    filename = 'image' + str(counter) + '.png'
    
    save(filename)
    
    if counter == 2019:
        exit()
