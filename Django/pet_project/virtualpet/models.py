from django.db import models
from django.utils import timezone

class VirtualPet(models.Model):
    name = models.CharField(max_length=100, default="宠物小猫")
    happiness = models.IntegerField(default=8)
    health = models.IntegerField(default=8)
    hunger = models.IntegerField(default=0)
    growth = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    time_cycle = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    # 添加各操作的最后执行时间字段，用于冷却时间机制
    last_feed_time = models.DateTimeField(default=timezone.now)
    last_walk_time = models.DateTimeField(default=timezone.now)
    last_play_time = models.DateTimeField(default=timezone.now)
    last_doctor_time = models.DateTimeField(default=timezone.now)

    def update_status(self):
        # 更新时间周期
        self.time_cycle += 1
        if self.time_cycle == 60:
            self.time_cycle = 0
            
        # 检查是否需要增加成长值
        if self.time_cycle % 60 == 0:
            self.growth += 1
            
        # 检查是否需要增加年龄
        if self.growth >= 365:
            self.growth = 0
            self.year += 1
            
        # 根据时间周期更新状态
        if self.time_cycle <= 48:  # 清醒状态
            # 每15秒增加1点饥饿值
            if self.time_cycle % 3 == 0:
                self.hunger += 1
            
            # 每30秒减少1点愉悦度
            if self.time_cycle % 6 == 0:
                self.happiness -= 1
        else:  # 睡眠状态
            # 每45秒增加1点饥饿值
            if self.time_cycle % 9 == 0:
                self.hunger += 1
            
        # 检查饥饿对健康的影响
        if self.hunger == 7 and self.time_cycle % 6 == 0:
            self.health -= 1
        if self.hunger == 8 and self.time_cycle % 3 == 0:
            self.health -= 1
            
        # 确保属性值在合理范围内
        self.hunger = max(0, min(self.hunger, 8))
        self.happiness = max(0, min(self.happiness, 8))
        self.health = max(0, min(self.health, 8))
        self.growth = max(0, min(self.growth, 365))
        
        self.save()
