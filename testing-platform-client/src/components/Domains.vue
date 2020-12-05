<template>
    <div>
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
                label="Operations"
                width="120">
                <template slot-scope="scope">
                    <el-button @click="chooseDomain(scope.$index)" type="text" size="small">Choose</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    data() {
        return {
            show: false
        }
    },
    computed: {
        ...mapGetters({domains: 'domains/getDomains'})
    },
    methods: {
        ...mapActions('domains', ['fetchAllDomains']),
        chooseDomain(index) {
            if (!this.domains.length) {
                console.log("Domains list is empty!")
                return;
            }

            const chosenDomain = this.domains[index]
            this.$router.push({path: 'exams', query: {'domain_id': chosenDomain.id}})
        }
    },
    mounted() {
        this.fetchAllDomains();
    }
}
</script>