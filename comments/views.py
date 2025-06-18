from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers import CommentSerializer


class CommentListAPIView(APIView):
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
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
