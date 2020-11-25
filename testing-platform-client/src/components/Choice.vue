<template>
    <ul id="choices">
        {{ "aaa" }}
        {{ log(getAllChoices()) }}
        <!-- {{ log("AAAAAA " + resolvePromise(choices)) }} -->
        {{ log(choices)}}
        <!-- {{ choices.then(chcs => {log(chcs)}) }} -->
        <li v-for="choice in choices" :key="choice.id">
            aaaa {{choice.id}} | {{choice.choiceText}}
        </li>
    </ul>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
export default {
    computed: {
        ...mapState({
            account: state => state.account,
            exams: exams => exams.currentExams
        }),
        ...mapGetters({choices: 'exams/getAllChoices'}),
    },
    methods: {
        ...mapActions('exams', ['getAllChoices']),   
        log(item) {
            console.log(item);
        },
    }
}
</script>