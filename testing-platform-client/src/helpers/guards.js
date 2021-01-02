export const teacherOnlyGuard = (to, from, next) => {
    const store = require('../store')['store'];
    const user = store.getters['account/getUserObject'];

    if(user && user.groups && user.groups.includes('Teacher')) {
        next()
    } 

    next('/login')
}