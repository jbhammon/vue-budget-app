from django.db import models

class CategoryType(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Category(models.Model):
  name = models.CharField(max_length=200)
  cat_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Income(models.Model):
  amount = models.IntegerField(default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date = models.DateField()
  description = models.TextField(default='', blank=True, null=True)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + str(self.date)

class Expense(models.Model):
  amount = models.IntegerField(default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date = models.DateField()
  description = models.TextField(default='', blank=True, null=True)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + str(self.date)

class Budget(models.Model):
  title = models.CharField(max_length=200)
  start_date = models.DateField()
  end_date = models.DateField()
  notes = models.TextField(default='', blank=True, null=True)

class BudgetItem(models.Model):
  amount = models.IntegerField(default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  notes = models.TextField(default='', blank=True, null=True)
  parent_budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + self.parent_budget.title
