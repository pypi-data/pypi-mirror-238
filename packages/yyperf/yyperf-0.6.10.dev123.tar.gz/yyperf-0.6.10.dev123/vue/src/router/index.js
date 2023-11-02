import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);
const routes = [{
    path: '/',
    component: () => import(/* webpackChunkName: "home" */ '../views/home.vue'),
    meta: {title: 'yyPerf'},
}, {
    path: '/perf',
    component: () => import(/* webpackChunkName: "home" */ '../views/yyPerf.vue'),
    meta: {title: '性能采集'},
}, {
    path: '/debug',
    component: () => import(/* webpackChunkName: "home" */ '../views/uiDebug.vue'),
    meta: {title: '调试'},
},]

const router = new VueRouter({
    routes
})

export default router
router.beforeEach((to, from, next) => {
  document.title = to.meta.title  // 设置页面标题为目标路由的标题
  next()
})