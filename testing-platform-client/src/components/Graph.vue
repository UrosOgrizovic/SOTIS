<template>
    <div>
        <svg :id="`canvas${name}`" style="border: 1px solid; height: 500px; width: 1000px;">
            <g v-if="isEditMode" id="plus" stroke='black' stroke-width="2px">
                <line x1='10' y1='40' x2='70' y2='40' />
                <line x1='40' y1='10' x2='40' y2='70' />
            </g>               
            <g id="OG">
                    <g :id="`paths${name}`"></g>
                    <g :id="`tooltips${name}`"></g>
                    <g :id="`nodes${name}`"></g>
                    <g :id="`texts${name}`"></g>
            </g>     
            <defs>
                <marker :id="`markerArrow${name}`" markerWidth="13" markerHeight="13" refX="2" refY="6"
                    orient="auto">
                    <path d="M2,2 L2,11 L10,6 L2,2" style="fill: #000000; stroke-width: 10px;" />
                </marker>
            </defs>
        </svg>
        
        {{init()}}
    </div>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            chartOptions: {
                width: 750,
                height: 400,
                margin: {
                    top: 50,
                    right: 50,
                    left: 50,
                    bottom: 50
                }
            },
            newLink: {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}
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
        isNewLink: {
            type: Boolean,
            required: false,
            default: true
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
    methods: {
        init() {
            if (!this.nodes) {
                return;
            }

            const svg = d3.select(`#canvas${this.name}`)
                .attr("width", this.chartOptions.width)
                .attr("height", this.chartOptions.height)
                .on("contextmenu", (event) => {
                    event.preventDefault();
                });
            
            const gPaths = d3.select(`#paths${this.name}`);
            const gTooltips = d3.select(`#tooltips${this.name}`);
            const gNodes = d3.select(`#nodes${this.name}`);
            const gTexts = d3.select(`#texts${this.name}`);
            
            let nodes = []
            for (let i in this.nodes) {
                let node = this.nodes[i];
                i = parseInt(i);
                nodes.push({id: node.id, title: node.title, x: (i+1) * 100/2, y: 200});
            }

            let links = [];                
            for (let i in this.nodes) {
                let node = this.nodes[i];
                i = parseInt(i);
                for (let next_node of node[this.nextNodesField]) {
                    let idx = -1;
                    for (let j in nodes) {
                        if (nodes[j].id == next_node.target) {
                            idx = parseInt(j) + 1;
                            break;
                        }
                    }
                    if(idx > (i + 1)) {
                        links.push({
                            source: {id: node.id, x: (i+1) * 100 / 2, y: 200}, 
                            target: {id: next_node.target, x: idx * 100 / 2 - 15, y: 215}
                        })
                    } else {
                        links.push({
                            source: {id: node.id, x: (i+1) * 100 / 2, y: 200}, 
                            target: {id: next_node.target, x: idx * 100 / 2 + 15, y: 185}
                        })
                    }
                }
            }

            const simulation = d3.forceSimulation(nodes);

            const loading = svg.append("text")
                .attr("dy", "0.35em")
                .attr("text-anchor", "middle")
                .attr("font-family", "sans-serif")
                .attr("font-size", 10)
                .text("Simulating. One moment please…");

            // Use a timeout to allow the rest of the page to load first.
            d3.timeout(() => {
                loading.remove();

                // See https://github.com/d3/d3-force/blob/master/README.md#simulation_tick
                for (let i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
                    simulation.tick();
                }

                // add paths
                gPaths
                    .selectAll("path")
                    .data(links)
                    .enter().append("path")
                    .attr("d", d => {
                        return "M" + d.source.x + "," + d.source.y +
                                    " A10,10" 
                                    + " 0 0,0" + " " +
                                        d.target.x + "," + d.target.y;
                    })
                    .attr("stroke", "#000")
                    .attr("stroke-width", 1.5)
                    .attr("marker-end", `url(#markerArrow${this.name})`)
                    .attr("fill", "none");

                // add text to tooltip
                const tooltip = gTooltips
                            .append("text")
                            .style("visibility", "hidden")
                            .style("background", "#fff")
                            .attr("y", 160)
                            .attr("x", 100)
                            .text("a simple tooltip");

                // add nodes
                gNodes
                    .attr("stroke", "black")
                    .attr("stroke-width", 1.5)
                    .selectAll("circle")
                    .data(nodes)
                    .enter().append("circle")
                    .attr("cx", d => d.x)
                    .attr("cy", 200)
                    .attr("r", 15)
                    .attr("fill", "white")
                    .attr("id", d => d.id)
                    .on("mouseover", (event, i) => {
                        // if green (i.e. selected), don't make it orange
                        if (d3.select(event.target).attr("fill") == "white") {
                            d3.select(event.target).attr("fill", "orange");
                        }
                        d3.select(event.target).attr("r", 30);

                        tooltip.style("visibility", "visible");
                        tooltip.text(i.title);
                        return tooltip.attr("x", i.x - 50);
                    })
                    .on("mouseout", (event) => {
                        if (d3.select(event.target).attr("fill") == "orange") {
                            d3.select(event.target).attr("fill", "white");
                        }
                        
                        d3.select(event.target).attr("r", 15);
                        return tooltip.style("visibility", "hidden");
                    })
                    .on("click", (event, i) => {   // add link
                        if(!this.isEditMode) {
                            return;
                        }

                        if (!this.newLink.source.id) {
                            this.newLink.source = {id: i.id, x: i.x, y: 200}; // start edge here
                            d3.select(event.target).attr("fill", "#00ffff");
                            return;
                        } 
                        if (this.newLink.source.id == i.id) { // deselect node if double-clicked
                            d3.select(event.target).attr("fill", "white");
                            // reset newLink
                            this.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}
                        } else {
                            this.newLink.target = {id: i.id, x: i.x, y: 200}; // end edge here
                            let sourceNode = d3.selectAll("circle").filter(d => {
                                return d.id == this.newLink.source.id;   // select source node by id
                            });
                            let targetNode = d3.selectAll("circle").filter(d => {
                                return d.id == this.newLink.target.id;   // select source node by id
                            });
                            
                            this.$emit('add-link', this.newLink);

                            setTimeout(() => { 
                                if (this.isNewLink) {
                                    d3.select("#paths")
                                        .data([this.newLink]).append("path")
                                        .attr("d", d => {
                                            return "M" + d.source.x + "," + d.source.y +
                                                        " A10,10" 
                                                        + " 0 0,0" + " " +
                                                        d.target.x + "," + d.target.y;
                                        })
                                        .attr("stroke", "#000")
                                        .attr("stroke-width", 1.5)
                                        .attr("fill", "none")
                                        .attr("marker-end", `url(#markerArrow${this.name})`);
                                    links.push(this.newLink);
                                }
                                // reset data
                                sourceNode.attr("fill", "white");   // deselect source node
                                targetNode.attr("fill", "white");   // deselect target node
                                this.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}    // reset newLink
                                this.$store.state.domains.isNewLink = false;
                            }, 100);
                            
                        }
                    });
                

                gTexts
                    .selectAll("circle")
                    .data(nodes)
                    .enter()
                    .append("text")
                    .text(d => d.id)
                    .attr('x', d => {
                        let x = d.x - 5;
                        if (d.id > 9) {
                            x = x - 5;
                        }
                        return x; 
                    })
                    .attr('y', 205);
                    
            });    
            
            if (this.isEditMode) {
                d3.select("#plus")
                    .on("mouseover", function() {
                        d3.select(this).attr("stroke", "blue");
                        d3.select(this).attr("stroke-width", "10px");
                    })
                    .on("mouseout", function () {
                        d3.select(this).attr("stroke", "black");
                        d3.select(this).attr("stroke-width", "2px");
                    })
                    .on("click", () => {
                        this.$emit('plus-clicked');
                    });
            }
        }
    }
}
</script>