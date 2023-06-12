from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q

from Posts.models import Post, Profile, BlockedProfile, PostComment
# Register your models here.


class BlockedProfileAdmin(admin.StackedInline):
    model = BlockedProfile
    extra = 0
    fk_name = "blocked_by"


class ProfileAdmin(admin.ModelAdmin):
    inlines = [BlockedProfileAdmin]
    list_display = ("first_name", "last_name", "skills")

    def save_model(self, request, obj, form, change):
        if User.objects.filter(first_name=obj.first_name).count() > 0:
            u = User.objects.create_user(obj.first_name, password=obj.password, is_staff=True)
            group = Group.objects.get(name="ProfileGroup")
            group.user_set.add(u)
            obj.profile_user = u

        obj.save()

    def has_change_permission(self, request, obj=None):
        if obj:
            if request.user.is_superuser or obj.profile_user == request.user:
                return True
            return False

    def has_delete_permission(self, request, obj=None):
        if obj:
            if request.user.is_superuser or obj.profile_user == request.user:
                return True
            return False


admin.site.register(Profile, ProfileAdmin)


class PostCommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.comment_user = Profile.objects.filter(profile_user=request.user.id).get()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            if obj.comment_user == Profile.objects.filter(profile_user=request.user.id).get():
                return True
            if obj.comment_post.post_profile == Profile.objects.filter(profile_user=request.user.id).get():
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            if obj.comment_user == Profile.objects.filter(profile_user=request.user.id).get():
                return True
        return False


admin.site.register(PostComment, PostCommentAdmin)


class PostCommentAdminInline(admin.StackedInline):
    model = PostComment
    extra = 0

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            if PostComment.objects.filter(comment_user=Profile.objects.filter(profile_user=request.user.id).get()).count() > 0:
                return True
            if PostComment.objects.filter(comment_post__post_profile= Profile.objects.filter(profile_user=request.user.id).get()).count() > 0:
                return True
        return False


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCommentAdminInline]
    list_filter = ("post_creation_date", )
    list_display = ("post_title", "post_profile")
    search_fields = ("post_title", "post_content")

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.post_profile = Profile.objects.filter(profile_user=request.user.id).get()
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj:
            if request.user.is_superuser or obj.post_profile == Profile.objects.filter(profile_user=request.user.id).get():
                return True
            return False

    def has_delete_permission(self, request, obj=None):
        if obj:
            if request.user.is_superuser or obj.post_profile == Profile.objects.filter(profile_user=request.user.id).get():
                return True
            return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        im_blocked = BlockedProfile.objects.filter(users__profile_user_id=request.user.id).all()
        i_blocked = BlockedProfile.objects.filter(blocked_by__profile_user_id=request.user.id).all()
        check_if_blocked = []
        check_if_i_blocked = []
        for row in im_blocked.values_list():
            check_if_blocked.append(row[1])

        for row in i_blocked.values_list():
            check_if_i_blocked.append(row[2])

        return qs.exclude(Q(post_profile_id__in=check_if_blocked) | Q(post_profile_id__in=check_if_i_blocked))


admin.site.register(Post, PostAdmin)


