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
            // answeredQuestions: {}
            answeredQuestions: []
        }
    },
    computed: {
        ...mapGetters({
            examResult: 'exams/getExamResult',
            personalizedQuestions: 'exams/getPersonalizedQuestions',
            nextQuestion: 'exams/getNextQuestion',
            statesLikelihoods: 'exams/getStatesLikelihoods',
            terminateTest: 'exams/getTerminateTest'
        }),
        exam() {
            return this.$store.getters['exams/getExam'](this.exam_id)
        },
        currentQuestion() {
            if (this.currentQuestionIndex == 0) {
                return this.personalizedQuestions.length > this.currentQuestionIndex ? this.personalizedQuestions[this.currentQuestionIndex] : null;
            }
            return this.nextQuestion;
        }
    },
    methods: {
        ...mapActions('exams', ['submitExam', 'fetchPersonalizedQuestions', 'submitQuestion', 'fetchStatesLikelihoods']),
        onSubmit(examId) {
            let lastIdx = this.form.choices.length - 1
            for (let i = 0; i < lastIdx; i++) {
                // each choice can only appear once in this.form.choices
                if (this.form.choices[i] == this.form.choices[lastIdx]) {
                    this.form.choices[i] = this.form.choices[lastIdx]
                    this.form.choices = this.form.choices.slice(0, lastIdx);
                }
            }
            // each question can only appear once in answeredQuestions
            // this.answeredQuestions[this.currentQuestion.id] = this.currentQuestion;
            // // pass list instead of object, so this is just reformatting
            // let answeredQuestions = [];
            // for (let key in this.answeredQuestions) {
            //     answeredQuestions.push(this.answeredQuestions[key]);
            // }
            this.answeredQuestions.push(this.currentQuestion);
            if (Object.keys(this.answeredQuestions).length == this.personalizedQuestions.length) {
                this.submitExam({"id": examId, "choices": this.form.choices, "states_likelihoods": this.statesLikelihoods,
                                 "answered_questions": this.answeredQuestions});
                this.show = true;
            } else {
                this.submitQuestion({"id": examId, "answered_questions": this.answeredQuestions, "choices": this.form.choices,
                                     "states_likelihoods": this.statesLikelihoods});
                let that = this;
                setTimeout(function(){ if (this.terminateTest) {
                        alert("Test terminated")
                        that.$router.push({name: 'domains'})
                    }
                }, 100);
                this.currentQuestionIndex = this.answeredQuestions.length;
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
        this.fetchStatesLikelihoods(this.exam_id);
    }
}
</script>