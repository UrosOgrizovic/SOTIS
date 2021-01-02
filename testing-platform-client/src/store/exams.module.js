import { examService, choiceService, questionService } from '../services';

const state = {
    exams: [],
    questions: [],
    choices: [],
    examResult: {
        id: 0,
        choices: [],
        score: 0
    },
    examTakers: [],
    xml: {},
    personalizedQuestions: []
};

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
            commit('setExams', exams)
        })
    },
    addNewExam({commit}, data) {
        examService.addNewExam(data).then(exam => {
            commit('addExam', exam)
        })
    },
    deleteExam({commit}, data) {
        const id = data.id
        examService.deleteExam(data).then(() => {
            commit('deleteExam', id)
        })
    },
    generateKnowledgeSpace(_, examId) {
        examService.generateKnowledgeSpace(examId).then(() => {})
    },
    fetchExamTakers({ commit }, examId) {
        examService.getExamTakers(examId).then(students => {
            commit('setExamTakers', students)
        });
    },
    fetchXML({ commit }, examId) {
        examService.getXML(examId).then(result => {
            commit('setXML', result);
        })
    },
    fetchPersonalizedQuestions({commit}, examId) {
        examService.getPersonalizedQuestions(examId).then(result => {
            commit('setPersonalizedQuestions', result);
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
    },
    addExam(state, exam) {
        state.exams = [...state.exams, exam]
    },
    deleteExam(state, id) {
        const index = state.exams.findIndex(exam => exam.id == id)
        state.exams.splice(index, 1)
    },
    setExamTakers(state, students) {
        state.examTakers = [...students];
    },
    setXML(state, xml) {
        state.xml = xml;
    },
    setPersonalizedQuestions(state, questions) {
        state.personalizedQuestions = [...questions];
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
    },
    getExamTakers(state) {
        return state.examTakers;
    },
    getXML(state) {
        return state.xml;
    },
    getPersonalizedQuestions(state) {
        return state.personalizedQuestions;
    }
};

export const exams = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};