import { domainService } from '../services';

const state = {domains: [], currentDomain: {}, createdNewLink: {}};

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
    },
    createLink({ commit }, link) {
        domainService.createLink(link).then(result => {
            commit('setLink', result);
        })
    }
};

const mutations = {
    setDomains(state, allDomains) {
        state.domains = [...allDomains];
    },
    setCurrentDomain(state, domain) {
        state.currentDomain = domain;
    },
    setLink(state, createdNewLink) {
        state.createdNewLink = createdNewLink;
    }
};

const getters = {
    getDomains(state) {
        return state.domains
    },
    getCurrentDomain(state) {
        return state.currentDomain;
    },
    getCreatedNewLink(state) {
        return state.createdNewLink;
    }
};

export const domains = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
