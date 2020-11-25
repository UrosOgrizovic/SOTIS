<template>
    <ul id="questions">
        <li v-for="question in questions" :key="question.id">
            {{question.id}}
        </li>
    </ul>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
export default {
    computed: {
        ...mapState({
            account: state => state.account
        }),
        ...mapGetters({questions: 'exams/getAllQuestions'}),
    },
    methods: {
        ...mapActions('exams', ['getAllQuestions'])
    }
}
</script>