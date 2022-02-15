from rottenshoe.models import *

# 편의성 / 화제성 / 착화감 / 기능성
# 화제성은 기존의 cop or drop을 이용하여 변동성을 줄 예정.
class SneakerFeatures(models.Model):
    sneaker = models.ForeignKey(Sneakers,on_delete=models.CASCADE)
    comfortable = models.FloatField(default=0.0,verbose_name='편안함')
    grip = models.FloatField(default=0.0,verbose_name='착화감')
    spotlight = models.FloatField(default=0.0,verbose_name='화제성')
    convenience = models.FloatField(default=0.0,verbose_name='실용성')