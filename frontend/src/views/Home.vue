<!--
 * @Author: your name
 * @Date: 2021-01-15 15:26:29
 * @LastEditTime: 2021-01-16 21:24:50
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\views\Home.vue
-->
<template>
  <!-- <div class="home"> -->
  <div class="container">
    <!-- <div class="sider">
      <home-left/>
    </div>
    <div class="content">
        <router-view/>
    </div> -->

    <div class="btns">
      <a-button @click="clickA" size="large" type="primary">文字</a-button>
      <br/>
      <a-button @click="clickB" size="large" type="primary">工单</a-button>
    </div>
  </div>

  <!-- </div> -->
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
// import HomeLeft from '../views/HomeLeft'

export default {
  name: "Home",
  components: {
    // HomeLeft
  },
  methods: {
    clickA() {
      this.$router.push({ path: "textOCR" });
    },
    clickB() {
      this.$router.push({ path: "tableOCR" });
    },
  },
};
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
}
button {
  margin: 3rem  auto;
  width: 15rem;
  height: 4rem;
  border-radius: 2rem;
}
.btns{
  position:absolute;
  top: 50%;
  width: 100%;
  text-align: center;
  transform: translateY(-50%);
  
}
</style>
