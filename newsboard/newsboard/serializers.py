from rest_framework import serializers

from .models import Post, Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    author_name = serializers.CharField(max_length=100)
    content = serializers.CharField()
    creation_date = serializers.DateField(format="%d-%m-%Y",
                                          input_formats=["%d-%m-%Y"],
                                          required=False,)
    post_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author_name',
            'content',
            'creation_date',
            'post_id',
        ]


    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, comment, validated_data):
        comment.author_name = validated_data.get('author_name', comment.author_name)
        comment.content = validated_data.get('content', comment.content)
        comment.creation_date = validated_data.get('creation_date', comment.creation_date)
        comment.save()
        return comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(required=True, max_length=100)
    link = serializers.URLField()
    creation_date = serializers.DateField(format="%d-%m-%Y",
                                          input_formats=["%d-%m-%Y"],
                                          required=False,)
    amount_of_upvotes = serializers.IntegerField()
    author_name = serializers.CharField(max_length=100,
                                        required=False,)
    comments = CommentSerializer(many=True, read_only=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'link',
            'creation_date',
            'amount_of_upvotes',
            'author_name',
            'comments',
        ]

    def create(self, validated_data):
        comments_data = validated_data.pop("comments")
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            comment_data["post_id"] = post.id
            Comment.objects.create(**comment_data)
        return post

    def update(self, post, validated_data):
        post.title = validated_data.get('title', post.title)
        post.link = validated_data.get('link', post.link)
        post.creation_date = validated_data.get('creation_date', post.creation_date)
        post.amount_of_upvotes = validated_data.get(
            'amount_of_upvotes',
            post.amount_of_upvotes
        )
        post.author_name = validated_data.get('author_name', post.author_name)
        post.comments.set(validated_data.get('comments', post.comments))
        post.save()
        return post
