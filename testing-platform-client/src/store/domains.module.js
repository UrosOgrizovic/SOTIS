import { domainService } from '../services';

const state = {domains: [], currentDomain: {}, isNewLink: false, newNode: {}, unattachedExams: [], domainGED: 0};

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
    async createNode({ commit }, node) {
        domainService.createNode(node).then(result => {
            commit('setNode', result);
        })
    },
    deleteDomain({ commit }, data) {
        const id = data.id
        domainService.deleteDomain(data).then(() => {
            commit('deleteDomain', id);
        })
    },
    addStudentToDomain({ commit }, data) {
        console.log(commit);
        domainService.addStudentToDomain(data);
    },
    fetchDomainGED({ commit }, domainId) {
        domainService.getDomainGED(domainId).then(result => {
            commit('setGED', result);
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
    },
    deleteDomain(state, id) {
        const index = state.domains.findIndex(domain => domain.id == id);
        state.domains.splice(index, 1);
    },
    setGED(state, ged) {
        state.domainGED = ged;
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
    },
    getDomainGED(state) { 
        return state.domainGED;
    }
};

export const domains = {
    namespaced: true,
    actions,
    mutations,
    getters,
    state
};
