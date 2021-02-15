<template>
    <div>
        <h2 v-if='this.budget'>Budget > {{this.budget.title}} </h2>
        <h2 v-else>Budget</h2>

        <table>
            <tr>
                <th>Category</th>
                <th>Budget</th>
                <th>Spent</th>
                <th>Notes</th>
            </tr>
            <tr class='data-table--row' v-bind:key="item.id" v-for="item in this.budgetItems">
                <td v-if='categories' >{{ categories[item.category] }}</td>
                <td style='min-width: 20%;'>${{ item.amount }}</td>
                <td>${{ item.spent }}</td>
                <td>{{ item.notes }}</td>
                <td><button @click="this.deleteItem(item.id)">Delete</button></td>
            </tr>
        </table>

        <button
            type="button"
            class="btn"
            @click="showModal"
            >
            Add Category
        </button>

        <modal
            v-show="isModalVisible"
            @close="closeModal"    
        >
            <template v-slot:header>
                Add a category
                <button
                    type="button"
                    class="btn-close"
                    @click="closeModal"
                    aria-label='Close modal'
                >
                    x
                </button>
            </template>
            <template v-slot:body>
                <label for='item-category'>Category</label>
                <select id='item-category' name='category' v-model='nextCategory'>
                    <option v-bind:key=id v-for="(name, id) in categories" v-bind:value="id">
                        {{ name }}
                    </option>
                </select>
                
                <label for='item-amount'>Amount</label>
                <input id='item-amount' type='text' v-model="nextAmount">
            </template>
            <template v-slot:footer>
                <button @click="saveItem">
                    Save
                </button>
            </template>
        </modal>
    </div>
</template>

<script>
import axios from 'axios';

import modal from '../components/Modal';

export default {
    name: "BudgetDetail",
    components: {
        modal,
    },
    methods: {
        showModal() {
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        resetModalFields() {
            this.nextAmount = '';
            this.nextCategory = '';
        },
        getItems() {
            axios.get('http://localhost:8000/budget_items?', {
                params: {
                    parent_budget: this.$route.params.id,
                }
            })
            .then(res => {
                this.budgetItems = res.data;
            });
        },
        saveItem() {
            const newItem = {
                amount: this.nextAmount,
                category: this.nextCategory,
                notes: '',
                parent_budget: this.budget.id,
            };
            axios.post('http://localhost:8000/budget_items/', newItem)
            .then(() => {
                this.resetModalFields();
                this.closeModal();
                this.getItems();
            })
            .catch(error => {
                this.error = error;
            });
        },
        deleteItem(id) {
            axios.delete(`http://localhost:8000/budget_items/${id}/`)
            .then(() => {
                this.getItems();
            })
            .catch(error => {
                this.error = error;
            });
        }
    },
    mounted() {
        axios.get(`http://localhost:8000/budgets/${this.$route.params.id}`)
        .then(res => {
        this.budget = res.data;
        });

        this.getItems();
    },
    computed: {
        categories () {
            if (this.$store.state.categories == null) {
                return this.$store.state.categories;
            }
            // We don't want 'income' categories
            const filteredCategories = this.$store.state.categories.filter(category => {return category.cat_type === 2;});
            // Create a lookup table to make displaying category names easier
            const categoryMap = {};
            for (const category of filteredCategories) {
                categoryMap[category.id] = category.name;
            }
            return categoryMap;
        },
    },
    data () {
        return {
          budget: null,
          budgetItems: null,
          nextCategory: '',
          nextAmount: '',
          isModalVisible: false,
          error: null,
        }
    },
}
</script>

<style scoped>
</style>