<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="seasons"
      class="elevation-1"
    >
      <template v-slot:no-data>
        <v-alert :value="true" color="error" icon="warning">
          Não foi possível apresentar uma lista das temporadas...
        </v-alert>
      </template>

      <template v-slot:items="props">
        <tr @click="rowClicked(props.item)">
          <td class="subheading">{{ props.item.name }}</td>
        </tr>
      </template>
    </v-data-table>
    <div>
      <v-btn @click="go_back()">Página Anterior</v-btn>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
const lhost = 'http://localhost:3000'

export default {
  props: ['idCompetition'],
  data: () => ({
    headers: [
      { text: 'Temporada', align: 'left', sortable: true, value: 'name', class: 'title' }
    ],
    seasons: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/competitions/' + this.idCompetition + '/seasons')
      this.seasons = response.data
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      this.$router.push('/classification/' + item.season.split('#')[1])
    },
    go_back: function () {
      this.$router.go(-1)
    }
  }
}
</script>
