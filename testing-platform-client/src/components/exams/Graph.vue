<template>
    <div class="container">
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
                size:{ w:400, h:300},
                nodeSize: 15,
                nodeLabels: true,
                canvas: false,
                linkWidth:2
            },
            newLink: {source: null, target: null},
            exchangePairs: {}
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
        },
        bidirectionDisable: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    computed: {
        formatWithBidirection() {
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
        },
        formatWithoutBidirection() {
            if (!this.nodes) {
                return {};
            }
            let resultNodes = [];
            let resultLinks = [];

            let currentLinks = {}
            let nodes = this.nodes
            do {
                resultNodes = [];
                resultLinks = [];
                nodes.forEach(node => {
                    node[this.nextNodesField].forEach(nextAttachment => {
                        const sid = this.exchangePairs[node.id] || node.id
                        const tid = this.exchangePairs[nextAttachment.target] || nextAttachment.target
                        if (currentLinks[tid] && currentLinks[tid].includes(sid)) {
                            this.exchangePairs[sid] = tid
                        } else {
                            currentLinks[sid] = currentLinks[sid] ? [...currentLinks[sid], tid] : [tid]
                        }
                    })
                })
                
                nodes.forEach(node => {
                    if (this.exchangePairs[node.id]) {
                        return;
                    }
                    if (!this.exchangePairs[node.id]) {
                        resultNodes.push({id: node.id, name: `${node.id}-node`})
                    }
                    node[this.nextNodesField].forEach(nextAttachment => {
                        const sid = this.exchangePairs[node.id] || node.id
                        const tid = this.exchangePairs[nextAttachment.target] || nextAttachment.target
                        if (sid == tid) {
                            return;
                        }
                        resultLinks.push({sid, tid});
                    })
                });
                nodes = this.nodes.filter(node => {return !Object.keys(this.exchangePairs).map(id => parseInt(id)).includes(node.id)})
            } while(this.checkBidirection(resultLinks));

            return {
                nodes: resultNodes,
                links: resultLinks
            }
        },
        format() {
            return this.bidirectionDisable ? this.formatWithoutBidirection : this.formatWithBidirection
        }
    },
    methods: {
        checkBidirection(links) {
            let bidirectionExists = false;
            links.forEach(link => {
                links.forEach(otherLink => {
                    if (link.sid == otherLink.tid && link.tid == otherLink.sid) {
                        bidirectionExists = true;
                    }
                })
            })
            return bidirectionExists;
        },
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
    width: 400px;
    border: 1px solid black;
}
#m-end path, #m-start{
  fill: rgba(18, 120, 98, 0.8);
}
</style>