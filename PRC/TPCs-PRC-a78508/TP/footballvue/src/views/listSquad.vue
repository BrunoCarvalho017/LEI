<template>
  <Squad :idSquad="$route.params.id"/>
</template>

<script>
  import Squad from '@/components/Squad'  //@ é um alias para src

  export default {
    components: {
      Squad
    }
  }
</script>