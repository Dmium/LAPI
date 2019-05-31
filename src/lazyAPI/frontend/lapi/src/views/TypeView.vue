<template>
  <div class="TypeView">
    <h1 v-on:click="bam()">
      Type: {{ $route.params.name }}
    </h1>
    <div id="properties">
      <p text-align="center">Properties</p>
      <b-table striped hover
        :items="items"
        :sortBy="sortBy"
        :sortDesc="true"
        :fields="fields">
        <template slot="merge" slot-scope="data">
          <b-button variant="info" :to="{ name: 'propertyview', params: {typename: $route.params.name, propertyname: data.item[0]} }">Merge</a>
        </template>
        <template slot="delete" slot-scope="data">
          <b-button variant="danger" @click="deleteProperty(data.item[0])">Delete</a>
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
        { key: '0', label: 'Name' },
        { key: '1', label: 'Type' },
        { key: 'merge', label: 'Merge' },
        { key: 'delete', label: 'Delete' }
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
        this.items = this.toList(response.data.properties)
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
    toList: function (dict) {
      return Object.keys(dict).map(function (key) {
          return [key, dict[key]];
      });
    },
    deleteProperty: function (propname) {
    axios.delete('/lapi/types/' + this.$route.params.name + '/property/' + propname)
      .then(response => {
        // JSON responses are automatically parsed.
        // this.items = this.toList(response.data.properties)
        this.bam()
      })
      .catch(e => {
        this.errors.push(e)
      })
    }
  }
}
</script>
