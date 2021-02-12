<template>
    <div>
        <h2 v-if='this.budget'>Budget > {{this.budget.title}} </h2>
        <h2 v-else>Budget</h2>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "BudgetDetail",
    components: {},
    methods: {},
    create() {
      axios.get(`http://localhost:8000/budgets/${this.$router.query.id}`)
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
        }
    },
}
</script>

<style scoped>
</style>