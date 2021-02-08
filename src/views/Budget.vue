<template>
    <div>
        <h2>Your budget</h2>
        <button
            type='button'
            class='btn'
            @click='showModal'
        >
            Create budget
        </button>

        <table>
            <tr>
                <th>Title</th>
                <th>Dates</th>
            </tr>
        </table>

        <!-- <button 
            @click="this.$store.dispatch('postBudgetItem', {time_period: '2021-01-01', amount: nextAmount, description: nextDescription, category: nextCategory})">
            Add
        </button> -->

        <modal
            v-show='isModalVisible'
            @close='closeModal'
        >
            <template v-slot:header>
                Create a new budget
                <button
                    type='button'
                    class='btn-close'
                    @click='closeModal'
                    aria-label='Close modal'
                >
                    x
                </button>
            </template>
            <template v-slot:body>
                <label for='title'>Title</label>
                <input id='title' type='text' v-model='nextTitle'>

                <label for="start-date">Start Date:</label>
                <input type="date" id="start-date" name="start-date" v-model='nextStartDate'>

                <label for="end-date">End Date:</label>
                <input type="date" id="end-date" name="end-date" v-model='nextEndDate'>

                <label for='title'>Notes</label>
                <input id='title' type='text' v-model='nextNotes'>
            </template>
            <template v-slot:footer>
                <button @click='createBudget'>
                    Create
                </button>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '../components/Modal';

export default {
    name: "Budget",
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
        createBudget() {
            this.$store.dispatch('postBudget', {title: this.nextTitle, start_date: this.nextStartDate, end_date: this.nextEndDate, notes: ''})
            .then(() => {
                this.closeModal();
            })
            .catch(error => {
                this.error = error;
            });
        },
    },
    computed: {
        budget () {
            return this.$store.state.budget;
        },
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
            nextTitle: '',
            nextStartDate: '',
            nextEndDate: '',
            nextNotes: '',
            isModalVisible: false,
            error: null,
        }
    },
}
</script>

<style scoped>
table {
    border-collapse: collapse;
    width: 100%;
}
.data-table--row:hover {
    background-color: #E7E7E7;
}
.data-table--row td {
    margin: none;
}
</style>