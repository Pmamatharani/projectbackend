from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP,Detail,Questions
from django.contrib.auth.hashers import make_password

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('otp',)




from rest_framework.validators import UniqueTogetherValidator

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Detail.objects.all(),
                fields=['department', 'year', 'subject'],
                message="This detail already exists."
            )
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Questions.objects.all(),
                fields=['Qdepartment', 'Qyear', 'Qsubject','Qquestion'],
                message="This question already exists."
            )
        ]   




class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def update_password(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")