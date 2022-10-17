This fetches the list of streams and then passes the info through to a
StreamPage once it has it

<template>
  <StreamPage
    v-if="streams.length !== 0 && selectedStreamIndex !== null"
    :selected-stream-index="selectedStreamIndex"
    :streams="streams"
    :key="selectedStreamIndex"
  />
  <h1 v-else>Loading streams...</h1>
</template>

<script setup>
import StreamPage from "./StreamPage.vue";
import { getStreams } from "../services/StreamsService";
import { useRoute } from "vue-router";
import { watch, ref, onMounted } from "vue";

const selectedStreamIndex = ref(null);
const streams = ref([]);

const route = useRoute();
watch(
  () => route.params.id,
  async (newId) => {
    // search list of streams to find one that matches the Id
    const selectedStream = streams.value.findIndex(
      (item) => item.name === newId
    );
    if (selectedStream !== undefined) {
      selectedStreamIndex.value = selectedStream;
    }
  }
);

onMounted(() => {
  getStreams((availableStreams) => {
    streams.value = availableStreams;

    // check current route when mounted and set stream
    // TODO reduce duplicated code here
    const selectedStream = streams.value.findIndex(
      (item) => item.name === route.params.id
    );
    if (selectedStream !== undefined) {
      selectedStreamIndex.value = selectedStream;
    }
  });
});
</script>
