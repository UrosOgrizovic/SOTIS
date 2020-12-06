import { subjectService } from '../services';

const state = {subjects: []};

const actions = {
    fetchSubjects({ commit }) {
        subjectService.getAll().then(domains => {
            commit('setSubjects', domains);
        })
    }
};

const mutations = {
    setSubjects(state, allSubjects) {
        state.subjects = [...allSubjects];
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
