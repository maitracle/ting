import os

from django.core.validators import MinLengthValidator
from django.db import models, transaction
from model_utils import Choices
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound

from common.KakaoClient import KakaoClient
from common.constants import COST_COUNT, COIN_CHANGE_REASON
from common.models import BaseModel
from common.models import BaseModel
from common.models import BaseModel
from self_date.validators import chat_link_validator
from users.models import User


class SelfDateProfileRight(BaseModel):
    buying_self_date_profile = models.ForeignKey('self_date.SelfDateProfile',
                                                 related_name='buying_self_date_profile_rights',
                                                 on_delete=models.CASCADE)
    target_self_date_profile = models.ForeignKey('self_date.SelfDateProfile',
                                                 related_name='target_self_date_profile_rights',
                                                 on_delete=models.CASCADE)
    right_type = models.CharField(max_length=50, choices=COIN_CHANGE_REASON)
    coin_history = models.OneToOneField('coins.CoinHistory', null=True, on_delete=models.PROTECT)


def image_path(instance, original_filename):
    path = f'profiles/{instance.profile.user.get_full_name()}/image{os.path.splitext(original_filename)[1]}'
    return path


class SelfDateProfile(BaseModel):
    BODY_TYPE_CHOICES = Choices('SLIM', 'SLIM_TONED', 'NORMAL', 'BUFF', 'CHUBBY')
    RELIGION_CHOICES = Choices('NOTHING', 'CHRISTIANITY', 'BUDDHISM', 'CATHOLIC', 'ETC')
    IS_SMOKE_CHOICES = Choices('YES', 'NO')

    profile = models.OneToOneField('users.Profile', related_name='self_date_profile', on_delete=models.CASCADE,
                                   verbose_name='프로필')

    nickname = models.CharField(max_length=8, unique=True, verbose_name='셀프데이트 닉네임')
    height = models.PositiveSmallIntegerField(verbose_name='키')
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, verbose_name='체형')
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, verbose_name='종교')
    is_smoke = models.CharField(max_length=10, choices=IS_SMOKE_CHOICES, verbose_name='흡연여부')

    tags = models.CharField(max_length=500)
    image = models.ImageField(upload_to=image_path, null=True, blank=True, max_length=1000, verbose_name='프로필이미지')
    one_sentence = models.CharField(max_length=35, verbose_name='하고싶은 한마디')

    appearance = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], verbose_name='외모')
    personality = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], verbose_name='성격')
    hobby = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], verbose_name='취미')
    date_style = models.CharField(max_length=1000, validators=[MinLengthValidator(60)], verbose_name='연애관')
    ideal_type = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], verbose_name='이상형')
    chat_link = models.URLField(validators=[chat_link_validator], verbose_name='카카오톡 채팅링크')

    is_active = models.BooleanField(default=True, help_text='셀프 데이트 프로필 공개 여부')

    def __str__(self):
        return self.nickname

    @property
    def is_valid_chat_link(self):
        return KakaoClient.instance().is_valid_kakao_link(self.chat_link)

    def get_target_self_date_profile_to_retrieve(self, target_self_date_profile):
        """
        self가 target_self_date_profile 내용을 조회 가능한지 확인 후 target_self_date_profile을 반환한다.
        """
        is_having_view_right = self.check_having_right(
            target_self_date_profile, COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW)

        if not is_having_view_right:
            self.buy_right_for_target_self_date_profile(
                target_self_date_profile=target_self_date_profile, right_type=COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW)

        return target_self_date_profile

    def get_target_chat_link(self, target_self_date_profile):
        if not target_self_date_profile.is_valid_chat_link:
            raise NotFound('상대방의 채팅방 삭제로 인한 not found')

        is_having_message_right = self.check_having_right(
            target_self_date_profile, COIN_CHANGE_REASON.SELF_DATE_SEND_MESSAGE)

        if not is_having_message_right:
            self.buy_right_for_target_self_date_profile(
                target_self_date_profile=target_self_date_profile, right_type=COIN_CHANGE_REASON.SELF_DATE_SEND_MESSAGE)

        return target_self_date_profile.chat_link

    def check_having_right(self, target_self_date_profile, right_type):
        right_queryset = SelfDateProfileRight.objects.filter(
            buying_self_date_profile=self.id
        ).filter(
            target_self_date_profile=target_self_date_profile
        ).filter(
            right_type=right_type
        )

        return right_queryset.exists()

    def buy_right_for_target_self_date_profile(self, target_self_date_profile, right_type):
        """
        rest_coin을 감소시킨 coin_history와 self_date_profile_right를 생성한다.
        :param target_self_date_profile: right의 대상이 되는 profile
        :param right_type: right 종류 (ex: SELF_DATE_PROFILE_VIEW, SELF_DATE_SEND_MESSAGE 등)
        :return: 생성된 self_date_profile_right
        """
        from coins.models import CoinHistory

        coin_history_kwargs = self._get_kwargs_for_coin_history(target_self_date_profile, right_type)

        with transaction.atomic():
            coin_history = CoinHistory(**coin_history_kwargs)
            coin_history.save()

            self_date_profile_right = SelfDateProfileRight(buying_self_date_profile=self,
                                                           target_self_date_profile=target_self_date_profile,
                                                           coin_history=coin_history,
                                                           right_type=right_type)
            self_date_profile_right.save()

        return self_date_profile_right

    def _get_kwargs_for_coin_history(self, target_self_date_profile, right_type):
        map_right_type_to_message = {
            COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW: '조회',
            COIN_CHANGE_REASON.SELF_DATE_SEND_MESSAGE: 'chat link 조회',
        }

        if self.profile.coin_histories.last().rest_coin - COST_COUNT[right_type] < 0:
            raise PermissionDenied('코인 개수 부족으로 인한 permission denied')

        try:
            message_suffix = map_right_type_to_message[right_type]

            new_coin_history_args = {
                'profile': self.profile,
                'rest_coin': self.profile.coin_histories.last().rest_coin - COST_COUNT[right_type],
                'reason': right_type,
                'message': f'{target_self_date_profile.nickname}의 self date profile {message_suffix}',
            }

            return new_coin_history_args

        except KeyError:
            raise ValidationError('잘못된 right_type으로 인한 validation error')


class SelfDateLike(BaseModel):
    self_date_profile = models.ForeignKey(SelfDateProfile, related_name='self_date_likes', on_delete=models.CASCADE,
                                          help_text='like를 보낸 사람')
    liked_self_date_profile = models.ForeignKey(SelfDateProfile, related_name='accepted_self_date_likes',
                                                on_delete=models.CASCADE, help_text='like를 받은 사람')
