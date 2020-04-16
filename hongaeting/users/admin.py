from django.contrib import admin
from django.contrib.admin import register

from coins.models import CoinHistory
from common.constants import REWORD_COUNT, COIN_CHANGE_REASON
from users.models import User, Profile


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'university_email', 'is_confirmed_student', 'student_id_card_image', 'user_code', 'is_staff',
        'is_superuser', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_confirmed_student',)
    ordering = ('-id', 'student_id_card_image',)
    actions = ('confirm_users',)

    def confirm_users(self, request, queryset):
        updated_count = queryset.update(is_confirmed_student=True)

        # confirm_users의 실행시간을 줄이기 위해 bulk create를 사용하여 코인지급을 한다.
        bulk_list = []
        for user in queryset:
            if not hasattr(user, 'profile'):
                continue
            coin_history = CoinHistory(profile=user.profile,
                                       rest_coin=user.profile.get_rest_coin() + REWORD_COUNT['CONFIRM_USER'],
                                       reason=COIN_CHANGE_REASON.CONFIRM_USER,
                                       message='학생 인증으로 인한 coin 지급')
            bulk_list.append(coin_history)

        CoinHistory.objects.bulk_create(bulk_list)

        self.message_user(request, f'{updated_count}명의 user를 confirm 상태로 변경')

    confirm_users.short_description = '여러명의 user를 한번에 confirm'


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
