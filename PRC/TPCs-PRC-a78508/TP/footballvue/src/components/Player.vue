<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="jogador"
      class="elevation-1"
    >
      <template v-slot:no-data>
        <v-alert :value="true" color="error" icon="warning">
          Não foi possível apresentar o jogador...
        </v-alert>
      </template>

      <template v-slot:items="props">
        <tr>
          <td class="subheading">{{ props.item.nat }}</td>
          <td class="subheading">{{ props.item.p }}</td>
          <td class="subheading">{{ props.item.bplace }}</td>
          <td class="subheading">{{ props.item.bdate }}</td>
          <td class="subheading">{{ props.item.name }}</td>
          <td class="subheading">{{ props.item.h }}</td>
          <td class="subheading">{{ props.item.jnr }}</td>
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
  props: ['idPlayer'],
  data: () => ({
    headers: [
      { text: 'Naturalidade', align: 'left', sortable: true, value: 'nat', class: 'title' },
      { text: 'Podição', align: 'left', sortable: true, value: 'p', class: 'title' },
      { text: 'Local Nasc', align: 'left', sortable: true, value: 'bplace', class: 'title' },
      { text: 'Data Nasc', align: 'left', sortable: true, value: 'bdate', class: 'title' },
      { text: 'Nome', align: 'left', sortable: true, value: 'name', class: 'title' },
      { text: 'Altura', align: 'left', sortable: true, value: 'h', class: 'title' },
      { text: 'Camisola', align: 'left', sortable: true, value: 'jnr', class: 'title' },
    ],
    jogador: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/player/' + this.idPlayer )
      this.jogador = response.data
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      this.$router.push('/competitions/' + item.comp.split('#')[1] + '/seasons')
    },
    go_back: function () {
      this.$router.go(-1)
    }
  }
}
</script>
