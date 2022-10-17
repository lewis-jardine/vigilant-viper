<script setup>
import StreamPageWrapper from "../components/StreamPageWrapper.vue";
</script>

<template>
  <main>
    <div>
      <StreamPageWrapper />
    </div>
  </main>
</template>

<style scoped>
div {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-content: center;
}

main {
  flex: 1;
}

@media screen and (max-width: 600px) {
  div {
    padding: 10px;
  }
}
</style>
