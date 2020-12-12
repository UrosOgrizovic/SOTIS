import { domainService } from '../services';

const state = {domains: []};

const actions = {
    fetchAllDomains({ commit }) {
        domainService.getAll().then(domains => {
            commit('setDomains', domains);
        })
    },
    deleteDomain({ commit }, data) {
        const id = data.id
        domainService.deleteDomain(data).then(() => {
            commit('deleteDomain', id);
        })
    },
    addStudentToDomain({ commit }, data) {
        console.log(commit)
        domainService.addStudentToDomain(data);
    }
};

const mutations = {
    setDomains(state, allDomains) {
        state.domains = [...allDomains];
    },
    deleteDomain(state, id) {
        const index = state.domains.findIndex(domain => domain.id == id)
        state.domains.splice(index, 1)
    }
};

const getters = {
    getDomains(state) {
        return state.domains
    }
};

export const domains = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
