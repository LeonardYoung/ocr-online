<!--
 * @Author: your name
 * @Date: 2021-01-16 20:09:17
 * @LastEditTime: 2021-01-16 22:11:59
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\views\TextOCR.vue
-->

<template>
  <skeleton title="文字识别">
    <template v-slot:sider>
      <sider-upload></sider-upload>
    </template>
    <template v-slot:contentLeft>
      left11
    </template>
    <template v-slot:contentRight>
      right
    </template>

  </skeleton>
</template>

<script>
  import Skeleton from "./Skeleton";
  import SiderUpload from './SiderUpload.vue'
  // import TinyCardList from '../components/content/TinyCardList.vue'
  export default {
    components: {
      Skeleton,
      SiderUpload
    },
    data() {
      return {    
        }
    }
  };
</script>

<style scoped>

</style>
