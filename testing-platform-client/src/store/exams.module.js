import { examService, choiceService, questionService } from '../services';

const currentExams = {exams: null, questions: null, choices: null};

const actions = {
    getAllExams({ commit }) {
        examService.getAll().then(exams => {
            commit('getAllExams', exams);
        })
    },
    getAllQuestions({ commit }) {
        questionService.getAll().then(questions => {
            commit('getAllQuestions', questions);
        })
    },
    getAllChoices({ commit }) {
        choiceService.getAll().then(choices => {
            commit('getAllChoices', choices);
        })
        
    }
};

const mutations = {
    getAllExams(allExams) {
        currentExams.exams = allExams;
    },
    getAllQuestions(allQuestions) {
        currentExams.questions = allQuestions;
    },
    getAllChoices(allChoices) {
        currentExams.choices = allChoices;
    }
};

const getters = {
    getAllExams: () => {return examService.getAll()},
    getAllQuestions: () => {return questionService.getAll()},
    getAllChoices: () => {return choiceService.getAll()}
};

export const exams = {
    namespaced: true,
    actions,
    mutations,
    getters,
    currentExams
};