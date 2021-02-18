from django.contrib import admin
from .models import Category, CategoryType, Income, Expense, BudgetItem, Budget

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryType)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(BudgetItem)
admin.site.register(Budget)