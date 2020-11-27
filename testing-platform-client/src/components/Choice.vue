<template>
    <ul>
        <li v-for="choice in choices" :key="choice.id">
            {{choice.choice_text}}
        </li>
    </ul>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
    computed: {
        ...mapGetters({choices: 'exams/getAllChoices'}),
    },
    methods: {
        ...mapActions('exams', ['fetchAllChoices'])
    },
    mounted() {
        this.fetchAllChoices();
    }
}
</script>