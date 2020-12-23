import Vue from 'vue';
import Router from 'vue-router';

import Home from '../components/Home'
import Login from '../components/Login'
import Register from '../components/Register'
import Domains from '../components/Domains'
import Exams from '../components/Exams'
import Exam from '../components/Exam'
import ExamForm from '../components/ExamForm'
import SubjectForm from '../components/SubjectForm'
import ExamTakersList from '../components/ExamTakersList'

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
    { path: '/domains', component: Domains},
    { path: '/new-exam', component: ExamForm},
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