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
  amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date = models.DateField()
  description = models.TextField(default='', blank=True, null=True)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + str(self.date)

class Expense(models.Model):
  amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date = models.DateField()
  description = models.TextField(default='', blank=True, null=True)

  def save(self, *args, **kwargs):
    # Call the parent save() method to save in the DB
    super(Expense, self).save(*args, **kwargs) 

    # Need to think about how to update the aggregated spending amounts
    # on the BudgetItems when we delete Expense records
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
      item.save()

  def delete(self, *args, **kwargs):
    category = self.category
    
    # Call the parent save() method to save in the DB
    super(Expense, self).delete(*args, **kwargs)

    items_to_update = BudgetItem.objects.filter(
      category=category
    )

    for item in items_to_update:
      item.save()
    
    

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
  amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  spent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  notes = models.TextField(default='', blank=True, null=True)
  parent_budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

  def save(self, *args, **kwargs):
    print('saving BudgetItem')
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
    # We need to watch for the aggregation being null if there are no
    # expenses for this BudgetItem now. If so, make 'spent' zero.
    if aggregate_dict['amount__sum']:
      self.spent = aggregate_dict['amount__sum']
    else:
      self.spent = 0

    # Call the parent save() method to save in the DB
    super(BudgetItem, self).save(*args, **kwargs)

  def __str__(self):
    return str(self.amount) + ', ' + self.category.name + ', ' + self.parent_budget.title
