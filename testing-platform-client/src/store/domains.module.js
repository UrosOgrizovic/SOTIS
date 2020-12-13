import { domainService } from '../services';

const state = {domains: [], currentDomain: {}, isNewLink: false, newNode: {}, unattachedExams: []};

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
            commit('setIsNewLink', result);
        })
    },
    createNode({ commit }, node) {
        domainService.createNode(node).then(result => {
            commit('setNode', result);
        })
    },
    getUnattachedExamsForDomainId({ commit }, domainId) {
        domainService.getUnattachedExamsForDomainId(domainId).then(unattachedExams => {
            commit('setUnattachedExams', unattachedExams);
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
    setIsNewLink(state, isNewLink) {
        state.isNewLink = isNewLink;
    },
    setNode(state, newNode) {
        state.newNode = newNode;
    },
    setUnattachedExams(state, unattachedExams) {
        state.unattachedExams = unattachedExams;
    }
};

const getters = {
    getDomains(state) {
        return state.domains
    },
    getCurrentDomain(state) {
        return state.currentDomain;
    },
    getIsNewLink(state) {
        return state.isNewLink;
    },
    getNewNode(state) {
        return state.newNode;
    },
    getUnattachedExams(state) {
        return state.unattachedExams;
    }
};

export const domains = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
