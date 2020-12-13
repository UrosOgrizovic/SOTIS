<template>
    <div>
        <div v-if="checkIfStudent">
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
                width="180">
            </el-table-column>
            <el-table-column
                fixed="right"
                label="Operations"
                width="120">
                <template slot-scope="scope">
                    <el-button @click="chooseExam(scope.$index)" type="text" size="small">Choose</el-button>
                </template>
            </el-table-column>
        </el-table>
        </div>
        <div v-else>
            <div v-if="currentDomain">
            </div>
                <router-link to="new-exam">New Exam</router-link>   
                <br>
                <h4>Add nodes/problems by clicking on the plus sign.</h4>
                <h4>Add edges/problem attachments by clicking on a source node, then clicking on a target node. Cycles are not allowed.</h4>
                <div id="problemForm" style="visibility: hidden;">
                    <label for="title">Title:</label><br>
                    <input type="text" id="newProblemTitle" name="title"><br><br>
                    <label for="examid">Exam id:</label><br>
                    <select name="examIds" id="examIds">
                        <option v-for="exam in this.unattachedExams" :key="exam.id"> {{ exam.id }} - {{ exam.title }} </option>
                    </select>
                    <br>
                    <button type="submit" id="problemSubmitBtn" v-on:click="myFunction()">Submit</button>
                </div>
                
                <svg id="dataviz_area" style="border: 1px solid; height: 500px; width: 1000px;">
                    <g id="plus" stroke='black' stroke-width="2px">
                        <line x1='10' y1='40' x2='70' y2='40' />
                        <line x1='40' y1='10' x2='40' y2='70' />
                    </g>               
                    <g id="OG">
                         <g id="paths"></g>
                         <g id="tooltips"></g>
                         <g id="nodes"></g>
                         <g id="texts"></g>
                    </g>     
                    <defs>
                        <marker id="markerArrow" markerWidth="13" markerHeight="13" refX="2" refY="6"
                            orient="auto">
                            <path d="M2,2 L2,11 L10,6 L2,2" style="fill: #000000; stroke-width: 10px;" />
                        </marker>
                    </defs>
                </svg>
                
                {{init(currentDomain.problems)}}
        </div>
        
    </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import * as d3 from 'd3'

export default {
    data() {
        return {
            show: false,
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
            newLink: {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}},
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
        ...mapGetters({currentDomain: 'domains/getCurrentDomain'}),
        ...mapGetters({isDomainNewLink: 'domains/getIsNewLink'}),
        ...mapGetters({domainNewNode: 'domains/getNewNode'}),
        ...mapGetters({unattachedExams: 'domains/getUnattachedExams'})
    },
    methods: {
        ...mapActions('exams', ['fetchPersonalizedExams', 'fetchAllExams']),
        ...mapActions('account', ['fetchUserObject']),
        ...mapActions('domains', ['fetchDomain', 'createLink', 'createNode', 'getUnattachedExamsForDomainId']),

        chooseExam(index) {
            if (!this.exams.length) {
                console.log("Exams list is empty!")
                return;
            }
            const chosenExam = this.exams[index]
            this.$router.push({name: 'single_exam', params: {'exam_id': chosenExam.id}})
        },
        init(problems) {
            
            if (problems) {
                let ref = this;

                var svg = d3.select("#dataviz_area").
                attr("width", this.chartOptions.width)
                .attr("height", this.chartOptions.height)
                .style(
                    "transform",
                    `translate(${this.chartOptions.margin.left}px, ${this.chartOptions.margin.top}px)`
                )
                .on("contextmenu", function(event) {
                    event.preventDefault();
                });
                

                // svg.append("svg:defs")
                //     .append("svg:marker")
                //     .attr("id", "markerArrow")
                //     .attr("markerWidth", "13")
                //     .attr("markerHeight", "13")
                //     .attr("refX", "6")
                //     .attr("refY", "6")
                //     .attr("orient", "auto")
                //     .attr("markerUnits","strokeWidth")
                //     .attr("stroke-width","13")
                //     .append("svg:path").attr("d", "M0,0 L0,6 L9,3 z").attr("fill","red");

                // var g = d3.select("#OG");
                var gPaths = d3.select("#paths");
                var gTooltips = d3.select("#tooltips");
                var gNodes = d3.select("#nodes");
                var gTexts = d3.select("#texts");

                let nodes = []
                for (let i in problems) {
                    let problem = problems[i];
                    i = parseInt(i);
                    nodes.push({id: problem.id, title: problem.title, x: (i+1) * 100/2, y: 200});
                }

                var links = [];                
                for (let i in problems) {
                    let problem = problems[i];
                    i = parseInt(i);
                    for (let target_problem of problem.target_problems) {
                        let idx = -1;
                        for (let j in nodes) {
                            if (nodes[j].id == target_problem.target) {
                                idx = parseInt(j) + 1;
                                break;
                            }
                        }
                        links.push({source: {id: problem.id, x: (i+1) * 100 / 2, y: 200}, 
                        target: {id: target_problem.target, x: idx * 100 / 2, y: 200}})
                    }
                }

                var simulation = d3.forceSimulation(nodes);

                var loading = svg.append("text")
                    .attr("dy", "0.35em")
                    .attr("text-anchor", "middle")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 10)
                    .text("Simulating. One moment please…");

                // Use a timeout to allow the rest of the page to load first.
                d3.timeout(function() {
                    loading.remove();

                    // See https://github.com/d3/d3-force/blob/master/README.md#simulation_tick
                    for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
                        simulation.tick();
                    }

                    // add paths
                    gPaths
                        .selectAll("path")
                        .data(links)
                        .enter().append("path")
                        .attr("d", function(d) {
                            return "M" + d.source.x + "," + d.source.y +
                                        " A10,10" 
                                        + " 0 0,0" + " " +
                                         d.target.x + "," + d.target.y;
                        })
                        .attr("stroke", "#000")
                        .attr("stroke-width", 1.5)
                        .attr("fill", "none")
                        .attr("marker-end", "url(#markerArrow)");

                    // add text to tooltip
                    var tooltip = gTooltips
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
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", 200)
                        .attr("r", 15)
                        .attr("fill", "white")
                        .attr("id", function(d) {return d.id;})
                        .on("mouseover", function(event, i) {
                            // if green (i.e. selected), don't make it orange
                            if (d3.select(this).attr("fill") == "white") {
                                d3.select(this).attr("fill", "orange");
                            }
                            d3.select(this).attr("r", 30);
                            if (event) {console.log();} // rebel against no-unused-vars!!
                            tooltip.style("visibility", "visible");
                            tooltip.text(i.title);
                            return tooltip.attr("x", i.x - 50);
                        })
                        .on("mouseout", function(event, i) {
                            if (d3.select(this).attr("fill") == "orange") {
                                d3.select(this).attr("fill", "white");
                            }
                            
                            d3.select(this).attr("r", 15);
                            if (event && i) {console.log();} // rebel against no-unused-vars!!
                            return tooltip.style("visibility", "hidden");
                        })
                        .on("click", function(event, i) {   // add link
                            if (!ref.newLink.source.id) {
                                ref.newLink.source = {id: i.id, x: i.x, y: 200}; // start edge here
                                d3.select(this).attr("fill", "#00ffff");
                            } else {
                                if (ref.newLink.source.id == i.id) { // deselect node if double-clicked
                                    d3.select(this).attr("fill", "white");
                                    // reset newLink
                                    ref.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}
                                } else {
                                    ref.newLink.target = {id: i.id, x: i.x, y: 200}; // end edge here
                                    let sourceNode = d3.selectAll("circle").filter(function(d) {
                                        return d.id == ref.newLink.source.id;   // select source node by id
                                    });
                                    let targetNode = d3.selectAll("circle").filter(function(d) {
                                        return d.id == ref.newLink.target.id;   // select source node by id
                                    });
                                    
                                    ref.createLink({domainId: ref.currentDomain.id, source: ref.newLink.source.id, target: ref.newLink.target.id});
                                    setTimeout(function(){ 
                                        if (ref.isDomainNewLink) {
                                             // draw path from newLink.source to newLink.target
                                            d3.select("#paths")
                                            .data([ref.newLink]).append("path")
                                            .attr("d", function(d) {
                                                return "M" + d.source.x + "," + d.source.y +
                                                            " A10,10" 
                                                            + " 0 0,0" + " " +
                                                            d.target.x + "," + d.target.y;
                                            })
                                            .attr("stroke", "#000")
                                            .attr("stroke-width", 1.5)
                                            .attr("fill", "none")
                                            .attr("marker-end", "url(#markerArrow)");
                                            links.push(ref.newLink);
                                            }
                                        // reset data
                                        sourceNode.attr("fill", "white");   // deselect source node
                                        targetNode.attr("fill", "white");   // deselect target node
                                        ref.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}    // reset newLink
                                        ref.$store.state.domains.isNewLink = false;
                                    }, 100);
                                }
                            }
                        });
                    

                    // add text
                    // g.append("g")
                    //     .attr("id", "texts")
                    gTexts
                        .selectAll("circle")
                        .data(nodes)
                        .enter()
                        .append("text")
                        .text(function(d) {return d.id; })
                        .attr('x', function(d) {
                            let x = d.x - 5;
                            if (d.id > 9) {
                                x = x - 5;
                            }
                            return x; 
                        })
                        .attr('y', 205);
                        
                });    
                
                d3.select("#plus")
                .on("mouseover", function() {
                    d3.select(this).attr("stroke", "blue");
                    d3.select(this).attr("stroke-width", "10px");
                })
                .on("mouseout", function() {
                    d3.select(this).attr("stroke", "black");
                    d3.select(this).attr("stroke-width", "2px");
                })
                .on("click", function() { // add node
                    if (ref.unattachedExams.length == 0) {
                        ref.$alert("There are no unattached exams in this domain available to connect a problem to. Please create an exam for this domain and try again."); // VueSimpleAlert
                    } else {
                        document.getElementById("problemForm").style.visibility = "visible";
                    }
                });
            }
        },
        myFunction() {
            let newNode = {domainId: this.currentDomain.id, title: document.getElementById("newProblemTitle").value, 
            examId: parseInt(document.getElementById("examIds").value.split("-")[0].trim())}
            this.createNode(newNode);
            let ref = this;
            setTimeout(function() {                
                if (ref.domainNewNode) {
                    // ref.nodes.push({id: ref.domainNewNode.id, title: ref.domainNewNode.title, x: (ref.nodes.length+1) * 100 / 2, y: 200});
                    // TODO: remove exam with newNode.examId from unattached exams
                    document.getElementById("problemForm").style.visibility = "hidden";
                    ref.fetchDomain(ref.currentDomain.id);
                    ref.getUnattachedExamsForDomainId(ref.currentDomain.id);
                    ref.init(ref.currentDomain.problems);
                    // console.log(ref.currentDomain); // ako je ovde dodat novi problem u probleme, odkomentarisi liniju ispod i probaj tako
                    // this.init(this.currentDomain.problems);










                    // let newNode = {id: nodes[nodes.length - 1].id + 1, title: "bla", x: nodes[nodes.length - 1].x + 50, y: 200};
                    // nodes.push(newNode);

                    // d3.select("#nodes")
                    // .data([newNode]).append("circle")
                    // .attr("cx", function(d) {return d.x;})
                    // .attr("cy", function(d) {return d.y;})
                    // .attr("r", 15)
                    // .attr("fill", "white")
                    // .on("click", function(event, i) {
                    //     if (!ref.newLink.source.id) {
                    //         ref.newLink.source = {id: i.id, x: i.id * 100 / 2, y: 200}; // start edge here
                    //         d3.select(this).attr("fill", "#00ffff");
                    //     } else {
                    //         if (ref.newLink.source.id == i.id) { // deselect node if double-clicked
                    //             d3.select(this).attr("fill", "white");
                    //             // reset newLink
                    //             ref.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}
                    //         } else {
                    //             ref.newLink.target = {id: i.id, x: i.id * 100 / 2, y: 200}; // end edge here
                    //             let sourceNode = d3.selectAll("circle").filter(function(d) {
                    //                 return d.id == ref.newLink.source.id;   // select source node by id
                    //             });
                    //             let targetNode = d3.selectAll("circle").filter(function(d) {
                    //                 return d.id == ref.newLink.target.id;   // select source node by id
                    //             });
                                
                    //             ref.createLink({domainId: ref.currentDomain.id, source: ref.newLink.source.id, target: ref.newLink.target.id});
                    //             setTimeout(function(){ 
                    //                 if (ref.isDomainNewLink) {
                    //                      // draw path from newLink.source to newLink.target
                    //                     d3.select("#paths")
                    //                     .data([ref.newLink]).append("path")
                    //                     .attr("d", function(d) {
                    //                         return "M" + d.source.x + "," + d.source.y +
                    //                                     " A10,10" 
                    //                                     + " 0 0,0" + " " +
                    //                                     d.target.x + "," + d.target.y;
                    //                     })
                    //                     .attr("stroke", "#000")
                    //                     .attr("stroke-width", 1.5)
                    //                     .attr("fill", "none")
                    //                     .attr("marker-end", "url(#markerArrow)");
                    //                     links.push(ref.newLink);
                    //                     }
                    //                 // reset data
                    //                 sourceNode.attr("fill", "white");   // deselect source node
                    //                 targetNode.attr("fill", "white"); // deselect source node
                    //                 ref.newLink = {source: {id: null, x: null, y: 200}, target: {id: null, x: null, y: 200}}    // reset newLink
                    //             }, 100);
                    //         }
                    //     }
                    // });
                    // // add text
                    // g.append("g")
                    // .attr("id", "texts")
                    // .selectAll("circle")
                    // .data([newNode])
                    // .enter()
                    // .append("text")
                    // .text(function(d) {return d.id; })
                    // .attr('x', function(d) {
                    //     let x = d.id * 100 / 2 - 5;
                    //     if (d.id > 9) {
                    //         x -= 5;
                    //     }
                    //     return x; 
                    // })
                    // .attr('y', 205);
                }
            }, 100)
        }
    },
    mounted() {
        this.fetchUserObject();
        if (this.$route.query.domain_id) {
            let domainId = this.$route.query.domain_id;
            this.fetchPersonalizedExams({id: domainId});
            this.fetchDomain(domainId);
            this.getUnattachedExamsForDomainId(domainId);
        } else {
            this.fetchAllExams()
        }
    }
}
</script>