import Vue from 'vue';
import VeeValidate from 'vee-validate';

import { store } from './store';
import { router } from './helpers';
import App from './App';

Vue.use(VeeValidate);
Vue.config.productionTip = false


new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
