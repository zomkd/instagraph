import Vue from 'vue'
import App from './App.vue'
import router from "./router/index"
import 'materialize-css/dist/js/materialize.min'

import * as GmapVue from 'gmap-vue'


Vue.config.productionTip = false

Vue.use(GmapVue, {
  load: {
    key: 'AIzaSyBJTTi_-Gg5cNzqojXVkSk9b_7Kh1MpfQc',
    libraries: 'places',
  },
})

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
