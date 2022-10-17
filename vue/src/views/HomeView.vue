<script setup>
import { onMounted, ref } from "vue";
import VideoPlayer from "../components/VideoPlayer.vue";
import { getStreams } from "../services/StreamsService";

const streams = ref([]);

onMounted(() => {
  getStreams((availableStreams) => {
    streams.value = availableStreams;
  });
});
</script>

<template>
  <main>
    <div class="grid-container">
      <template v-for="i in streams">
        <div class="grid-item">
          <h2>{{ i.name }}</h2>
          <VideoPlayer
            :videoid="i._id"
            :src="i.url"
            type="application/x-mpegURL"
          />
        </div>
      </template>
    </div>
  </main>
</template>

<style scoped>
div {
  padding: 20;
  display: flex;
  flex-direction: column;
  align-content: center;
}

.grid-container {
  display: grid;
  grid-template-columns: 40% 40%;
  margin: 3%;
}
main {
  width: 100%;
}

h2 {
  padding-bottom: 10px;
}
.grid-item {
  padding: 5%;
  text-align: center;
}

@media screen and (max-width: 600px) {
  div {
    padding: 10px;
  }
}
</style>
