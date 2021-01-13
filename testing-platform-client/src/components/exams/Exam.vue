<template>
    <div>
        <el-form :model="form" label-width="120px" :rules="rules" ref="form">
            <h3 style="float: left;">Test title: {{exam.title}}</h3><br><br>
            <div v-if="currentQuestion">
                <li v-html="currentQuestion.question_text"></li>
                <el-form-item>
                    <el-checkbox v-for="choice in currentQuestion.choices" :key="choice.id" :label="choice.choice_text" id="choice.id" @change="handleChange(choice.id)"></el-checkbox>
                </el-form-item>
                <el-form-item prop="choices">
                    <el-button style="float: right; margin-right: 10px;" type="primary" @click="onSubmit(exam.id)">Add answer</el-button>
                </el-form-item>
            </div>
            <div v-else>
                There are no questions!
            </div>
            
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
            show: false,
            currentQuestionIndex: 0,
            answeredQuestions: []
        }
    },
    computed: {
        ...mapGetters({
            examResult: 'exams/getExamResult',
            personalizedQuestions: 'exams/getPersonalizedQuestions'
        }),
        exam() {
            return this.$store.getters['exams/getExam'](this.exam_id)
        },
        currentQuestion() {
            return this.personalizedQuestions.length > this.currentQuestionIndex ? this.personalizedQuestions[this.currentQuestionIndex] : null;
        }
    },
    methods: {
        ...mapActions('exams', ['submitExam', 'fetchPersonalizedQuestions', 'submitQuestion']),
        onSubmit(examId) {
            if ((this.currentQuestionIndex + 1) == this.personalizedQuestions.length) {
                this.submitExam({"id": examId, "choices": this.form.choices});
                this.show = true;  
            } else {
                this.answeredQuestions.push(this.currentQuestion);
                this.submitQuestion({"answered_questions": this.answeredQuestions, "choices": this.form.choices});
                this.currentQuestionIndex += 1;
            }
                    
        },
        handleChange(choiceId) {
            const idx = this.form.choices.indexOf(choiceId);
            if (idx == -1) {
                this.form.choices.push(choiceId);
            } else {
                this.form.choices.splice(idx, 1);
            }
        }
    },
    created() {
        this.exam_id = this.$route.params.exam_id
        this.fetchPersonalizedQuestions(this.exam_id)
    }
}
</script>