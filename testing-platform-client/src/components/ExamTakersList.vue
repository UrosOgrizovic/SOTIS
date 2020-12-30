<template>
    <div>
        <el-table
            :data="students"
            style="width: 100%">
            <el-table-column
                prop="username"
                label="Username"
                width="180">
            </el-table-column>
            <el-table-column
                prop="first_name"
                label="First Name"
                width="180">
            </el-table-column>
            <el-table-column
                prop="last_name"
                label="Last Name"
                width="180">
            </el-table-column>
        </el-table>
        <el-button style="margin-top: 1em" @click="generateKnowledgeSpace(examId)">
            Generate Knowledge Space
        </el-button>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    data() {
        return {
            examId: null,
            displaySuccessMessage: false
        }
    },
    computed: {
        ...mapGetters({
            students: 'exams/getExamTakers'
        })
    },
    methods: {
        ...mapActions('exams', ['fetchExamTakers', 'generateKnowledgeSpace']),
    },
    mounted() {
        this.examId = this.$route.params.exam_id;
        this.fetchExamTakers(this.examId);
    }
}
</script>