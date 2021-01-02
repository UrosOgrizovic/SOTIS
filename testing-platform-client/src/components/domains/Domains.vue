<template>
    <div>
        <router-link v-if="belongsToGroup('Teacher')" to="new-subject">New Subject</router-link>
        <el-table
            :data="domains"
            style="width: 100%">
            <el-table-column
                prop="title"
                label="Domain Title"
                width="180">
            </el-table-column>
            <el-table-column
                prop="subject.title"
                label="Subject"
                width="180">
            </el-table-column>
            <el-table-column
                prop="subject.description"
                label="Description"
                width="400">
            </el-table-column>
            <el-table-column
                fixed="right"
                label="Actions"
                width="240">
                <template slot-scope="scope">
                    <el-button v-if="belongsToGroup('Teacher')" @click="openAddStudentModal(scope.$index)" type="text" size="small">Add student</el-button>
                    <el-button @click="chooseDomain(scope.$index)" type="text" size="small">View</el-button>
                    <el-button v-if="belongsToGroup('Teacher')" @click="openDeleteDomainModal(scope.$index)" type="text" size="small">Delete</el-button>
                </template>
            </el-table-column>

        </el-table>
        <confirm-modal title="Are you sure?" ref="confirm"></confirm-modal>
        <el-dialog :title="'Add students'" :visible.sync="studentDialogVisible" width="30%">
            <el-form :model="addStudentForm" label-width="120px">
                <el-form-item label="Student">
                    <el-select v-model="addStudentForm.student" placeholder="Select Student">
                        <el-option v-for="student in students" :key="student.id" :label="student.username" :value="student.id">{{student.username}}</el-option>
                    </el-select>
                </el-form-item>     
            </el-form>       
            <span slot="footer" class="dialog-footer">
            <el-button @click="studentDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="addStudent">Confirm</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import ConfirmModal from '@Components/shared/ConfirmModal';

export default {
    components: {
        ConfirmModal
    },
    data() {
        return {
            show: false,
            studentDialogVisible: false,
            addStudentForm: {
                student: null
            },
            chosenDomain: null
        }
    },
    computed: {
        ...mapGetters({
            domains: 'domains/getDomains',
            students: 'account/getStudents'
        })
    },
    methods: {
        ...mapActions('domains', ['fetchAllDomains', 'deleteDomain', 'addStudentToDomain']),
        ...mapActions('account', ['fetchStudents']),
        chooseDomain(index) {
            if (!this.domains.length) {
                console.log("Domains list is empty!")
                return;
            }

            const chosenDomain = this.domains[index]
            this.$router.push({path: 'exams', query: {'domain_id': chosenDomain.id}})
        },
        openDeleteDomainModal(index) {
            this.$refs.confirm.show().then(() => {
                const chosenDomain = this.domains[index]
                this.deleteDomain(chosenDomain)
            })
            .catch(() => {});
        },
        addStudent() {
            this.studentDialogVisible = false;
            this.addStudentToDomain({domain: this.chosenDomain, student: this.addStudentForm.student})
        },
        openAddStudentModal(index) {
            this.fetchStudents();
            this.studentDialogVisible = true;
            this.chosenDomain = this.domains[index]
        }
    },
    mounted() {
        this.fetchAllDomains();
    }
}
</script>