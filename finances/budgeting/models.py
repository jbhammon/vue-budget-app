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

  def save(self, *args, **kwargs):
    # Need to think about how to update the aggregated spending amounts
    # on the BudgetItems when we create, update, or delete Expense records
    print('saved it bruh')
    items_to_update = BudgetItem.objects.filter(
      category=self.category
    )
    # This will make the query faster, but why doesn't it work??
    # .filter(
    #   parent_budget__start_date__gte=self.date
    # ).filter(
    #   parent_budget__end_date__lte=self.date
    # )
    for item in items_to_update:
      print(item)
      item.save()

    # Call the parent save() method to save in the DB
    super().save(*args, **kwargs) 

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + str(self.date)

class Budget(models.Model):
  title = models.CharField(max_length=200)
  start_date = models.DateField()
  end_date = models.DateField()
  notes = models.TextField(default='', blank=True, null=True)

  def __str__(self):
    return self.title

class BudgetItem(models.Model):
  amount = models.IntegerField(default=0)
  spent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  notes = models.TextField(default='', blank=True, null=True)
  parent_budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

  def save(self, *args, **kwargs):
    # calculate actual spending for this item
    start_date = self.parent_budget.start_date
    end_date = self.parent_budget.end_date
    aggregate_dict = Expense.objects.filter(
      category=self.category
    ).filter(
      date__gte=start_date
    ).filter(
      date__lte=end_date
    ).aggregate(
      models.Sum('amount')
    )
    self.spent = aggregate_dict['amount__sum']

    # Call the parent save() method to save in the DB
    super().save(*args, **kwargs)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + self.parent_budget.title
