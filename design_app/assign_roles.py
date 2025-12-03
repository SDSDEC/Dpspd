import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DesignPro.settings')
django.setup()

from django.contrib.auth.models import User
from design_app.models import UserProfile

# роли
users_roles = {
    'admin': 'ADMIN',
    'designer1': 'DESIGNER',
    'manager1': 'MANAGER',
}

for username, role in users_roles.items():
    try:
        user = User.objects.get(username=username)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.user_type = role
        profile.full_name = f"Тестовый {role}"
        profile.agreement = True
        profile.save()
        print(f"✅ Назначена роль {role} пользователю {username}")
    except User.DoesNotExist:
        print(f"⚠️ Пользователь {username} не найден")

print("🎉 Роли назначены!")