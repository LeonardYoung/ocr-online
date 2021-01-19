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
      <a-button @click="clickA" size="large" type="primary">文字识别在线演示</a-button>
      <br/>
      <a-button @click="clickB" size="large" type="primary">工单识别在线演示</a-button>
    </div>
  </div>

  <!-- </div> -->
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
// import HomeLeft from '../views/HomeLeft'
// import PageOCR from '@/components/PageOCR'

export default {
  name: "Home",
  components: {
    // HomeLeft
  },
  methods: {
    clickA() {
      const type = '1';
      this.$router.push({ path: "/pageOCR" , query: { type:type }});
    },
    clickB() {
      const type = '2';
      this.$router.push({ path: "/pageOCR" ,query: { type:type }});
    },
  },
};
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
  background-image: url("/bg5.jpg");
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
