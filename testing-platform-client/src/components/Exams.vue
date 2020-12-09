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
                <svg id="dataviz_area">
                    <!-- <defs>
                        <marker id="markerArrow" markerWidth="13" markerHeight="13" refX="2" refY="6"
                            orient="auto">
                            <path d="M2,2 L2,11 L10,6 L2,2" style="fill: #000000; stroke-width: 10px;" />
                        </marker>
                    </defs> -->
                </svg>
                <!-- {{currentDomain.problems}} -->
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
        ...mapGetters({currentDomain: 'domains/getCurrentDomain'}),
    },
    methods: {
        ...mapActions('exams', ['fetchPersonalizedExams', 'fetchAllExams']),
        ...mapActions('account', ['fetchUserObject']),
        ...mapActions('domains', ['fetchDomain']),

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
                var svg = d3.select("#dataviz_area").
                attr("width", this.chartOptions.width)
                .attr("height", this.chartOptions.height)
                .style(
                    "transform",
                    `translate(${this.chartOptions.margin.left}px, ${this.chartOptions.margin.top}px)`
                );

                svg.append("svg:defs")
                    .append("svg:marker")
                    .attr("id", "markerArrow")
                    .attr("markerWidth", "13")
                    .attr("markerHeight", "13")
                    .attr("refX", "6")
                    .attr("refY", "6")
                    .attr("orient", "auto")
                    .attr("markerUnits","strokeWidth")
                    .attr("stroke-width","13")
                    .append("svg:path").attr("d", "M0,0 L0,6 L9,3 z").attr("fill","red");

                var g = svg.append("g");

                let nodes = problems.map(problem => ({id: problem.id, title: problem.title, x: problem.id * 100, y: 100}));

                var links = [];
                for (let problem of problems) {
                    for (let target_problem of problem.target_problems) {
                        links.push({source: {id: problem.id, x: problem.id * 100, y: 100}, target: {id: target_problem.target, x: target_problem.target * 100, y: 100}})
                    }
                }

                var simulation = d3.forceSimulation(nodes);
                    // .force("charge", d3.forceManyBody().strength(5))
                    // .force("link", d3.forceLink(links).distance(20).strength(1).iterations(10))
                    // .force("x", d3.forceX())
                    // .force("y", d3.forceY())
                    // .stop();

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

                    g.append("g")
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

                    var tooltip = g.append("g")
                                .append("text")
                                .style("visibility", "hidden")
                                .style("background", "#fff")
                                .attr("y", 60)
                                .attr("x", 100)
                                .text("a simple tooltip");

                    // add nodes
                    g.append("g")
                        .attr("stroke", "black")
                        .attr("stroke-width", 1.5)
                        .selectAll("circle")
                        .data(nodes)
                        .enter().append("circle")
                        .attr("cx", function(d) { return d.id * 100; })
                        .attr("cy", 100)    // TODO: make it work with levels
                        .attr("r", 15)
                        .attr("fill", "white")
                        .on("mouseover", function(event, i) {
                            d3.select(this).attr("fill", "orange");
                            d3.select(this).attr("r", 30);
                            if (event) {console.log();} // rebel against no-unused-vars!!
                            tooltip.style("visibility", "visible");
                            tooltip.text(i.title);
                            return tooltip.attr("x", i.id * 100 - 50);
                        })
                        .on("mouseout", function(event, i) {
                            d3.select(this).attr("fill", "white");
                            d3.select(this).attr("r", 15);
                            if (event && i) {console.log();} // rebel against no-unused-vars!!
                            return tooltip.style("visibility", "hidden");
                        });

                    // add text
                    g.append("g")
                        .selectAll("circle")
                        .data(nodes)
                        .enter()
                        .append("text")
                        .text(function(d) {return d.id; })
                        .attr('x', function(d) {return d.id * 100 - 5; })
                        .attr('y', 105);
                        
                });               
            }
            
        }
    },
    mounted() {
        this.fetchUserObject();
        
        // this.init();

        if (this.$route.query.domain_id) {
            this.fetchPersonalizedExams({id: this.$route.query.domain_id});
            this.fetchDomain(this.$route.query.domain_id);
        } else {
            this.fetchAllExams()
        }
    }
}
</script>