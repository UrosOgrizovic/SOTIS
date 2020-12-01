<template>
    <div class="login">
        <el-card>
            <h2>Login</h2>
            <el-form
                class="login-form"
                @submit.native.prevent="handleSubmit"
            >
                <el-form-item prop="username">
                    <el-input v-model="username" placeholder="Username" prefix-icon="fas fa-user"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="password"
                        placeholder="Password"
                        type="password"
                        prefix-icon="fas fa-lock"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button
                        :loading="submitted"
                        class="login-button"
                        type="primary"
                        native-type="submit"
                        block
                    >
                        Login
                    </el-button>
                </el-form-item>
                <router-link to="/register" class="btn btn-link register">Register</router-link>
            </el-form>
        </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    data () {
        return {
            username: '',
            password: '',
            submitted: false,
        }
    },
    computed: {
        ...mapState('account', ['status'])
    },
    created () {
        // reset login status
        this.logout();
    },
    methods: {
        ...mapActions('account', ['login', 'logout']),
        handleSubmit () {
            this.submitted = true;
            const { username, password } = this;
            if (username && password) {
                this.login({ username, password })
            }
        }
    }
};
</script>


<style scoped>
.login {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-button {
  width: 100%;
  margin-top: 40px;
}
.login-form {
  width: 290px;
}
.register {
  margin-top: 10px;
}
</style>
