/*
 * @Author: your name
 * @Date: 2020-12-06 15:50:28
 * @LastEditTime: 2021-01-16 21:10:18
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\main.js
 */
import Vue from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import router from './router'


Vue.config.productionTip = false
Vue.use(router)
Vue.use(Antd)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
