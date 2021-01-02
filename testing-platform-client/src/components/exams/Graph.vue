<template>
    <div class="container">
        <svg>
            <defs>
                <marker id="m-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth" >
                    <path d="M0,0 L0,6 L9,3 z"></path>
                </marker>
                <marker id="m-start" markerWidth="6" markerHeight="6" refX="-4" refY="3" orient="auto" markerUnits="strokeWidth" >
                    <rect width="3" height="6"></rect>
                </marker>
            </defs>
        </svg>

    
        <d3-network :ref='`net-${name}`' 
                    :net-nodes="format.nodes" 
                    :net-links="format.links" 
                    :options="options"  
                    :link-cb="lcb"
                    @node-click="onNodeSelect"/>
    </div>
</template>

<script>
// import * as d3 from 'd3'
import D3Network from 'vue-d3-network';

export default {
    components: {
        D3Network
    },
    data() {
        return {
            options: {
                size:{ w:800, h:600},
                nodeSize: 15,
                nodeLabels: true,
                canvas: false,
                linkWidth:2
            },
            newLink: {source: null, target: null}
        }
    },
    props: {
        nodes: {
            type: Array,
            required: true
        },
        nextNodesField: {
            type: String,
            required: true
        },
        isEditMode: {
            type: Boolean,
            required: false,
            default: true
        },
        name: {
            type: String,
            required: false,
            default: ''
        }
    },
    computed: {
        format() {
            let nodes = [];
            let links = [];

            this.nodes.forEach(node => {
                nodes.push({id: node.id, name: `${node.id}-node`})
                node[this.nextNodesField].forEach(nextAttachment => {links.push({sid: node.id, tid: nextAttachment.target})})
            });
            return {
                nodes,
                links
            }
        }
    },
    methods: {
        lcb (link) {
            link._svgAttrs = { 'marker-end': 'url(#m-end)',
                            'marker-start': 'url(#m-start)'}
            return link
        },
        onNodeSelect(event, node) {
            if (!this.isEditMode) {
                return;
            }

            if (!this.newLink.source) {
                return this.newLink.source = node.id;
            }
            this.newLink.target = node.id;
            this.$emit('add-link', this.newLink)
        }
    }
}
</script>

<style src="vue-d3-network/dist/vue-d3-network.css"></style>

<style scoped>
.container {
    width: 800px;
}
#m-end path, #m-start{
  fill: rgba(18, 120, 98, 0.8);
}
</style>