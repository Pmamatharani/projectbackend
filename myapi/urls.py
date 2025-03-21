from django.urls import path
from .views import (
    LoginView, VerifyOTPView, ResendOTPView, 
    DetailListCreate, QuestionListCreate, 
    GenerateQuestionsView, DeleteItemView, UpdateItemView, 
    DeleteQuestionView, UpdateQuestionView,ForgotPasswordOTPView,ResetPasswordView , SendPDFEmailView
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend/', ResendOTPView.as_view(), name='resend'),
    path('ForgotPasswordOTPView/',ForgotPasswordOTPView.as_view(),name='ForgotPasswordOTPView'),
    path('ResetPasswordView/',ResetPasswordView.as_view(),name='ResetPasswordView'),

   # Detail Endpoints
    path('detail/', DetailListCreate.as_view(), name='detail'),
    path('delete_item/<int:item_id>/', DeleteItemView.as_view(), name='delete_item'),
    path('update_item/<int:item_id>/', UpdateItemView.as_view(), name='update_item'),

    # Question Endpoints
    path('question/', QuestionListCreate.as_view(), name='question'),
    path('delete_question/<int:id>/', DeleteQuestionView.as_view(), name='delete_question'),
    path('update_question/<int:id>/', UpdateQuestionView.as_view(), name='update_question'),

    # Generate Questions
    path('generate_questions/', GenerateQuestionsView.as_view(), name='generate_questions'),
    path('SendPDFEmailView/', SendPDFEmailView.as_view(),name="SendPDFEmailView"),
    
]
