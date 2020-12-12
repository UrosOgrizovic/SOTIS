<template>
    <div>
        <el-form :model="form" label-width="120px">
            <h2>New Subject</h2>
            <el-form-item label="Title">
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
            this.addNewSubject({teacher: this.user.id, ...this.form})
            this.$router.push({path: 'domains'})
        }
    }
}
</script>