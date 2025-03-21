from django.contrib import admin
from django.contrib import admin
from .models import OTP,Detail,Questions
admin.site.register(OTP)
admin.site.register(Detail)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('Qdepartment','Qyear','Qsubject','Qquestion','type','marks')
    list_filter = ('Qdepartment','Qyear','Qsubject','type')
    search_fields = ('Qdepartment','Qyear','Qsubject','type')
admin.site.register(Questions,QuestionAdmin)
