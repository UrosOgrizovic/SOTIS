import Vue from 'vue';
import Router from 'vue-router';

import Home from '@Components/home/Home'
import Login from '@Components/home/Login'
import Register from '@Components/home/Register'
import Domains from '@Components/domains/Domains'
import Exams from '@Components/exams/Exams'
import Exam from '@Components/exams/Exam'
import ExamForm from '@Components/exams/ExamForm'
import SubjectForm from '@Components/subjects/SubjectForm'
import ExamTakersList from '@Components/exams/ExamTakersList'
import States from '@Components/exams/States'

import { teacherOnlyGuard } from '@Helpers/guards';

Vue.use(Router);

export const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/exams/:exam_id', name: 'single_exam', component: Exam},
    { path: '/exams/:exam_id/students', name: 'exam_takers_list', component: ExamTakersList},
    { path: '/exams', component: Exams},
    { path: '/states/:exam_id', name: 'states', component: States},
    { path: '/domains', name: 'domains', component: Domains},
    { path: '/new-exam', component: ExamForm, beforeRouteEnter: teacherOnlyGuard},
    { path: '/new-subject', component: SubjectForm },

    // otherwise redirect to home
    { path: '*', redirect: '/' }
  ]
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})