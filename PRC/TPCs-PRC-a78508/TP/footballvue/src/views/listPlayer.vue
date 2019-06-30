<template>
  <Player :idPlayer="$route.params.id"/>
</template>

<script>
  import Player from '@/components/Player'  //@ é um alias para src

  export default {
    components: {
      Player
    }
  }
</script>