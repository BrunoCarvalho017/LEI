<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="classification"
      class="elevation-1"
    >
      <template v-slot:no-data>
        <v-alert :value="true" color="error" icon="warning">
          Não foi possível apresentar a classificação desta temporada...
        </v-alert>
      </template>

      <template v-slot:items="props">
        <tr @click="rowClicked(props.item)">
          <td class="subheading">{{ props.item.pos }}</td>
          <td class="subheading">{{ props.item.squad }}</td>
          <td class="subheading">{{ props.item.pg }}</td>
          <td class="subheading">{{ props.item.win }}</td>
          <td class="subheading">{{ props.item.draw }}</td>
          <td class="subheading">{{ props.item.loss }}</td>
          <td class="subheading">{{ props.item.sg }}</td>
          <td class="subheading">{{ props.item.cg }}</td>
          <td class="subheading">{{ props.item.p }}</td>
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
  props: ['idSeason'],
  data: () => ({
    headers: [
      { text: 'Pos', align: 'left', sortable: true, value: 'pos', class: 'title' },
      { text: 'Equipa', align: 'left', sortable: true, value: 'squad', class: 'title' },
      { text: 'JJ', align: 'left', sortable: true, value: 'pg', class: 'title' },
      { text: 'V', align: 'left', sortable: true, value: 'win', class: 'title' },
      { text: 'E', align: 'left', sortable: true, value: 'draw', class: 'title' },
      { text: 'D', align: 'left', sortable: true, value: 'loss', class: 'title' },
      { text: 'GM', align: 'left', sortable: true, value: 'sc', class: 'title' },
      { text: 'GS', align: 'left', sortable: true, value: 'cg', class: 'title' },
      { text: 'P', align: 'left', sortable: true, value: 'p', class: 'title' }
    ],
    classification: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/classification/' + this.idSeason )
      this.classification = response.data
      console.log(lhost+'/classification/'+this.idSeason)
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      console.log(2)
      console.log(item.squadid.split("#")[1]  )
      this.$router.push('/squad/' + item.squadid.split("#")[1])
    },
    go_back: function () {
      this.$router.go(-1)
    }
  }
}
</script>
