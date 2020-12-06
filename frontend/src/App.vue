<template>
  <div id="app">
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
<!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <PageOCR class="page-ocr"/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import PageOCR from "./components/PageOCR";

export default {
  name: 'App',
  components: {
    PageOCR,
    // HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
    width: 100%;
    height: 100%;
}
html{
    font-size: 20px;
}
    .page-ocr{
        width: 100%;
        height: 100%;
    }
</style>
