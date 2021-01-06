<template>
    <div>
        <div>
            <el-table
            :data="exams"
            style="width: 100%">
                <el-table-column
                    prop="title"
                    label="Exam"
                    width="180">
                </el-table-column>
                <el-table-column
                    prop="subject.title"
                    label="Subject"
                    width="180">
                </el-table-column>
                <el-table-column
                    prop="creator.username"
                    label="Author"
                    width="120">
                </el-table-column>
                <el-table-column
                    fixed="right"
                    label="Actions"
                    width="360">
                    <template slot-scope="scope">
                        <el-button v-if="belongsToGroup('Teacher')" @click="openDeleteExamModal(scope.$index)" type="text" size="small">Remove</el-button>
                        <el-button v-if="belongsToGroup('Teacher')" @click="openStudentList(scope.$index)" type="text" size="small">See student list</el-button>
                        <el-button v-if="belongsToGroup('Student')" @click="chooseExam(scope.$index)" type="text" size="small">Choose</el-button>
                        <el-button v-if="belongsToGroup('Teacher')" @click="downloadXML(scope.$index)" type="text" size="small">Download XML</el-button>
                    </template>
                </el-table-column>
            </el-table>
        <confirm-modal title="Are you sure?" ref="confirm"></confirm-modal>
        <router-link v-if="belongsToGroup('Teacher')" to="new-exam">New Exam</router-link>

        </div>
        <div v-if="belongsToGroup('Teacher') && domainId">
            <h4>Add nodes/problems by clicking on the plus sign.</h4>
            <h4>Add edges/problem attachments by clicking on a source node, then clicking on a target node. Cycles are not allowed.</h4>
            <el-button type="primary" @click="showProblemForm">Add new node</el-button>
            <el-form v-show="problemFormVisibility" :model="problemForm" label-width="120px" style="width: 50%">
                <h2>New Problem</h2>
                <el-form-item label="Question text" prop="question_text">
                    <el-col :span="12"><el-input v-model="problemForm.question_text" type="textarea"></el-input></el-col>
                </el-form-item>
                <el-form-item label="Exam">
                    <el-select v-model="problemForm.exam" placeholder="Select Exam">
                        <el-option v-for="exam in exams" :key="exam.id" :label="exam.title" :value="exam.id">{{exam.title}}</el-option>
                    </el-select>
                </el-form-item>

                <el-button style="float: right; margin-right: 10px;" type="primary" @click="submitProblem()">Submit</el-button>
                <el-button @click="choiceFormVisibility = true" icon="el-icon-circle-plus" circle></el-button>
                <ul>
                    <li v-for="choice in problemForm.choices" :key="choice.choice_text">{{choice.choice_text}}</li>
                </ul>
            </el-form>

            

            <el-form v-if="choiceFormVisibility" :model="choiceForm" label-width="120px" style="width: 50%">
                <h2>New Choice</h2>
                <el-form-item label="Choice Text" prop="choice_text">
                    <el-col :span="12"><el-input v-model="choiceForm.choice_text" type="textarea"></el-input></el-col>
                </el-form-item>
                <el-checkbox v-model="choiceForm.correct_answer">Correct Answer</el-checkbox>
                <el-form-item>
                    <el-button style="float: right; margin-right: 10px;" type="primary" @click="onAddChoice()">Add</el-button>
                </el-form-item>
            </el-form>


            <div style="display: flex; flex-direction: row;">
                <div>
                    <h3>Expected Knowledge Space</h3>
                    <graph @add-link="connectProblems"
                           :is-edit-mode="true"
                           :nodes="currentDomain.problems || []" 
                           :is-new-link="isDomainNewLink"
                           :name="'expected-ks'"
                           :next-nodes-field="'target_problems'"/>
                </div>
                <div>
                    <h3>Actual Knowledge Space</h3>
                    <graph :is-edit-mode="false"
                           :nodes="currentDomain.problems || []" 
                           :name="'actual-ks'"
                           :is-new-link="isDomainNewLink"
                           :next-nodes-field="'actual_target_problems'"/>
                </div>
                <div>
                    <h3>Compare Knowledge Spaces</h3>
                    <h3>Graph edit distance = {{domainGED}}</h3>
                    <graph :is-edit-mode="false"
                           :nodes="currentDomain.problems || []" 
                           :name="'diff-ks'"
                           :is-new-link="isDomainNewLink"
                           :next-nodes-field="'diff_target_problems'"/>
                </div>
                
            </div>
            
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import ConfirmModal from '@Components/shared/ConfirmModal';
import Graph from './Graph';

export default {
    components: {
        ConfirmModal,
        Graph
    },
    data() {
        return {
            domainId: null,
            problemFormVisibility: false,
            choiceFormVisibility: false,
            problemForm: {
                question_text: '',
                exam: null,
                choices: []
            },
            choiceForm: {
                choice_text: '',
                correct_answer: false
            }
        }
    },
    computed: {
        ...mapState({
            account: state => state.account,
            checkIfStudent(state) {
                var isStudent = false;
                if (state.account.userObject.groups && state.account.userObject.groups.includes("Student")) {
                    isStudent = true;
                }
                return isStudent;    
            }
        }),
        ...mapGetters({exams: 'exams/getAllExams'}),
        ...mapGetters({xml: 'exams/getXML'}),
        ...mapGetters({examGED: 'exams/getExamGED'}),
        ...mapGetters({isDomainNewLink: 'domains/getIsNewLink'}),
        ...mapGetters({domainNewNode: 'domains/getNewNode'}),
        ...mapGetters({unattachedExams: 'domains/getUnattachedExams'}),
        ...mapGetters({currentDomain: 'domains/getCurrentDomain'}),
        ...mapGetters({domainGED: 'domains/getDomainGED'}),
    },
    methods: {
        ...mapActions('exams', ['fetchPersonalizedExams', 'fetchAllExams', 'deleteExam', 'fetchXML', 'compareKnowledgeSpaces']),
        ...mapActions('account', ['fetchUserObject']),
        ...mapActions('domains', ['fetchDomain', 'createLink', 'createNode', 'fetchDomainGED']),
        chooseExam(index) {
            if (!this.exams.length) {
                console.log("Exams list is empty!")
                return;
            }
            const chosenExam = this.exams[index]
            this.$router.push({name: 'single_exam', params: {'exam_id': chosenExam.id}})
        },
        openStudentList(index) {
            if (!this.exams.length) {
                console.log("Exams list is empty!")
                return;
            }
            const chosenExam = this.exams[index]
            this.$router.push({name: 'exam_takers_list', params: {'exam_id': chosenExam.id}})
        },
        downloadXML(index) {
            if (!this.exams.length) {
                console.log("Exams list is empty!")
                return;
            }
            const chosenExam = this.exams[index];
            this.fetchXML(chosenExam.id);
            
            let a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            const blob = new Blob([this.xml], {type: "octet/stream"}),
            url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = chosenExam.title + ".xml";
            a.click();
            window.URL.revokeObjectURL(url);
        },
        openDeleteExamModal(index) {
            this.$refs.confirm.show().then(() => {
                const chosenExam = this.exams[index]
                this.deleteExam(chosenExam)
            })
            .catch(() => {});
        },
        submitProblem() {
            const domain = this.currentDomain.id
            const newNode = {
                domain,
                ...this.problemForm
            }
            this.createNode(newNode);
            this.problemFormVisibility = false;
            this.fetchDomain(this.currentDomain.id);
        },
        showProblemForm() {
            this.problemFormVisibility = true;
        },
        connectProblems(newLink) {
            this.createLink({domainId: this.currentDomain.id, source: newLink.source, target: newLink.target});
            this.fetchDomain(this.currentDomain.id);
        },
        onAddChoice() {
            this.problemForm.choices.push(this.choiceForm)

            this.choiceForm = {
                choice_text: '',
                correct_answer: false
            }
        }
    },
    mounted() {
        this.fetchUserObject();
        if (this.$route.query.domain_id) {
            this.domainId = this.$route.query.domain_id;
            this.fetchPersonalizedExams({id: this.domainId});
            this.fetchDomain(this.domainId);
            this.fetchDomainGED(this.domainId);
        }
        this.fetchAllExams();
    }
}
</script>