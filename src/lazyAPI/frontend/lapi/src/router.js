import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    },
    {
      path: '/overview',
      name: 'overview',
      component: () => import('./views/Overview.vue')
    },
    {
      path: '/typeview/:name',
      name: 'typeview',
      component: () => import('./views/TypeView.vue')
    },
    {
      path: '/typeview/:typename/property/:propertyname/merge',
      name: 'propertyview',
      component: () => import('./views/PropertyView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/Login.vue')
    }
  ]
})
