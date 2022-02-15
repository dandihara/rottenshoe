#컨텐츠 기반 핕터링 / 유클리드 사용
# 타겟 인스턴스에 유사한 스니커즈 찾도록 고안.

import math
import numpy as np
def get_uclid_similar(target,whole_list):
    result = []
    for compare in whole_list:
        dist = math.sqrt(pow(target['comfortable']-compare['comfortable'],2) +
        pow(target['grip']-compare['grip'],2) + pow(target['spotlight'] - compare['spotlight'],2) +
        pow(target['convenience'] - compare['convenience'],2))

        result.append(dist) 
    
    return result

#코사인 유사도 코드
def get_cos_similar(target,compare):
    target = np.array(list(target.values())[2:])
    compare = np.array(list(compare.values())[2:])

    return np.dot(target,compare) /(np.norm(target) * np.norm(compare))
        