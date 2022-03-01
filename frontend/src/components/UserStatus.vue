<template>
  <div class="status-line">
    <span> {{ name }} </span>
    <span> {{ location }} </span>
    <span> {{ status }} </span>
    <span> {{ scope }} </span>
  </div>
</template>

<script>
export default {
  name: "UsersStatus",
  props: [
      "name", "location", "status", "scope"
  ]
}
</script>

<style scoped lang="sass">

.status-line
  margin: 0 20vw 10px
  display: flex
  justify-content: space-between
  transition-duration: .5s
  transition-property: font-size, margin, color
  font-size: 16px
  &:hover
    font-size: 18px
    margin: 0 15vw 10px
    color: red


</style>