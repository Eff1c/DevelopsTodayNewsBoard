from typing import Type, Union

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


def get_object(cls: Type[Union[Post, Comment]], pk: int):
    try:
        return cls.objects.get(pk=pk)
    except cls.DoesNotExist:
        raise Http404


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(APIView):
    def get(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ViewSet):
    def list(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        queryset = post.comments
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id: int) -> Response:
        validated_data = request.data
        validated_data["post_id"] = post_id
        serializer = CommentSerializer(validated_data)

        serializer = CommentSerializer(data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get(self, request, post_id: int, comment_id: int) -> Response:
        comment = get_object(Comment, comment_id)
        if comment.post_id != post_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id: int, comment_id: int) -> Response:
        comment = get_object(Comment, comment_id)
        if comment.post_id != post_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id: int, comment_id: int) -> Response:
        comment = get_object(Comment, comment_id)
        if comment.post_id != post_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpvoteView(APIView):
    def post(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        post.amount_of_upvotes += 1
        post.save()
        return Response({"message": "Post upvoted"}, status=status.HTTP_200_OK)


class DownvoteView(APIView):
    def post(self, request, post_id: int) -> Response:
        post = get_object(Post, post_id)
        post.amount_of_upvotes -= 1
        post.save()
        return Response({"message": "Post downvoted"}, status=status.HTTP_200_OK)
