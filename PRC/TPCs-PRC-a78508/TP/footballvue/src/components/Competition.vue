<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="ligas"
      class="elevation-1"
    >
      <template v-slot:no-data>
        <v-alert :value="true" color="error" icon="warning">
          Não foi possível apresentar uma lista das competições...
        </v-alert>
      </template>

      <template v-slot:items="props">
        <tr @click="rowClicked(props.item)">
          <td class="subheading">{{ props.item.name }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import axios from 'axios'
const lhost = 'http://localhost:3000'

export default {
  data: () => ({
    headers: [
      { text: 'Competições', align: 'left', value: 'name', class: 'title' }
    ],
    ligas: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/competitions')
      this.ligas = response.data
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      this.$router.push('/competitions/' + item.comp.split('#')[1] + '/seasons')
    }
  }
}
</script>