from sklearn.neighbors import KNeighborsClassifier

def get_pharmacy(longitude, latitude)
  kn=KNeighborsClassifier()
  kn.fit(longitude, latitude) #드롭다운 된 경도, 위도를 가져와야 합니다.
  user=[경도, 위도] #사용자의 경도, 위도입니다.
  kn.predict([new]) 
  distances, indexes=kn.neighbors([new])

  for i in indexes:
    print(name[i], gu[i]+" "+road_name_adress[i]) #사용자 주변 5개의 약국 이름, 약국 주소를 출력합니다.

  for i in len(indexes):
    print(distances[i]) #거리 변환이 필요합니다.
