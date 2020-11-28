import { examService, choiceService, questionService } from '../services';

const state = {exams: [], questions: [], choices: []};

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
    }
};
// import Vue from 'vue'
const mutations = {
    setExams(state, allExams) {
        state.exams = [...allExams];
    },
    setQuestions(state, allQuestions) {
        state.questions = allQuestions;
        state.questions = [...allQuestions];
    },
    setChoices(state, allChoices) {
        state.choices = [...allChoices];
    }
};

const getters = {
    getAllExams(state) {
        return state.exams
    },
    getAllQuestions(state) {
        return state.questions
    },
    getAllChoices(state) {
        return state.choices
    }
};

export const exams = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};