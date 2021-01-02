<template>
    <div>
        <el-form :model="form" ref="subjectForm" :rules="rules" label-width="120px" style="width: 50%">
            <h2>New Subject</h2>
            <el-form-item label="Title" prop="title">
                <el-col :span="12"><el-input v-model="form.title"></el-input></el-col>
            </el-form-item>
            <el-form-item>
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onSubmit()">Submit</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
    data() {
        return {
            form: {
                title: ''
            },
            rules: {
                title: [{type: 'string', required: true, message: 'Please add the exam title', trigger: 'change'}]
            }
        }
    },
    computed: {
        ...mapState({
            user: state => state.account.userObject
        })
    },
    methods: {
        ...mapActions('subjects', ['addNewSubject']),
        onSubmit() {
            this.$refs['subjectForm'].validate((valid) => {
                if (valid) {
                    this.addNewSubject({teacher: this.user.id, ...this.form});
                    this.$router.push({path: 'domains'});
                }
            });
        }
    }
}
</script>