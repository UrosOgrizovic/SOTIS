<template>
    <div>
        <router-link to="new-exam">New Exam</router-link>
        <el-table
            :data="exams"
            style="width: 100%">
            <el-table-column
                prop="title"
                label="Exam"
                width="180">
            </el-table-column>
            <el-table-column
                prop="subject.title"
                label="Subject"
                width="180">
            </el-table-column>
            <el-table-column
                prop="creator.username"
                label="Author"
                width="180">
            </el-table-column>
            <el-table-column
                fixed="right"
                label="Operations"
                width="120">
                <template slot-scope="scope">
                    <el-button @click="chooseExam(scope.$index)" type="text" size="small">Choose</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    data() {
        return {
            show: false
        }
    },
    computed: {
        ...mapGetters({exams: 'exams/getAllExams'})
    },
    methods: {
        ...mapActions('exams', ['fetchPersonalizedExams', 'fetchAllExams']),
        chooseExam(index) {
            if (!this.exams.length) {
                console.log("Exams list is empty!")
                return;
            }
            const chosenExam = this.exams[index]
            this.$router.push({name: 'single_exam', params: {'exam_id': chosenExam.id}})
        }
    },
    mounted() {
        if (this.$route.query.domain_id) {
            this.fetchPersonalizedExams({id: this.$route.query.domain_id});
        } else {
            this.fetchAllExams()
        }
    }
}
</script>