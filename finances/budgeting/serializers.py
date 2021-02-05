from rest_framework import serializers
from .models import Category, CategoryType, Income, Expense, Budget, BudgetItem

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class CategoryTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
  date = serializers.DateField(format='%b %d, %Y')
  class Meta:
    model = Income
    fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
  date = serializers.DateField(format='%b %d, %Y')
  class Meta:
    model = Expense
    fields = ['id', 'amount', 'category', 'date', 'description']

class BudgetSerialize(serializers.ModelSerializer):
  class Meta:
    model = Budget
    fields = '__all__'

class BudgetItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = BudgetItem
    fields = '__all__'