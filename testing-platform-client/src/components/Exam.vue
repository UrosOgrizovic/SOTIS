<template>
    <ul id="exams">
        <li v-for="exam in exams" :key="exam.id">
            {{exam.id}}
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
        // ...mapGetters({exams: 'exams/getAllExams'}),
        ...mapGetters({exams: 'exams/getAllExams'}),
    },
    methods: {
        ...mapActions('exams', ['getAllExams'])
    }
    
}
</script>