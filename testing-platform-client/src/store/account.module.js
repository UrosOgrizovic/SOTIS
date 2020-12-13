import { userService } from '../services';
import { router } from '../helpers';

const user = JSON.parse(localStorage.getItem('user'));
const state = {
    status: { loggedIn: !!user },
    user: user,
    students: [],
    userObject: {}
}

const actions = {
    login({ dispatch, commit }, { username, password }) {
        commit('loginRequest', { username });
    
        userService.login(username, password)
            .then(
                user => {
                    commit('loginSuccess', user);
                    router.push('/');
                },
                error => {
                    commit('loginFailure', error);
                    dispatch('alert/error', error, { root: true });
                }
            );
    },
    logout({ commit }) {
        userService.logout();
        commit('logout');
    },
    register({ commit }, user) {
        commit('registerRequest', user);
    
        userService.register(user)
            .then(
                user => {
                    commit('registerSuccess', user);
                    router.push('/login');
                },
                error => {
                    commit('registerFailure', error);
                }
            );
    },
    fetchUserObject({commit}) {
        userService.fetchUserObject()
            .then(
                user => {
                    commit('setUserObject', user)
                }
            )
    },
    fetchStudents({commit}) {
        userService.fetchStudents()
            .then(users => {
                commit('setStudents', users)
            })
    }
};

const mutations = {
    loginRequest(state, user) {
        state.status = { loggingIn: true };
        state.user = user;
    },
    loginSuccess(state, user) {
        state.status = { loggedIn: true };
        state.user = user;
    },
    loginFailure(state) {
        state.status = {};
        state.user = null;
    },
    logout(state) {
        state.status = {};
        state.user = null;
    },
    registerRequest(state) {
        state.status = { registering: true };
    },
    registerSuccess(state) {
        state.status = {};
    },
    registerFailure(state) {
        state.status = {};
    },
    setUserObject(state, user) {
        state.userObject = user
    },
    setStudents(state, users) {
        state.students = [...users]
    }
};


const getters = {
    getUserObject(state) {
        return state.userObject
    },
    getStudents(state) {
        return state.students
    }
};

export const account = {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};