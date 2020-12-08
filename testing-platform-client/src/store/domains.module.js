import { domainService } from '../services';

const state = {domains: [], currentDomain: {}};

const actions = {
    fetchAllDomains({ commit }) {
        domainService.getAll().then(domains => {
            commit('setDomains', domains);
        })
    },
    fetchDomain({ commit }, domainId) {
        domainService.get(domainId).then(domain => {
            commit('setCurrentDomain', domain);
        })
    }
};

const mutations = {
    setDomains(state, allDomains) {
        state.domains = [...allDomains];
    },
    setCurrentDomain(state, domain) {
        state.currentDomain = domain;
    }
};

const getters = {
    getDomains(state) {
        return state.domains
    },
    getCurrentDomain(state) {
        return state.currentDomain;
    }
};

export const domains = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
