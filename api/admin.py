from django.contrib import admin

from .models import Purchase, Report, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "user_type")
    search_fields = ("name", "email")
    list_filter = ("user_type",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "get_user_name")
    search_fields = ("title", "status")
    list_filter = ("status",)

    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.admin_order_field = "user"
    get_user_name.short_description = "Admin Name"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "price", "get_user_name")
    search_fields = ("item",)
    list_filter = ("price",)

    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.admin_order_field = "user"
    get_user_name.short_description = "User Name"
