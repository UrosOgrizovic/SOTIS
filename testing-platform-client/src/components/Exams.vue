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
                <svg id="dataviz_area"></svg>
                {{currentDomain.problems}}
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
            console.log('u init');
            
            // console.log(data);
            if (problems) {

                var svg = d3.select("#dataviz_area").
                attr("width", this.chartOptions.width)
                .attr("height", this.chartOptions.height)
                // .selectAll("g").data(problems)
                // .enter().append("g")    // add one g element for each node, so as to allow centering text in node
                .style(
                    "transform",
                    `translate(${this.chartOptions.margin.left}px, ${this.chartOptions.margin.top}px)`
                );

                var g = svg.append("g");

                let nodes = problems.map(problem => ({id: problem.id, title: problem.title, x: problem.id * 100, y: 100}));
                
                var links = [];
                for (let problem of problems) {
                    for (let target_problem of problem.target_problems) {
                        links.push({source: {id: problem.id, x: problem.id * 100, y: 100}, target: {id: nodes[target_problem.id].id, x: target_problem.target * 100, y: 100}})
                    }
                }

                var simulation = d3.forceSimulation(nodes)
                    .force("charge", d3.forceManyBody().strength(-80))
                    .force("link", d3.forceLink(links).distance(20).strength(1).iterations(10))
                    .force("x", d3.forceX())
                    .force("y", d3.forceY())
                    .stop();

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
                        .attr("stroke", "#000")
                        .attr("stroke-width", 1.5)
                        .selectAll("line")
                        .data(links)
                        .enter().append("line")
                        .attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });

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
                        .on("mouseover", function(d, i) {
                            d3.select(this).attr("fill", "orange");
                            d3.select(this).attr("r", 30);
                            console.log(d, i);
                            tooltip.style("visibility", "visible");
                            tooltip.text(i.title);
                            return tooltip.attr("x", i.id * 100 - 50);
                        })
                        .on("mouseout", function(d, i) {
                            d3.select(this).attr("fill", "white");
                            d3.select(this).attr("r", 15);
                            console.log(d, i);
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

                // let node = svg.append("g").selectAll("g").data(nodes).enter().append("g");

                // node.append("circle").style("fill", "white").attr("stroke", "black");

                // // let link = svg.selectAll("line").data(links).enter().append("line").style("stroke", "#aaa");
                // // let link = svg.append("line").style("stroke", "#aaa").attr("marker-end", "url(#arrow)");
                // let link = svg.append("g").selectAll("line").data(links).enter().append("line").style("stroke", "#aaa").attr("marker-end", "url(#arrow)");

                // // let text = svg.append("text").text(function(d) {return d.id})
                // // let text = svg.append("g").selectAll("g").append("text").text(function(d) {return d.id})
                // let text = node.append("text").text(function(d) {return d.id})                
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