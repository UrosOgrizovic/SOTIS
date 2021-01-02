<template>
    <div>
        <el-form :model="examForm" ref="examForm" :rules="examRules" label-width="120px" style="width: 50%">
            <h2>New Exam</h2>
            <el-form-item label="Title" prop="title">
                <el-col :span="12"><el-input v-model="examForm.title"></el-input></el-col>
            </el-form-item>
            <el-form-item label="Subject" prop="subject">
                <el-select v-model="examForm.subject" placeholder="please select your subject">
                    <el-option v-for="subject in subjects" :key="subject.id" :label="subject.title" :value="subject.id">{{subject.title}}</el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onSubmit()">Submit</el-button>
            </el-form-item>
        </el-form>
        <ul>
            <li v-for="question in questions" :key="question.id">
                {{question.question_text}}
                <el-button @click="setChoiceFormVisibility(true, question)" icon="el-icon-circle-plus" circle></el-button>
                <ul>
                    <li v-for="choice in question.choices" :key="choice.id">{{choice.choice_text}}</li>
                </ul>
            </li>
        </ul>
        <el-button @click="setQuestionFormVisibility(true)" icon="el-icon-circle-plus" circle></el-button>

        <el-form v-if="questionFormVisibility" :model="questionForm" ref="questionForm" :rules="questionRules" label-width="120px" style="width: 50%">
            <h2>New Question</h2>
            <el-form-item label="Question Text" prop="question_text">
                <el-col :span="12"><el-input v-model="questionForm.question_text" type="textarea"></el-input></el-col>
            </el-form-item>
            <el-form-item>
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onAddQuestion()">Add</el-button>
            </el-form-item>
        </el-form>

        <el-form v-if="choiceFormVisibility" :model="choiceForm" ref="choiceForm" :rules="choiceRules" label-width="120px" style="width: 50%">
            <h2>New Choice</h2>
            <el-form-item label="Choice Text" prop="choice_text">
                <el-col :span="12"><el-input v-model="choiceForm.choice_text" type="textarea"></el-input></el-col>
            </el-form-item>
            <el-checkbox v-model="choiceForm.correct_answer">Correct Answer</el-checkbox>
            <el-form-item>
                <el-button style="float: right; margin-right: 10px;" type="primary" @click="onAddChoice()">Add</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'

export default {
    data() {
        return {
            examForm: {
                title: '',
                subject: null
            },
            questionForm: {
                question_text: ''
            },
            choiceForm: {
                choice_text: '',
                correct_answer: false
            },
            examRules: {
                title: [{type: 'string', required: true, message: 'Please add the exam title', trigger: 'change'}],
                subject: [{required: true, message: 'Please select a subject', trigger: 'change'}]
            },
            questionRules: {
                question_text: [{type: 'string', required: true, message: 'Please add the question text', trigger: 'change'}]
            },
            choiceRules: {
                choice_text: [{type: 'string', required: true, message: 'Please add the choice text', trigger: 'change'}]
            },
            questionFormVisibility: false,
            choiceFormVisibility: false,
            questions: [],
            chosenQuestion: null
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
            this.$refs['examForm'].validate((valid) => {
                if (valid) {
                    this.addNewExam({creator: this.user.id, ...this.examForm, questions: this.questions})
                }
            });
        },
        setQuestionFormVisibility(visibility) {
            this.questionFormVisibility = visibility;
        },
        setChoiceFormVisibility(visibility, question) {
            this.choiceFormVisibility = visibility;
            this.chosenQuestion = question;
        },
        onAddQuestion() {
            this.$refs['questionForm'].validate((valid) => {
                if (valid) {
                    const id = '_' + Math.random().toString(36).substr(2, 9);
                    this.questions.push({id, ...this.questionForm, choices: []});
                    this.setQuestionFormVisibility(false);
                    this.questionForm = {
                        question_text: ''
                    }
                }
            });
        },
        onAddChoice() {
            this.$refs['choiceForm'].validate(valid => {
                if (valid) {
                    const id = '_' + Math.random().toString(36).substr(2, 9);
                    this.chosenQuestion.choices.push({id, ...this.choiceForm});
                    this.setChoiceFormVisibility(false);
                    this.choiceForm = {
                        choice_text: ''
                    }
                }
            })
        }
    },
    mounted() {
        this.fetchSubjects()
    }
}
</script>