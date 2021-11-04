from django.db import models
from django.contrib.auth.models import User

# Модели портала.

# Модель класса автор.
class Author(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    # функции формирования рейтинга
    def update_rating(self):
        result = 0
        user = self.id_user

        post_list = Post.objects.filter(id_author=self, type=Post.article)

        # суммарный рейтинг каждой статьи автора умножается на 3
        post_rating_list = post_list.values("rating")
        result = 3 * (sum(item["rating"] for item in post_rating_list))

        # суммарный рейтинг всех комментариев автора
        comment_rating_list = Comment.objects.filter(id_user=user).values("rating")
        result += sum(item["rating"] for item in comment_rating_list)

        # суммарный рейтинг всех комментариев к статьям автора
        for post in post_list:
            comment_in_post = Comment.objects.filter(id_post=post).values("rating")
            result += sum(item["rating"] for item in comment_in_post)

        self.rating = result
        self.save()

# Модель класса категории.
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)



# Модель класса Пост(Новость/Статья).
class Post(models.Model):
    article = "AR"
    news = "NW"
    POST_TYPE = [(article, 'Статья'), (news, 'Новость')]

    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPE, default=article)
    created = models.DateTimeField(auto_now_add=True)
    id_post_category = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    # увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.rating += 1
        self.save()

    # увеличивают/уменьшают рейтинг на единицу.
    def dislike(self):
        self.rating -= 1
        self.save()

    # (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        result = self.text[:124] + "..."
        return result

#Модель класса Пост-Категория(промежуточная)
class PostCategory(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель класса Комментарий.
class Comment(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField()



    # увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.rating += 1
        self.save()

    # увеличивают/уменьшают рейтинг на единицу.
    def dislike(self):
        self.rating -= 1
        self.save()