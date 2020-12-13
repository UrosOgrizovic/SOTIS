import Vue from 'vue';

import ElementUI from 'element-ui';
import VueSimpleAlert from "vue-simple-alert";

import { store } from './store';
import { router } from './helpers';
import App from './App';
import './plugins/element.js'

import '../styles/login-register.scss';

// Vue.use(VeeValidate);
Vue.use(ElementUI)
Vue.use(VueSimpleAlert)

Vue.config.productionTip = false

Vue.mixin({
    methods: {
        belongsToGroup(group) {
            const user = this.$store.getters['account/getUserObject']
            if(user && user.groups) {
                return user.groups.includes(group);
            } 
            return false
        }
    }
})


new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
