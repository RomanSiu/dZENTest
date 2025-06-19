from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .models import Comment, CommentAttachment
from .serializers import CommentSerializer


class CommentListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        sort_param = request.GET.get('sort', 'created_at')
        order = request.GET.get('order', 'desc')

        sort_fields = {
            'username': 'username',
            'email': 'email',
            'created_at': 'created_at',
        }
        sort_field = sort_fields.get(sort_param, 'created_at')
        if order == 'desc':
            sort_field = '-' + sort_field

        queryset = Comment.objects.filter(parent__isnull=True).order_by(sort_field)
        paginator = PageNumberPagination()
        paginator.page_size = 25
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        captcha_key = request.data.get('captcha_key')
        captcha_text = request.data.get('captcha_text')

        if not captcha_key or not captcha_text:
            return Response({'error': 'CAPTCHA required'}, status=400)

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response != captcha_text.lower():
                return Response({'error': 'CAPTCHA incorrect'}, status=400)
        except CaptchaStore.DoesNotExist:
            return Response({'error': 'CAPTCHA expired'}, status=400)

        if serializer.is_valid():
            comment = serializer.save(user=request.user)

            for file in request.FILES.getlist('attachments'):
                CommentAttachment.objects.create(
                    comment=comment,
                    file=file,
                    name=file.name
                )

            return Response(CommentSerializer(comment, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaptchaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        new_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(new_key)
        return Response({
            'key': new_key,
            'image_url': request.build_absolute_uri(image_url)
        })
