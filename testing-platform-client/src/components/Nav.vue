<template>
    <el-row style="margin-bottom: 10%">
        <el-col :span="24" class="navbar__menu-box">
            <img style="width: 50px" src="../assets/logo.png" alt="" class="navbar__logo">
            <p class="navbar__title"><a href="/">Testing Platform</a></p>
            <ul class="el-menu el-menu--horizontal navbar__menu">
                <li class="el-menu-item"><router-link to="/">Home</router-link></li>
                <li class="el-menu-item"><router-link to="/domains">View Domains</router-link></li>
                <li class="el-menu-item"><router-link v-if="belongsToGroup('Teacher')" to="/exams">My Exams</router-link></li>
                <li class="el-menu-item"><router-link to="/login">Logout</router-link></li>
            </ul>
        </el-col>
    </el-row>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
    computed: {
        ...mapState({
            user: state => state.account.userObject
        }),
    },
    methods: {
        ...mapActions('account', ['fetchUserObject'])
    },
    mounted() {
        if(!Object.entries(this.user).length) {
            this.fetchUserObject()
        }
    }
};
</script>
<style>
    .navbar__logo {
        display: block;
        height: 60px;
        margin-left: 10%;
        margin-right: 10%;
    }
    .navbar__menu-box {
        background-color: #fff;
        box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: space-around;
    }
    .navbar__menu {
        float: right;
        background-color: #fff;
    }
    .navbar__dropdown-menu a {
        color: inherit;
        text-decoration: none;
    }
    .navbar__title {
        margin-top: 0;
        margin-bottom: 0;
        margin-left: 12px;
        height: 60px;
        line-height: 60px;
        font-size: 1.5em;
        font-weight: bold;
    }
    .navbar__title a {
        color: #48576a;
        text-decoration: none;
    }
</style>