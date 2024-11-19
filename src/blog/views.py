import random

from django.http import HttpResponse
from faker import Faker

from blog.models import Blog, Entity


def create_blog(request):
    faker = Faker("UK")

    saved_data = Entity(
        blog=[
            Blog(
                name=faker.word(),
                text=faker.paragraph(nb_sentences=5),
                author=faker.first_name(),
                rating=random.randint(1, 10),
            )
            for _ in range(5)
        ],
        headline=faker.paragraph(nb_sentences=1),
    ).save()

    return HttpResponse(f"Done: {saved_data}")


def all_blogs(request):
    blogs = Entity.objects.all()

    print(blogs)
    return HttpResponse(f"Done: {[blog.headline for blog in blogs]}")
