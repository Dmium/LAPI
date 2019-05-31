<template>
  <div class="overview">
    <h1 v-on:click="bam()">
      Overview
    </h1>
    <div id="Types">
      <p text-align="center">Types</p>
      <b-table striped hover
             :items="items"
             :sortBy="sortBy"
             :sortDesc="true"
             :fields="fields">
         <template slot="eh" slot-scope="data">
           <b-button variant="info" :to="{ name: 'typeview', params: {name: data.item.name } }">Configure</a>
        </template>
      </b-table>
    </div>
    <h2>
      eh
    </h2>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  data () {
    return {
      sortBy: 'seq',
      desc: true,
      fields: [
        { key: 'name', sortable: true },
        { key: 'seq', sortable: false },
        { key: 'eh', label: 'First name and age' }
      ],
      errors: [],
      items: []
    }
  },
  created() {
  axios.get(`/lapi/types`)
    .then(response => {
      // JSON responses are automatically parsed.
      this.items = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  },
  methods: {
    bam: function (event) {
    axios.get(`/lapi/types`)
      .then(response => {
        // JSON responses are automatically parsed.
        this.items = response.data
      })
      .catch(e => {
        this.errors.push(e)
      })
    }
  }
}
</script>
