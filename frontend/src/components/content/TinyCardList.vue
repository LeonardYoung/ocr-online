<template>
  <div class="container">
    <div class="children" v-for="item in picList" v-bind:key="item.name">
      <tiny-card :picture="item.src" ></tiny-card>
    </div>
  </div>
</template>

<script>
  import TinyCard from './TinyCard.vue'
  export default{
    components:{
      TinyCard
    },
    props:['picList'],
    data(){
      return{
        
      }
    }
  }
</script>

<style scoped>
  .container{
    display: flex;
    flex-direction:column;
    width: 100%;
    height: 100%;
    text-align: center;
    overflow: auto;
    /* flex-grow: 2; */
  }
  .children{
    /* text-align: center; */
    margin: 0.5rem auto;
  }
</style>
