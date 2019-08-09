<template>
  <div class="overview">
    <h1 v-on:click="bam()">
      Overview
    </h1>
    <div id="Types">
      <p text-align="center">Types</p>
      <input name="csrf_token" value="{{ csrf_token() }}" /> 
      <b-table striped hover
             :items="items"
             :sortBy="sortBy"
             :sortDesc="true"
             :fields="fields">
         <template slot="eh" slot-scope="data">
           <b-button variant="info" :to="{ name: 'typeview', params: {name: data.item.name } }">Configure</a>
        </template>

         <template slot="ehrel" slot-scope="data">
           <b-button variant="info" :to="{ name: 'relationshipview', params: {name: data.item.name } }">Configure</a>
        </template>
      </b-table>
    </div>
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
        { key: 'eh', label: 'Configure Properties' },
        { key: 'ehrel', label: 'Configure Relationships' }
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
