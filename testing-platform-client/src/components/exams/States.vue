<template>
    <div>
        <svg style="width: 0px; height: 0px;">
            <defs>
                <marker id="m-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth" >
                    <path d="M0,0 L0,6 L9,3 z"></path>
                </marker>
                <marker id="m-start" markerWidth="6" markerHeight="6" refX="-4" refY="3" orient="auto" markerUnits="strokeWidth" >
                    <rect width="3" height="6"></rect>
                </marker>
            </defs>
        </svg>
        <d3-network :ref='`net-states`' 
                    :net-nodes="format.nodes"
                    :net-links="format.links"
                    :link-cb="lcb"
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
                nodeSize: 20,
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
        format() {
            let nodes = []
            let links = []

            this.states.forEach(state => {
                const _color = state.code == this.currentState ? 'red' : 'green';
                nodes.push({name: state.code, id: state.code, _color})
                if (!state.edges) {
                    return;
                }
                state.edges.forEach(nextState => {
                    const linkExists = links.find((link) => { return link.sid == nextState && link.tid == state.code})
                    if (linkExists) {
                        return;
                    }
                    links.push({sid: state.code, tid: nextState})
                })
            })
            return { nodes, links }
        }
    },
    methods: {
        ...mapActions('exams', ['fetchExamState']),
        lcb (link) {
            link._svgAttrs = { 'marker-end': 'url(#m-end)',
                            'marker-start': 'url(#m-start)'}
            return link
        }
    },
    mounted() {
        const examId = this.$route.params.exam_id;
        this.fetchExamState(examId);
    }
}
</script>

<style scoped>
#m-end path, #m-start{
  fill: rgba(18, 120, 98, 0.8);
}
</style>