<template>
    <v-container>
        <MetaAtor :idAtor="$route.params.id"/>
        <FilmesAtor :idAtor="$route.params.id"/>
        <v-layout>
            <v-btn small @click="$router.go(-1)">Voltar</v-btn>
        </v-layout>
    </v-container>
</template>

<script>
import MetaAtor from '@/components/MetaAtor'
import FilmesAtor from '@/components/FilmesAtor'

export default {
  components: {
    MetaAtor, FilmesAtor
  }
}
</script>
