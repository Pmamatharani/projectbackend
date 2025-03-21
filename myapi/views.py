
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.middleware.csrf import get_token
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
import random

from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, Detail, Questions
from .serializers import OTPSerializer, DetailSerializer, QuestionSerializer






#views for the login 



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            otp = ''.join(random.choices('0123456789', k=6))
            OTP.objects.update_or_create(user=user, defaults={'otp': otp})
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'mamatharani8143@gmail.com',
                [user.email],
                fail_silently=False,
            )
           

            return Response({
                'message': 'OTP sent to email',
                'email':user.email,
               
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


#views for the otp verification



class VerifyOTPView(APIView):

    def post(self, request):
        otp = request.data.get('otp')
        try:
            otp_obj = OTP.objects.get(otp=otp)
            user = otp_obj.user
            otp_obj.delete()
            refresh = RefreshToken.for_user(user)
            csrf_token = get_token(request)  # Generate CSRF token

            return Response({
                'message': 'OTP verified',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'csrf_token': csrf_token  # Include CSRF token in response
            }, status=status.HTTP_200_OK)
        
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        


#views for the resend otp



class ResendOTPView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = ''.join(random.choices('0123456789', k=6))
            OTP.objects.update_or_create(user=user, defaults={'otp': otp})
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                 settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP resent to email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#  Send OTP for Password Reset



class ForgotPasswordOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            otp = ''.join(random.choices('0123456789', k=6))  # Generate a 6-digit OTP
            OTP.objects.update_or_create(user=user, defaults={'otp': otp})

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)




#  Reset Password


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)  
            user.save()

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



#views for the departments and subjects adding


class DetailListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer

    def get(self, request, *args, **kwargs):
     return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


#views for the delete item in the deparments and subjects

class DeleteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = Detail.objects.get(id=item_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

#views for the update item in the deparments and subjects




class UpdateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = Detail.objects.get(id=item_id)
            serializer = DetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)




    #views for the questions creations

class QuestionListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

    #views for the delete functionality for the question delete



class DeleteQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            question = Questions.objects.get(id=id)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Questions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

#views for the delete functionality for the question delete




class UpdateQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            question = Questions.objects.get(id=id)
            serializer = QuestionSerializer(question, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Questions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



#views for the generations of questions

class GenerateQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = request.GET.get('Qdepartment')
        year = request.GET.get('Qyear')
        subject = request.GET.get('Qsubject')
        num_questions = int(request.GET.get('num_questions', 0))

        if not department or not year or not subject:
            return Response({"error": "Missing required parameters."}, status=400)

        questions = list(Questions.objects.filter(Qdepartment=department, Qyear=year, Qsubject=subject))

        if len(questions) < num_questions:
            return Response({"error": "Not enough questions available."}, status=400)

        random.shuffle(questions)
        selected_questions = questions[:num_questions]

        return Response({"questions": [q.Qquestion for q in selected_questions]})
    



#views  for the  generated send pdf through email

class SendPDFEmailView(APIView):
    
    def post(self, request):
        questions = request.data.get("questions", [])

        if not questions:
            return Response({"error": "No questions provided"}, status=400)
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 800, "Generated Question Paper")
        
        pdf.setFont("Helvetica", 12)
        y = 780
        for idx, question in enumerate(questions, start=1):
            pdf.drawString(50, y, f"{idx}. {question}")
            y -= 20

        pdf.save()
        pdf_buffer.seek(0)

        try:
            recipient_email = "mamatharani8143@gmail.com"  

            email = EmailMessage(
                subject="Generated Question Paper",
                body="Please find the attached question paper.",
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient_email],
            )

            email.attach("Question_Paper.pdf", pdf_buffer.getvalue(), "application/pdf")
            email.send()
            return Response({"message": "Email sent successfully!"})
        
        except Exception as e:   
             return Response({"error": str(e)}, status=500)
           
        
           
