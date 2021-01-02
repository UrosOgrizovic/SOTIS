<template>
    <div>
        <el-form :model="form" label-width="120px" :rules="rules" ref="form">
            <h3 style="float: left;">Test title: {{exam.title}}</h3><br><br>
            <ol style="margin-left: 0; margin-right: 0;">
                <div v-for="question in exam.questions" :key="question.id">
                    <li v-html="question.question_text"></li>
                    <el-form-item>
                        <el-checkbox v-for="choice in question.choices" :key="choice.id" :label="choice.choice_text" id="choice.id" @change="handleChange(choice.id)"></el-checkbox>
                    </el-form-item>
                </div>
            </ol>
            
            <el-form-item prop="choices">
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onSubmit(exam.id)">Submit</el-button>
            </el-form-item>
        </el-form>
        <div style="display: flex;" v-if="show && examResult.length > 0" id="score">
            <p>Score: {{examResult[0].score}}</p>
        </div>
        
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    data() {
        return {
            form: {
                choices: []
            },
            rules: {
                choices: [{type: 'array', required: true, message: 'Please select at least one answer', trigger: 'change'}]
            },
            show: false
        }
    },
    computed: {
        ...mapGetters({
            examResult: 'exams/getExamResult'
        }),
        exam() {
            return this.$store.getters['exams/getExam'](this.exam_id)
        }
    },
    methods: {
        ...mapActions('exams', ['submitExam']),
        onSubmit(examId) {
            this.submitExam({"id": examId, "choices": this.form.choices});
            this.show = true;          
        },
        handleChange(choiceId) {
            var idx = this.form.choices.indexOf(choiceId);
            if (idx == -1) {
                this.form.choices.push(choiceId);
            } else {
                this.form.choices.splice(idx, 1);
            }
        }
    },
    created() {
        this.exam_id = this.$route.params.exam_id
    }
}
</script>