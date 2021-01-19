<template>
    <div>
        <d3-network :ref='`net-states`' 
                    :net-nodes="nodes" 
                    :net-links="[]"
                    :options="options"/>
    </div>
</template> 

<script>
import { mapGetters, mapActions } from 'vuex'
import D3Network from 'vue-d3-network';


export default {
    components: {
        D3Network
    },
    data() {
        return {
            options: {
                size: { w:400, h:300},
                nodeSize: 35,
                nodeLabels: true,
                canvas: false,
                linkWidth:2
            }
        }
    },
    computed: {
        ...mapGetters({
            states: 'exams/getExamStates',
            currentState: 'exams/getCurrentState'
        }),
        nodes() {
            return this.states.map((state, id) => {
                const _color = state == this.currentState ? 'red' : 'green';
                return {name: state, id, _color}
            })
        }
    },
    methods: {
        ...mapActions('exams', ['fetchExamState']),
    },
    mounted() {
        const examId = this.$route.params.exam_id;
        this.fetchExamState(examId);
    }
}
</script>