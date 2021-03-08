<template>
    <div>
        <h2>Your Income</h2>
        <table>
            <tr class='data-table--row' v-bind:key="item.id" v-for="item in income">
                <td>{{ item.date }}</td>
                <td style='min-width: 20%;'>${{ item.amount }}</td>
                <td v-if='categories' >{{ categories[item.category] }}</td>
                <td>{{ item.description }}</td>
                <td><button @click="this.$store.dispatch('deleteIncomeItem', item.id)">Delete</button></td>
                <td><button @click="this.updateIncome(item)">Update</button></td>
            </tr>
        </table>

        <button
            type="button"
            class="btn"
            @click="showModal"
            >
            Add income
        </button>

        <ul>
            <li>
                
            </li>
        </ul>

        <modal
            v-show="isModalVisible"
            @close="closeModal"    
        >
            <template v-slot:header>
                Add an income
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
                <label for="date">Date:</label>
                <input type="date" id="date" name="date" v-model='nextDate'>

                <label for='income-amount'>Amount</label>
                <input id='income-amount' type='text' v-model='nextAmount'>

                <label for='income-category'>Category</label>
                <select id='income-category' name='category' v-model='nextCategory'>
                    <option v-bind:key=id v-for="(name, id) in categories" v-bind:value="id">
                        {{ name }}
                    </option>
                </select>
                
                <label for='income-description'>Description</label>
                <input id='income-description' type='text' v-model="nextDescription">
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
import modal from '../components/Modal';

export default {
    name: "Income",
    components: {
        modal,
    },
    methods: {
        showModal() {
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
            this.resetModalFields();
        },
        resetModalFields() {
            this.nextID = '';
            this.nextDate = '';
            this.nextAmount = '';
            this.nextCategory = '';
            this.nextDescription = '';
        },
        saveIncome(close) {
            if (this.nextID === '') {
                this.$store.dispatch('postIncomeItem', {date: this.nextDate, amount: this.nextAmount, description: this.nextDescription, category: this.nextCategory})
                .then(() => {
                    this.resetModalFields();
                    if (close) {
                        this.closeModal();
                    }
                })
                .catch(error => {
                    this.error = error;
                    this.errorState = true;
                });
            } else {
                this.$store.dispatch('putIncomeItem', {id: this.nextID, date: this.nextDate, amount: this.nextAmount, description: this.nextDescription, category: this.nextCategory})
                .then(() => {
                    this.resetModalFields();
                    if (close) {
                        this.closeModal();
                    }
                })
                .catch(error => {
                    this.error = error;
                    this.errorState = true;
                });
            }
        },
        updateIncome(item) {
            const prevDate = new Date(item.date);
            let year = prevDate.getFullYear().toString();
            let month = prevDate.getMonth() + 1;
            if (month < 10) {
                month = '0' + month.toString();
            } else {
                month = month.toString();
            }
            let date = prevDate.getDate();
            if (date < 10) {
                date = '0' + date.toString();
            } else {
                date = date.toString();
            }

            this.nextDate = year + '-' + month + '-' + date; 
            this.nextAmount = item.amount;
            this.nextCategory = item.category;
            this.nextDescription = item.description;
            this.nextID = item.id;
            this.showModal();
        },
    },
    computed: {
        income () {
            return this.$store.state.income;
        },
        categories () {
            if (this.$store.state.categories == null) {
                return this.$store.state.categories;
            }
            // We don't want 'expense' categories
            const filteredCategories = this.$store.state.categories.filter(category => {return category.cat_type === 1;});
            // Create a lookup table to make displaying category names easier
            const categoryMap = {};
            for (const category of filteredCategories) {
                categoryMap[category.id] = category.name;
            }
            return categoryMap;
        },
    },
    data() {
        return {
            nextID: '',
            nextDate: '',
            nextAmount: '',
            nextCategory: '',
            nextDescription: '',
            isModalVisible: false,
            error: null,
            errorState: false,
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