<template>
  <div class="login">
    <h1>
      Login
    </h1>
    <input v-model="username" placeholder="Username">
    <br>
    <input type="password" v-model="password" placeholder="Password">
    <br>
    <b-button variant="primary" @click="tryLogin()">Login</b-button>

  </div>
</template>
<script>
import axios from 'axios';
export default {
  data () {
    return {
    }
  },
  methods: {
    tryLogin: function (event) {
    this.$http.post(`/login`, {"id": this.username, "password": this.password})
      .then(response => {
      })
      .catch(e => {
        this.errors.push(e)
      })
    }
  }
}
</script>
