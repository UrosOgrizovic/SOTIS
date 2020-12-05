import { domainService } from '../services';

const state = {domains: []};

const actions = {
    fetchAllDomains({ commit }) {
        domainService.getAll().then(domains => {
            commit('setDomains', domains);
        })
    }
};

const mutations = {
    setDomains(state, allDomains) {
        state.domains = [...allDomains];
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
