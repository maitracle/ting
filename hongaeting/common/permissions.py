from rest_framework import permissions


class IsOwnerUserOnly(permissions.BasePermission):
    def has_object_permission(self, request, views, obj):
        return obj.user == request.user


class IsOwnerUserOrReadonly(permissions.BasePermission):
    # 인증된 유저에 대해 목록 조회 / 포스팅 등록 허용
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # 작성자에 한해 Record에 대한 수정 / 삭제 허용
    def has_object_permission(self, request, views, obj):
        # 조회 요청은 항상 True
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT, DELETE 요청에 한해, 작성자에게만 허용
        return obj.user == request.user


class IsOwnerProfileOrReadonly(permissions.BasePermission):
    # 인증된 유저에 대해 목록 조회 / 포스팅 등록 허용
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # 작성자에 한해 Record에 대한 수정 / 삭제 허용
    def has_object_permission(self, request, views, obj):
        # 조회 요청은 항상 True
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT, DELETE 요청에 한해, 작성자에게만 허용
        return obj.profile.user == request.user


class IsHaveSelfDateProfileAndIsActive(permissions.BasePermission):
    # 자신의 SelfDateProfile 이 존재하고 is_active가 True이면 retrieve 허용
    # 거절되었을 때 보내주는 에러메세지
    message = 'Inactive users not alloewed.'

    def has_permission(self, request, view):
        return bool(request.user.profile.selfdateprofile and
                    request.user.profile.selfdateprofile.is_active)
