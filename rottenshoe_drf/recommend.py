#컨텐츠 기반 핕터링 / 유클리드 사용
# 타겟 인스턴스에 유사한 스니커즈 찾도록 고안.

import math
def get_uclid_distance(target,whole_list):
    dist_list = []
    for compare in whole_list:
        dist = math.sqrt(pow(target['comfortable']-compare['comfortable'],2) +
        pow(target['grip']-compare['grip'],2) + pow(target['spotlight'] - compare['spotlight'],2) +
        pow(target['convenience'] - compare['convenience'],2))

        dist_list.append(dist) 
    
    return dist_list