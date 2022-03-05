#컨텐츠 기반 핕터링 / 유클리드 사용
# 타겟 인스턴스에 유사한 스니커즈 찾도록 고안.

import math
import numpy as np
from .models import SneakerFeatures,Sneakers
def get_uclid_similar(target,whole_list):
    result = []
    for compare in whole_list:
        dist = math.sqrt(pow(target['comfortable']-compare['comfortable'],2) +
        pow(target['grip']-compare['grip'],2) + pow(target['spotlight'] - compare['spotlight'],2) +
        pow(target['convenience'] - compare['convenience'],2))

        result.append(dist) 
    
    return result

#코사인 유사도 코드
def get_cos_similar(target):
    result = []
    #원하는 필드만 골라서 튜플로 반환 => 리스트로 원한다면 flat속성 true
    featrue_list = SneakerFeatures.objects.values_list('comfortable','grip','spotlight','convenience').exclude(id = target.id)
    target = np.array(list(target)) #  형식 변경 -> queryset -> list
    norm_target = np.linalg.norm(target)
    for f in featrue_list:
        f = np.array(list(f))
        result.append(np.dot(target,f) /(norm_target * np.linalg.norm(f)))
    result.sort(reverse=True) # 내림차순
    return result
        