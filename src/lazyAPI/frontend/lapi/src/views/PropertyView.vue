<template>
  <div class="MergeView">
    <h1>
      Property: {{ $route.params.propertyname }}
    </h1>
    <p text-align="center">Properties</p>
    <b-table striped hover
      :items="items"
      :sortBy="sortBy"
      :sortDesc="true"
      :fields="fields">
      <template slot="merge" slot-scope="data">
        <b-button variant="primary">Merge in</a>
      </template>
    </b-table>
    <b-button variant="info" :to="{ name: 'typeview', params: {name: $route.params.typename } }">Back to Type</a>
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
        { key: 'merge', label: 'Merge' }
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
    axios.get(`/lapi/types/` + this.$route.params.typename)
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
    }
  }
}
</script>
