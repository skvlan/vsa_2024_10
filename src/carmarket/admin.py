from django.contrib import admin

from carmarket.models import Car, Card, ContactSeller, Favorite, SearchHistory

admin.site.register([Car, Card, Favorite, ContactSeller, SearchHistory])
