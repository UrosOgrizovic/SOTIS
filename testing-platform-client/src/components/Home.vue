  
<template>
    <div>
        <img width="200px" src="../assets/logo.png">
        <h1>Hi {{account.user.firstName}}!</h1>
        <div class="container">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vitae ex quis lacus viverra mattis. Nullam non rutrum dui. Nunc commodo, erat quis condimentum hendrerit, ex arcu faucibus tortor, non dapibus ante ex quis nulla. Donec faucibus nunc ante, a blandit nulla porta nec. Phasellus blandit diam quis laoreet ultrices. Pellentesque et malesuada elit. Duis urna risus, feugiat id dignissim et, auctor eu lacus. Quisque ac tempor elit, quis mattis justo. Phasellus non porta ante. Nulla facilisi. In non feugiat urna, id suscipit lorem.</p>
            <p>Vestibulum tincidunt accumsan leo in auctor. Etiam diam felis, aliquam non aliquet in, faucibus quis quam. Maecenas in tortor risus. Quisque laoreet arcu nec magna consequat tincidunt. Etiam vel feugiat nisi. Suspendisse potenti. Nam gravida lectus libero, a tempor dolor auctor eget. Maecenas feugiat nibh sed magna volutpat sollicitudin. Maecenas felis risus, auctor at arcu et, posuere porta dui. Ut ac augue ut elit porta pulvinar nec et justo. Curabitur metus ante, pulvinar sit amet tortor a, consectetur interdum nisl.</p>
            <p>Praesent porttitor sed urna vitae vulputate. Donec euismod, sapien cursus pellentesque eleifend, ligula magna egestas ante, quis maximus diam arcu volutpat odio. Donec pretium sapien a sem tempor tristique. Ut eu lectus vel nunc pellentesque ullamcorper. Donec hendrerit lorem at risus imperdiet lacinia non id nisl. Aliquam pulvinar accumsan ultricies. Nunc enim orci, interdum nec convallis nec, sollicitudin eu justo. Curabitur vel felis viverra, scelerisque justo aliquam, sodales ipsum. Maecenas fringilla, elit et consectetur consectetur, neque felis efficitur ex, sit amet laoreet neque lacus nec enim. Donec elementum lacus vel mattis egestas. Etiam dictum enim dolor, quis finibus magna efficitur ut. Donec nec ligula at sem facilisis mollis vitae eget arcu. Donec gravida mi ac enim consequat, vitae luctus neque semper.</p>
        </div>
        
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    computed: {
        ...mapState({
            account: state => state.account
        })
    }
};
</script>

<style scoped>
.container {
    margin-left: 25%;
    margin-right: 25%;
}
</style>