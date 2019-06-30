<template>
  <Seasons :idCompetition="$route.params.id"/>
</template>

<script>
  import Seasons from '@/components/Seasons'  //@ é um alias para src

  export default {
    components: {
      Seasons
    }
  }
</script>