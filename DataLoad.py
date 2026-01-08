#열 단위 데이터 형성의 전체 과정입니다.
#1. OpenAPI로 약국 위치 정보 데이터를 가져와 데이터 프레임으로 만들기
#2. 외국어 가능 약국 데이터를 다운 받아 데이터 프레임으로 만들기
#3. 약국 위치 정보와 외국어 가능 약국의 데이터프레임을 합치고 중복 행 제거하기
#4. 주소 파싱


#1
#OpenAPI 데이터 가져오기
import requests
import pandas as pd
import numpy as np

# 1. OpenAPI 데이터 가져오기
api_key = "보안키"  
base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/TbPharmacyOperateInfo/"

all_rows = []
start_idx = 1
end_idx = 1000
step = 1000

print("데이터를 불러오는 중...")

while True:
    url = f"{base_url}{start_idx}/{end_idx}/"
    response = requests.get(url)
    json_ob = response.json() # .json()을 사용하면 더 간편합니다.
    
    # 데이터가 있는지 확인
    if 'TbPharmacyOperateInfo' in json_ob:
        rows = json_ob['TbPharmacyOperateInfo']['row']
        all_rows.extend(rows)
        
        # 전체 건수를 확인하여 더 가져올 데이터가 있는지 판단
        total_count = json_ob['TbPharmacyOperateInfo']['list_total_count']
        if end_idx >= total_count:
            break
            
        start_idx += step
        end_idx += step
    else:
        # 오류 발생 시 혹은 더 이상 데이터가 없을 시 중단
        break

# OpenAPI 데이터를 통합 데이터프레임으로 변환
ph_df = pd.DataFrame(all_rows)
print(f"총 {len(ph_df)}개의 약국 데이터를 가져왔습니다.")


# 2. 외국어 가능 약국 데이터 가져오기
# (파일 경로를 확인해주세요)
Fph_df = pd.read_excel("/content/외국어 가능 약국 현황.xlsx", header=2)
Fph_df.drop([0], axis=0, inplace=True)
Fph_df = Fph_df.rename(columns={
    '약국이름':'DUTYNAME', 
    '주소 (도로명)': 'DUTYADDR', 
    '전화번호':'DUTYTEL1',
    '가능 외국어':'외국어가능',
    'Unnamed: 6': 'English',
    'Unnamed: 7': 'Chinese', 
    'Unnamed: 8':'Japanese'
})


# 3. 데이터프레임 합치기 및 정제
Pharmacy_df = pd.concat([ph_df, Fph_df], ignore_index=True)

# 중복 제거 (전화번호 기준)
Pharmacy_df = Pharmacy_df.drop_duplicates(subset=['DUTYTEL1'], keep=False)

# 자치구 열 삭제 (존재할 경우에만)
if '자치구' in Pharmacy_df.columns:
    Pharmacy_df = Pharmacy_df.drop('자치구', axis=1)

# 결측치 처리
Pharmacy_df.fillna(False, inplace=True)
Pharmacy_df['WGS84LON'] = pd.to_numeric(Pharmacy_df['WGS84LON'].replace(False, np.NaN))
Pharmacy_df['WGS84LAT'] = pd.to_numeric(Pharmacy_df['WGS84LAT'].replace(False, np.NaN))


# 4. 주소 파싱 (시, 구, 도로명 단위 분리)
# 기존의 복잡한 루프 대신 Pandas의 str.split을 사용하면 훨씬 빠르고 안전합니다.
addr_split = Pharmacy_df['DUTYADDR'].str.split(' ', n=2, expand=True)

Pharmacy_df['시'] = addr_split[0]
Pharmacy_df['구'] = addr_split[1]
Pharmacy_df['도로명'] = addr_split[2]

# 결과 확인
print(Pharmacy_df[['DUTYNAME', '시', '구', '도로명']].head())
