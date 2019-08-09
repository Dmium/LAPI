<template>
  <div class="TypeView">
    <h1 v-on:click="bam()">
      {{ $route.params.name }}'s Hidden Relationships
    </h1>
    <div id="properties">
      <p text-align="center">Properties</p>
      <b-table striped hover
        :items="items"
        :sortBy="sortBy"
        :sortDesc="true"
        :fields="fields">
        <template slot="fieldnameedit" slot-scope="data">
            <input v-model='data.item.fieldname' class="form-control" type="text" placeholder="Name for the relationship">
            <b-button variant="info" @click="reveal(data.item.relfieldname, data.item.fieldname)">Reveal</b-button>
        </template>
      </b-table>
    </div>
    <b-button variant="info" :to="{ name: 'overview'}">Back to Overview</b-button>
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
        { key: 'relfieldname', label: 'Origin Model' },
        { key: 'fieldnameedit', label: 'Field Name' },
      ],
      errors: [],
      items: []
    }
  },
  created() {
    this.bam()
  },
  methods: {
    bam: function () {
    axios.get(`/lapi/types/` + this.$route.params.name)
      .then(response => {
        // JSON responses are automatically parsed.
        this.items = response.data.impliedrelationships.filter(this.checkHidden)
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
    reveal: function(relfieldname, fieldname){
        this.$http.post('/lapi/types/' + this.$route.params.name + '/relationships/' + relfieldname,{
            fieldname: fieldname})
            .then(response => {
                this.items = response.data.impliedrelationships.filter(this.checkHidden)
            })
            .catch(e => {
                this.errors.push(e)
                this.bam()
            })
    },
    checkHidden: function (relationship) {
        return !('fieldname' in relationship)
    }
  }
}
</script>
