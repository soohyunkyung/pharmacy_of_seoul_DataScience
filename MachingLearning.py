!pip install haversine

from sklearn.neighbors import KNeighborsClassifier
from haversine import haversine
import numpy as np

#datas, 유저의 위도&경도-> datas 내에서 사용자와 가까운 약국이 있는 5개의 딕셔너리와 해당 딕셔너리에 약국과의 거리를 추가하여 return.

def get_pharmacy(datas, user_latitude, user_longitude):
    
    filtered_longitude=[]
    filtered_latitude=[]
    datas_results=[]

    for i in range(len(datas)):
        filtered_longitude.append(float(datas[i]['longitude']))
        filtered_latitude.append(float(datas[i]['latitude']))

    lat_lon_zip=[[lat,lon] for lat, lon in zip(filtered_latitude, filtered_longitude)]
    fake=np.zeros(len(datas))
    
    if (len(datas))>4:
        kn=KNeighborsClassifier()

        mean=np.mean(lat_lon_zip,axis=0)
        std=np.std(lat_lon_zip,axis=0)

        lat_lon_zip=(lat_lon_zip-mean)/std
        new=([user_latitude, user_longitude]-mean)/std

        kn.fit(lat_lon_zip, fake)
        distances, indexes=kn.kneighbors([new])
        

    elif(len(datas))<5:
        kn=KNeighborsClassifier(n_neighbors=len(datas))

        kn.fit(lat_lon_zip, fake)
        distances, indexes=kn.kneighbors([[user_latitude, user_longitude]])
    
    for i in indexes[0]:
        datas[i]["distance"]=(str(haversine((float(user_latitude), float(user_longitude)),(float(datas[i]['latitude']),float(datas[i]['longitude']))))+"km") #사용자로부터 가까운 5개 약국과의 거리를 저장합니다.
    
    for i in indexes[0]:
        datas_results.append(datas[i])
        
    return datas_results
