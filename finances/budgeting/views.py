from rest_framework import viewsets

from .models import Category, CategoryType, Income, Expense, BudgetItem, Budget
from .serializers import CategorySerializer, CategoryTypeSerializer, IncomeSerializer, ExpenseSerializer, BudgetItemSerializer, BudgetSerialize

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer

class CategoryTypeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = CategoryType.objects.all()
  serializer_class = CategorySerializer

class IncomeViewSet(viewsets.ModelViewSet):
  queryset = Income.objects.all()
  serializer_class = IncomeSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
  queryset = Expense.objects.all()
  serializer_class = ExpenseSerializer

class BudgetViewSet(viewsets.ModelViewSet):
  queryset = Budget.objects.all()
  serializer_class = BudgetSerialize

class BudgetItemViewSet(viewsets.ModelViewSet):
  serializer_class = BudgetItemSerializer

  def get_queryset(self):
    queryset = BudgetItem.objects.all()
    budget = self.request.query_params.get('parent_budget', None)
    if budget is not None:
      queryset = queryset.filter(parent_budget=budget)
    return queryset