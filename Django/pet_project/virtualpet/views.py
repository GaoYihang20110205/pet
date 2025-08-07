from django.shortcuts import render, redirect, get_object_or_404
from .models import VirtualPet
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse


def test_update(request):
    # 测试页面视图
    return render(request, 'virtualpet/test_update.html')


# 首页视图
def index(request):
    return render(request, 'virtualpet/index.html')


def pet_detail(request):
    # 获取或创建宠物实例
    pet = VirtualPet.objects.first()
    if not pet:
        pet = VirtualPet.objects.create()
    
    # 计算状态百分比
    hunger_percent = (8 - pet.hunger) * 100 / 8
    happiness_percent = pet.happiness * 100 / 8
    health_percent = pet.health * 100 / 8
    
    # 确定当前状态（用于显示相应的动画）
    status = "idle"
    if pet.time_cycle > 48:
        status = "sleeping"
    
    return render(request, 'virtualpet/pet_detail.html', {
        'pet': pet,
        'hunger_percent': hunger_percent,
        'happiness_percent': happiness_percent,
        'health_percent': health_percent,
        'status': status
    })


def feed_pet(request):
    pet = get_object_or_404(VirtualPet, id=1)
    # 检查冷却时间（2秒）
    cooldown = 2  # 冷却时间（秒）
    now = timezone.now()
    time_diff = (now - pet.last_feed_time).total_seconds()
    
    if time_diff >= cooldown:
        pet.hunger = max(0, pet.hunger - 2)
        pet.last_feed_time = now
        pet.save()
        return JsonResponse({'status': 'success', 'message': '喂食成功'})
    else:
        # 返回冷却中信息
        remaining = cooldown - int(time_diff)
        return JsonResponse({'status': 'error', 'message': f'喂食功能冷却中，还需{remaining}秒'})


def walk_pet(request):
    pet = get_object_or_404(VirtualPet, id=1)
    # 检查冷却时间（5秒）
    cooldown = 5  # 冷却时间（秒）
    now = timezone.now()
    time_diff = (now - pet.last_walk_time).total_seconds()
    
    if time_diff >= cooldown:
        # 散步增加愉悦度和健康度
        pet.happiness = min(8, pet.happiness + 1)
        pet.health = min(8, pet.health + 1)
        pet.last_walk_time = now
        pet.save()
        return JsonResponse({'status': 'success', 'message': '散步成功'})
    else:
        # 返回冷却中信息
        remaining = cooldown - int(time_diff)
        return JsonResponse({'status': 'error', 'message': f'散步功能冷却中，还需{remaining}秒'})


def play_pet(request):
    pet = get_object_or_404(VirtualPet, id=1)
    # 检查冷却时间（4秒）
    cooldown = 4  # 冷却时间（秒）
    now = timezone.now()
    time_diff = (now - pet.last_play_time).total_seconds()
    
    if time_diff >= cooldown:
        # 玩耍增加愉悦度
        pet.happiness = min(8, pet.happiness + 1)
        pet.last_play_time = now
        pet.save()
        return JsonResponse({'status': 'success', 'message': '玩耍成功'})
    else:
        # 返回冷却中信息
        remaining = cooldown - int(time_diff)
        return JsonResponse({'status': 'error', 'message': f'玩耍功能冷却中，还需{remaining}秒'})


def doctor_pet(request):
    pet = get_object_or_404(VirtualPet, id=1)
    # 检查冷却时间（7秒）
    cooldown = 7  # 冷却时间（秒）
    now = timezone.now()
    time_diff = (now - pet.last_doctor_time).total_seconds()
    
    if time_diff >= cooldown:
        # 寻医增加健康度
        pet.health = min(8, pet.health + 1)
        pet.last_doctor_time = now
        pet.save()
        return JsonResponse({'status': 'success', 'message': '寻医成功'})
    else:
        # 返回冷却中信息
        remaining = cooldown - int(time_diff)
        return JsonResponse({'status': 'error', 'message': f'寻医功能冷却中，还需{remaining}秒'})


def update_pet_status(request):
    # 这个视图用于定期更新宠物状态
    pet = get_object_or_404(VirtualPet, id=1)
    pet.update_status()
    
    # 计算状态百分比
    hunger_percent = (8 - pet.hunger) * 100 / 8
    happiness_percent = pet.happiness * 100 / 8
    health_percent = pet.health * 100 / 8
    
    # 确定当前状态
    status = "idle"
    if pet.time_cycle > 48:
        status = "sleeping"
    
    return JsonResponse({
        'status': 'success',
        'hunger': pet.hunger,
        'happiness': pet.happiness,
        'health': pet.health,
        'hunger_percent': hunger_percent,
        'happiness_percent': happiness_percent,
        'health_percent': health_percent,
        'pet_status': status,
        'growth': pet.growth,
        'year': pet.year
    })
