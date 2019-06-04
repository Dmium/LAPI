import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Axios from 'axios'
import VueCookies from 'vue-cookies'

Vue.prototype.$http = Axios.create({headers: { "X-CSRFTOKEN": $cookies.get("X-CSRF") }})
Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.use(VueCookies)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
