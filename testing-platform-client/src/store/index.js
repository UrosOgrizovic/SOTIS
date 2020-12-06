import Vue from 'vue';
import Vuex from 'vuex';

import { account } from './account.module';
import { exams } from './exams.module';
import { domains } from './domains.module';
import { subjects } from './subjects.module';

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        account,
        exams,
        domains,
        subjects
    }
});