/*
 * @Author: your name
 * @Date: 2021-01-15 15:26:29
 * @LastEditTime: 2021-01-16 20:40:25
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\router\index.js
 */
import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import TextOCR from '../views/TextOCR.vue'
import TableOCR from '../views/TableOCR.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/textOCR',
    component: TextOCR
  },
  {
    path: '/tableOCR',
    component: TableOCR
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
