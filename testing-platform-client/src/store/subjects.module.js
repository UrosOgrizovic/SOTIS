import { subjectService } from '../services';

const state = {subjects: []};

const actions = {
    fetchSubjects({ commit }) {
        subjectService.getAll().then(subjects => {
            commit('setSubjects', subjects);
        })
    },
    addNewSubject({ commit }, data) {
        subjectService.addNewSubject(data).then(subject => {
            commit('addSubject', subject);
        })
    }
};

const mutations = {
    setSubjects(state, allSubjects) {
        state.subjects = [...allSubjects];
    },
    addSubject(state, subject) {
        state.subjects = [...state.subjects, subject];
    }
};

const getters = {
    getSubjects(state) {
        return state.subjects
    }
};

export const subjects = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
