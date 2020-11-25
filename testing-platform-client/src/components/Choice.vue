<template>
    <ul>
        {{ "zzz" }}
        <!-- {{ log(fetchAllChoices()) }} -->
        <!-- {{ log(JSON.parse(JSON.stringify(allChoices))) }} -->
        {{ log(choices) }}
        <!-- {{ getChoices() }} -->
        <li v-for="choice in choices" :key="choice.id">
            aaaa {{choice.id}} | {{choice.choiceText}}
        </li>
    </ul>
</template>

<script>
import { mapActions } from 'vuex'
// import { mapGetters, mapActions } from 'vuex'
export default {
    // data () {
    //     return {
    //         // choices: {},
    //     }
    // },
    computed: {
        choices: {
            cache: false,
            get: function () {
                return this.$store.state.exams.allChoices;
            }
        }
        // ...mapState({
            // account: state => state.account,
            // choices: exams => exams.allChoices
        // }),
        // ...mapState('exams', ['allChoices']),
        // ...mapGetters({choices: 'exams/getAllChoices'}),
        // choices() {
            // return this.$store.state.exams.choices
        // }
        // ...mapGetters({getAllChoices: 'exams/getAllChoices'}),
        // getChoices() {
        //     console.log(this.$store);
        //     return this.$store.state.exams.allChoices;
        // }

    },
    methods: {
        ...mapActions('exams', ['fetchAllChoices']),   
        log(item) {
            console.log(item);
        }
    },
    mounted() {
        this.fetchAllChoices();
        console.log("A");
        // console.log(this.$store)
        setTimeout(() => {console.log(this.$store.state.exams.choices)}, 1000)
        // console.log(JSON.parse(JSON.stringify(this.choices)));
        // console.log(this.getAllChoices);
    }
}
</script>