<template>
    <ul id="questions">
        <li v-for="question in questions" :key="question.id">
            {{question}}
        </li>
    </ul>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    computed: {
        ...mapGetters({questions: 'exams/getAllQuestions'}),
    },
    methods: {
        ...mapActions('exams', ['fetchAllQuestions'])
    },
    mounted() {
        this.fetchAllQuestions();
    }
}
</script>