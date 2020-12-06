<template>
    <div id="app">
        <Nav></Nav>
        <router-view></router-view>
    </div>
</template>

<script>
import Nav from './components/Nav.vue'
export default {
  name: 'App',
  components: {
      Nav
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
