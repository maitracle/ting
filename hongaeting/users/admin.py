from django.contrib import admin
from django.contrib.admin import register

from users.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'university_email', 'is_confirmed_student', 'student_id_card_image', 'user_code', 'is_staff',
        'is_superuser', 'is_active')
    list_filter = ('is_active', 'is_confirmed_student',)
    ordering = ('-id', 'student_id_card_image',)
    actions = ('confirm_user', )

    def confirm_user(self, request, queryset):
        updated_count = queryset.update(is_confirmed_student=True)
        self.message_user(request, f'{updated_count}명의 user를 confirm상태로 변경')
    confirm_user.short_description = '여러명의 user를 한번에 confirm'
