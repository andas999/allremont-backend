from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(RequestPhoto)
admin.site.register(RequestedService)
admin.site.register(Worker)
admin.site.register(WorkerPortfolioPhoto)
admin.site.register(WorkerPortfolio)
admin.site.register(Response)
