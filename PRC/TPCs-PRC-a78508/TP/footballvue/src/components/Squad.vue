<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="squad"
      class="elevation-1"
    >
      <template v-slot:no-data>
        <v-alert :value="true" color="error" icon="warning">
          Não foi possível apresentar o plantel...
        </v-alert>
      </template>

      <template v-slot:items="props">
        <tr @click="rowClicked(props.item)">
          <td class="subheading">{{ props.item.jnr }}</td>
          <td class="subheading">{{ props.item.pname }}</td>
          <td class="subheading">{{ props.item.pos }}</td>
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
  props: ['idSquad'],
  data: () => ({
    headers: [
      { text: 'Camisola', align: 'left', sortable: true, value: 'jnr', class: 'title' },
      { text: 'Nome', align: 'left', sortable: true, value: 'pname', class: 'title' },
      { text: 'Posição', align: 'left', sortable: true, value: 'pos', class: 'title' }
    ],
    squad: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/squad/' + this.idSquad )
      this.squad = response.data
      console.log(this.squad)
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      console.log(item)
      this.$router.push('/player/' + item.p.split('#')[1])
    },
    go_back: function () {
      this.$router.go(-1)
    }
  }
}
</script>
