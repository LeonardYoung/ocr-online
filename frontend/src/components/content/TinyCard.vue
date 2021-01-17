<template>
  <div class="card">
    <img :src="picture" width="70px" height="80px" @click="imgClick" />
    <p> describe </p>
  </div>

</template>

<script>
  export default {
    name: 'TinyCard',
    props:['picture'],
    data(){
      return{
        // picture:"https://yangsj-first-bucket.oss-cn-guangzhou.aliyuncs.com/markdown/image-20201222121429413.png"
      }
    },
    methods:{
      imgClick(){
        console.log('click')
      }
    }
  }
</script>

<style scoped>
  img:hover{
    cursor: hand;
  }
  .card{
    width: 72px;
    height: 110px;
    border: 1px solid black;
  }
</style>
