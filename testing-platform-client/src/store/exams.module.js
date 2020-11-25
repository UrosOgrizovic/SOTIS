import { examService, choiceService, questionService } from '../services';

const currentExams = {exams: [], questions: [], choices: {}};

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
    setExams(currentExams, allExams) {
        currentExams.exams = allExams;
    },
    setQuestions(currentExams, allQuestions) {
        currentExams.questions = allQuestions;
    },
    setChoices(currentExams, allChoices) {
        // Vue.set(currentExams, 'choices', allChoices);
        currentExams.choices = allChoices[0];
    }
};

const getters = {
    getAllExams: currentExams => {return currentExams.exams},
    getAllQuestions: currentExams => {return currentExams.questions},
    // getAllChoices: currentExams => { console.log(JSON.parse(JSON.stringify(currentExams))); return currentExams.choices}
    
    getAllChoices: currentExams => { return currentExams.choices }
    // getAllChoices: () => {return "AAA"}
};

export const exams = {
    namespaced: true,
    actions,
    mutations,
    getters,
    currentExams
};