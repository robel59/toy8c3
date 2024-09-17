from django.contrib import admin
from .models import *

class BlogContentInline(admin.TabularInline):
    model = BlogContent

@admin.register(Item)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogContentInline]
# Register your models here.
admin.site.register(Description)
admin.site.register(ImageSize)
admin.site.register(Image)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Order_chart)
admin.site.register(Type)
admin.site.register(Rating)
admin.site.register(Coupon)
admin.site.register(Bank)
admin.site.register(Payment)
admin.site.register(Recipt)

admin.site.register(SubcategoryType)
admin.site.register(SubcategoryValue)
admin.site.register(ProductVariant)


admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Quote)
admin.site.register(CodeBlock)
admin.site.register(Video)
admin.site.register(Ad)
admin.site.register(List)
admin.site.register(Title)
admin.site.register(Imagec)
admin.site.register(Subtitle)
admin.site.register(BlogContent)
