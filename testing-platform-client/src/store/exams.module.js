import { examService, choiceService, questionService } from '../services';

const state = {exams: [], questions: [], choices: [], examResult: {id: 0, choices: [], score: 0}};

const actions = {
    fetchAllExams({ commit }) {
        examService.getAll().then(exams => {
            commit('setExams', exams);
        })
    },
    fetchAllQuestions({ commit }) {
        questionService.getAll().then(questions => {
            commit('setQuestions', questions);
        })
    },
    fetchAllChoices({ commit }) {
        choiceService.getAll().then(choices => {
            commit('setChoices', choices);
        })
    },
    submitExam({ commit }, examChoices) {
        examService.submitExam(examChoices).then(result => {
            commit('setExamResult', result);
        })
    },
    fetchPersonalizedExams({ commit }, data) {
        examService.getPersonalizedExams(data).then(exams => {
            console.log(exams)
            commit('setExams', exams)
        })
    }
};

const mutations = {
    setExams(state, allExams) {
        state.exams = [...allExams];
    },
    setQuestions(state, allQuestions) {
        state.questions = [...allQuestions];
    },
    setChoices(state, allChoices) {
        state.choices = [...allChoices];
    },
    setExamResult(state, examResult) {
        state.examResult = [...[examResult]];
    }
};

const getters = {
    getAllExams(state) {
        return state.exams
    },
    getExam(state) {
        return (id) => {
            return state.exams.find(exam => exam.id == id)
        }
    },
    getAllQuestions(state) {
        return state.questions
    },
    getAllChoices(state) {
        return state.choices
    },
    getExamResult(state) {
        return state.examResult
    },
    getExamScore(state) {
        return state.examResult.score
    }
};

export const exams = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};