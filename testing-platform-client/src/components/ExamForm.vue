<template>
    <div>
        <el-form :model="form" label-width="120px">
            <h2>New Exam</h2>
            <el-form-item label="Title">
                <el-col :span="12"><el-input v-model="form.title"></el-input></el-col>
            </el-form-item>
            <el-form-item label="Subject">
                <el-select v-model="form.subject" placeholder="please select your subject">
                    <el-option v-for="subject in subjects" :key="subject.id" :label="subject.title" :value="subject.id">{{subject.title}}</el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onSubmit()">Submit</el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'

export default {
    data() {
        return {
            form: {
                title: '',
                subject: null
            }
        }
    },
    computed: {
        ...mapGetters({
            subjects: 'subjects/getSubjects'
        }),
        ...mapState({
            user: state => state.account.userObject
        })
    },
    methods: {
        ...mapActions('subjects', ['fetchSubjects']),
        ...mapActions('exams', ['addNewExam']),
        onSubmit() {
            console.log(this.user)
            this.addNewExam({creator: this.user.id, ...this.form})
        }
    },
    mounted() {
        this.fetchSubjects()
    }
}
</script>