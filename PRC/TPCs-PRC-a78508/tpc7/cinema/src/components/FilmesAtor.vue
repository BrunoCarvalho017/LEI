<template>
    <v-container>
        <v-layout row wrap v-if="filmes.length > 0">
            <v-flex xs2>
                <h3>Filmes</h3>
            </v-flex>
            <v-flex xs10>
                <v-data-table
                    :headers="headers"
                    :items="filmes"
                    :class="elevation-1"
                >
                    <template v-slot:no-data>
                        <v-alert :value="true" color="error" icon="warning">
                            Não foi possível apresentar uma lista dos filmes...
                        </v-alert>
                    </template>
                    <template v-slot:items="props">
                        <tr>
                            <td class="subheading">{{ props.item.ftit }}</td>
                            <td class="subheading">{{ props.item.f}}</td>
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
  props: ['idAtor'],
  data: () => ({
    headers: [
      { text: 'Título', align: 'left', sortable: true, value: 'ftit', class: 'title' },
      { text: 'Identificador', sortable: false, value: 'f', class: 'title' }
    ],
    filmes: []
  }),
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/atores/' + this.idAtor + '/filmes')
      this.filmes = response.data
    } catch (e) {
      return (e)
    }
  }
}
</script>
