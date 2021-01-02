<template>
    <!-- <div>
        <h2>Register</h2>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="firstName">First Name</label>
                <input type="text" v-model="user.first_name" v-validate="'required'" name="firstName" class="form-control" :class="{ 'is-invalid': submitted && errors.has('first_name') }" />
                <div v-if="submitted && errors.has('first_name')" class="invalid-feedback">{{ errors.first('first_name') }}</div>
            </div>
            <div class="form-group">
                <label for="lastName">Last Name</label>
                <input type="text" v-model="user.last_name" v-validate="'required'" name="lastName" class="form-control" :class="{ 'is-invalid': submitted && errors.has('last_name') }" />
                <div v-if="submitted && errors.has('last_name')" class="invalid-feedback">{{ errors.first('last_name') }}</div>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" v-model="user.email" v-validate="'required|email'" name="email" class="form-control" :class="{ 'is-invalid': submitted && errors.has('email') }" />
                <div v-if="submitted && errors.has('email')" class="invalid-feedback">{{ errors.first('email') }}</div>
            </div>
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" v-model="user.username" v-validate="'required'" name="username" class="form-control" :class="{ 'is-invalid': submitted && errors.has('username') }" />
                <div v-if="submitted && errors.has('username')" class="invalid-feedback">{{ errors.first('username') }}</div>
            </div>
            <div class="form-group">
                <label htmlFor="password">Password</label>
                <input type="password" v-model="user.password" v-validate="{ required: true, min: 6 }" name="password" class="form-control" :class="{ 'is-invalid': submitted && errors.has('password') }" />
                <div v-if="submitted && errors.has('password')" class="invalid-feedback">{{ errors.first('password') }}</div>
            </div>
            <div class="col-auto my-1">
                <label class="mr-sm-2" for="inlineFormCustomSelect">Preference</label>
                <select v-model="user.group" class="custom-select mr-sm-2" id="inlineFormCustomSelect">
                    <option value="Student">Student</option>
                    <option value="Expert">Expert</option>
                    <option value="Teacher">Teacher</option>
                </select>
            </div>
            <div class="form-group mt-4">
                <button class="btn btn-primary" :disabled="status.registering">Register</button>
                <img v-show="status.registering" src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==" />
                <router-link to="/login" class="btn btn-link">Cancel</router-link>
            </div>
        </form>
    </div> -->
    <div class="register">
        <el-card>
            <h2>Register</h2>
            <el-form
                class="register-form"
                @submit.native.prevent="handleSubmit"
            >
                <el-form-item prop="first_name">
                    <el-input v-model="user.first_name" placeholder="First Name" prefix-icon="fas fa-user"></el-input>
                </el-form-item>
                <el-form-item prop="last_name">
                    <el-input v-model="user.last_name" placeholder="Last Name" prefix-icon="fas fa-user"></el-input>
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="user.email" placeholder="Email" prefix-icon="fas fa-user"></el-input>
                </el-form-item>
                <el-form-item prop="username">
                    <el-input v-model="user.username" placeholder="Username" prefix-icon="fas fa-user"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="user.password"
                        placeholder="Password"
                        type="password"
                        prefix-icon="fas fa-lock"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-select v-model="user.group" placeholder="Group">
                        <el-option v-for="item in options"
                                   :key="item.value"
                                   :label="item.label"
                                   :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button
                        :loading="submitted"
                        class="register-button"
                        type="primary"
                        native-type="submit"
                        block
                    >
                        Register
                    </el-button>
                </el-form-item>
                <router-link to="/login" class="btn btn-link login">Cancel</router-link>
            </el-form>
        </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    data () {
        return {
            user: {
                first_name: '',
                last_name: '',
                email: '',
                username: '',
                password: '',
                group: ''
            },
            options: [
                {
                    label: 'Student',
                    value: 'Student'
                },
                {
                    label: 'Expert',
                    value: 'Expert'
                },
                {
                    label: 'Teacher',
                    value: 'Teacer'
                }
            ],
            submitted: false
        }
    },
    computed: {
        ...mapState('account', ['status'])
    },
    methods: {
        ...mapActions('account', ['register']),
        handleSubmit() {
            this.submitted = true;
            this.register(this.user);

        }
    }
};
</script>


<style scoped>
.register {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-button {
  width: 100%;
  margin-top: 40px;
}
.register-form {
  width: 290px;
}
.login {
  margin-top: 10px;
}
</style>

