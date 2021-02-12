<template>
    <div>
        <h2 v-if='this.budget'>Budget > {{this.budget.title}} </h2>
        <h2 v-else>Budget</h2>

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
                <button @click="saveIncome(true)">
                    Save and Close
                </button>
                <button @click="saveIncome(false)">
                    Save and add another
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
    },
    mounted() {
      axios.get(`http://localhost:8000/budgets/${this.$route.params.id}`)
      .then(res => {
        this.budget = res.data;
      });
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
          nextCategory: '',
          nextAmount: '',
          isModalVisible: false,
        }
    },
}
</script>

<style scoped>
</style>