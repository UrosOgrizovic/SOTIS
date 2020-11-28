<template>
    <ul id="exams">
        <li v-for="exam in exams" :key="exam.id">
            {{exam}} {{exam.questions[0]}}
        </li>
    </ul>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    computed: {
        ...mapGetters({exams: 'exams/getAllExams'}),
    },
    methods: {
        ...mapActions('exams', ['fetchAllExams'])
    },
    mounted() {
        this.fetchAllExams();
    }
}
</script>