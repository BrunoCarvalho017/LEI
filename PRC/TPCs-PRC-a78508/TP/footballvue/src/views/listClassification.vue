<template>
  <Classification :idSeason="$route.params.id"/>
</template>

<script>
  import Classification from '@/components/Classification'  //@ é um alias para src

  export default {
    components: {
      Classification
    }
  }
</script>