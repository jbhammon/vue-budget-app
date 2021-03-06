import { createStore } from 'vuex'
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

const store = createStore({
  state () {
    return {
      budget: [],
      expenses: [],
      income: [],
    }
  },
  actions: {
    init (context) {
      context.dispatch('getBudgets');
      context.dispatch('getCategoryItems');
      context.dispatch('getIncomeItems');
      context.dispatch('getExpenseItems');
    },
    // getBudgetItems (context) {
    //   axios.get('http://localhost:8000/budget_items/')
    //   .then(res => {
    //     context.commit('storeSetBudget', res.data);
    //   })
    //   .catch(err => {
    //     context.commit('storeSetBudgetError', err);
    //   });
    // },
    getCategoryItems (context) {
      axios.get('http://localhost:8000/category/')
      .then(res => {
        context.commit('storeSetCategories', res.data);
      })
      .catch(err => {
        context.commit('storeSetCategoriesError', err);
      });
    },
    getIncomeItems (context) {
      axios.get('http://localhost:8000/income/')
      .then(res => {
        context.commit('storeSetIncome', res.data);
      })
      .catch(err => {
        context.commit('storeSetIncomeError', err);
      });
    },
    getExpenseItems (context) {
      axios.get('http://localhost:8000/expenses/')
      .then(res => {
        context.commit('storeSetExpenses', res.data);
      })
      .catch(err => {
        context.commit('storeSetExpensesError', err);
      });
    },
    postBudgetItem (context, item) {
      axios.post('http://localhost:8000/budget_items/', item)
      .then(() => {
        context.dispatch('getBudgetItems');
      });
    },
    postIncomeItem (context, item) {
      return new Promise((resolve, reject) => {
        axios.post('http://localhost:8000/income/', item)
        .then(res => {
          context.dispatch('getIncomeItems');
          resolve(res);
        })
        .catch(error => {
          // should have an error dispatch here
          reject(error);
        });
      });
    },
    putIncomeItem (context, item) {
      const {id, ...putItem} = item;
      return new Promise((resolve, reject) => {
        axios.put(`http://localhost:8000/income/${id}/`, putItem)
        .then(res => {
          context.dispatch('getIncomeItems');
          resolve(res);
        })
        .catch(error => {
          // should have an error dispatch here
          reject(error);
        });
      });
    },
    postExpenseItem (context, item) {
      return new Promise((resolve, reject ) => {
        axios.post('http://localhost:8000/expenses/', item)
        .then(res => {
          context.dispatch('getExpenseItems');
          resolve(res);
        })
        .catch(error => {
          // should have an error dispatch here
          reject(error);
        });
      });
    },
    putExpenseItem (context, item) {
      const {id, ...putItem} = item;
      return new Promise((resolve, reject) => {
        axios.put(`http://localhost:8000/expenses/${id}/`, putItem)
        .then(res => {
          context.dispatch('getExpenseItems');
          resolve(res);
        })
        .catch(error => {
          // should have an error dispatch here
          reject(error);
        });
      });
    },
    deleteBudgetItem (context, id) {
      axios.delete(`http://localhost:8000/budget_items/${id}/`)
      .then(() => {
        context.dispatch('getBudgetItems');
      });
    },
    deleteIncomeItem (context, id) {
      axios.delete(`http://localhost:8000/income/${id}/`)
      .then(() => {
        context.dispatch('getIncomeItems');
      });
    },
    deleteExpenseItem (context, id) {
      axios.delete(`http://localhost:8000/expenses/${id}/`)
      .then(() => {
        context.dispatch('getExpenseItems');
      });
    },
    getBudgets (context) {
      axios.get('http://localhost:8000/budgets/')
      .then(res => {
        context.commit('storeSetBudgets', res.data);
      })
      .catch(err => {
        context.commit('storeSetBudgetsError', err);
      });
    },
    postBudget (context, budget) {
      return new Promise((resolve, reject) => {
        axios.post('http://localhost:8000/budgets/', budget)
        .then(res => {
          context.dispatch('getBudgets');
          resolve(res);
        })
        .catch(error => {
          reject(error);
        });
      });
    },
  },
  mutations: {
    storeSetBudget(state, newItems) {
      state.budgets = [...newItems];
    },
    storeSetBudgetError(state, error) {
      console.error(error);
    },

    storeSetCategories(state, newItems) {
      state.categories = [...newItems];
    },
    storeSetCategoriesError(state, error) {
      console.error(error);
    },

    storeSetIncome(state, newItems) {
      state.income = [...newItems];
    },
    storeSetIncomeError(state, error) {
      console.error(error);
    },

    storeSetExpenses(state, newItems) {
      state.expenses = [...newItems];
    },
    storeSetExpensesError(state, error) {
      console.error(error);
    },

    storeSetBudgets(state, newItems) {
      state.budgets = [...newItems];
    },
    storeSetBudgetsError(state, error) {
      console.error(error);
    },

    addExpense (state, newAmount) {
      const id = uuidv4();
      state.expenses = [
        ...state.expenses, 
        {
          id: id, 
          amount: parseInt(newAmount)
        }
      ];
    },
    delExpense (state, id) {
      state.expenses = state.expenses.filter(expense => expense.id !== id);
    },
    addIncome (state, newAmount) {
      const id = uuidv4();
      state.income = [
        ...state.income, 
        {
          id: id, 
          amount: parseInt(newAmount)
        }
      ];
    },
    delIncome (state, id) {
      state.income = state.income.filter(income => income.id !== id);
    },
  }
});

export default store;