
import csv
import requests
import time
import json

username = ""

def requestGeoName(row):
    #parts = row.split(',')
    lng = row[0]
    lat = row[1]
    r = requests.get("http://api.geonames.org/findNearestIntersectionOSMJSON?lat="+lat+"&lng="+lng+"&username="+username)
    if (r.status_code == 200):
        return r.json()
    else:
        return {"error":r.status_code}

def requestNameWsUsig(row):
    x = row[0]
    y = row[1]
    reqReverseGeo = requests.get("http://ws.usig.buenosaires.gob.ar/geocoder/2.2/reversegeocoding?y={0}&x={1}".format(y,x))
    resReverseGeo = json.loads(reqReverseGeo.content.replace("(", "").replace(")", ""), encoding="utf-8")
    
    reqConvertirCoord = requests.get("http://ws.usig.buenosaires.gob.ar/rest/convertir_coordenadas?x={0}&y={1}&output=lonlat".format(resReverseGeo["puerta_x"], resReverseGeo["puerta_y"]))
    resConvertirCoord = reqConvertirCoord.json()
    
    result = { "intersection" : {
            "lng" : resConvertirCoord["resultado"]["x"],
            "lat" : resConvertirCoord["resultado"]["y"],
            "street1" : resReverseGeo["esquina"],
            "street2" : resReverseGeo["esquina"]
        }}
    
    return result

with open('mostSearchedPlaces.csv', 'rb') as csvfile:
    with open('mostSearchedPlacesWithCorners.csv', 'a') as outputCSV:
        csv_writer = csv.writer(outputCSV, delimiter=',')
        
        reader = csv.reader(csvfile, delimiter = ',')
        i = 1
        for row in reader:
            geoNameResult = requestGeoName(row)
            
            # Check if there is no intersection
            if (geoNameResult == {}):
                geoNameResult = requestNameWsUsig(row)
            
            print(geoNameResult)
            
            if (not geoNameResult.has_key("error")):
                row.append(str(geoNameResult["intersection"]["lng"]))
                row.append(str(geoNameResult["intersection"]["lat"]))
                row.append(geoNameResult["intersection"]["street1"].encode("utf-8"))
                row.append(geoNameResult["intersection"]["street2"].encode("utf-8"))
                
            csv_writer.writerow(row)
            print("Elemento {0} procesado".format(i))
            i += 1
            time.sleep(2)
