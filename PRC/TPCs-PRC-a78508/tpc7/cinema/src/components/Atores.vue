<template>
    <v-container>
        <v-layout row wrap v-if="atores.length > 0">
            <v-flex xs2>
                <h3>Atores</h3>
            </v-flex>
            <v-flex xs10>
                <v-data-table
                    :headers="headers"
                    :items="atores"
                    :class="elevation-1"
                >
                    <template v-slot:no-data>
                        <v-alert :value="true" color="error" icon="warning">
                            Não foi possível apresentar uma lista dos filmes...
                        </v-alert>
                    </template>
                    <template v-slot:items="props">
                        <tr @click="rowClicked(props.item)">
                            <td class="subheading">{{ props.item.nomeAtor }}</td>
                            <td class="subheading">{{ props.item.a}}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-flex>
        </v-layout>
        <v-layout row wrap v-else>
            <v-flex xs12>
                <p>Sem atores associados...</p>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios'
const lhost = 'http://cinema.di.uminho.pt'

export default {
  props: ['idFilme'],
  data: () => ({
    headers: [
      { text: 'Nome', align: 'left', sortable: true, value: 'nomeAtor', class: 'title' },
      { text: 'Identificador', sortable: false, value: 'a', class: 'title' }
    ],
    atores: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/filmes/' + this.idFilme + '/atores')
      this.atores = response.data
    } catch (e) {
      return (e)
    }
  },
  methods: {
    rowClicked: function (item) {
      this.$router.push('/atores/' + item.a.split('#')[1])
    }
  }
}
</script>
