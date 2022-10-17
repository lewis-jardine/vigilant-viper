<script setup>
import StreamPageWrapper from "../components/StreamPageWrapper.vue";
import VideoPlayer from "../components/VideoPlayer.vue";
import EventLog from "../components/EventLog.vue";

import { ref, computed, defineProps, onMounted, onUnmounted } from "vue";
import { useEventsStore } from "@/stores/events";
import { getStreams } from "../services/StreamsService";
import SearchBar from "../components/SearchBar.vue";
const eventsStore = useEventsStore();
// TODO filter these by stream ID
const events = computed(() =>
  eventsStore.allEvents
    .slice()
    .reverse()
    .filter((event) => event.type.indexOf("movement") === -1)
); // ignore start stream events to declutter
const socket = ref(null);
const props = defineProps({
  streamId: {
    type: Number,
    required: true,
  },
  streamTitle: {
    type: String,
    required: true,
  },
});

const streams = ref([]);
const currentSearchTerm = ref("")
onMounted(() => {
  // fetch event details from API
  const domainParts = window.location.origin.split(":");
  const domain = `${domainParts[0]}:${domainParts[1]}`;
  const port = 5000;
  const url = `${domain}:${port}/events`;
  getStreams((streamDetails) => {
    streams.value = streamDetails;
  });
  fetch(url).then((jsonData) => {
    jsonData.json().then((data) => {
      // TODO filter these into order in case any live ones snuck in before this resolves
      eventsStore.allEvents = data.events;
    });
  });
});

const searchActivated = (searchTerm) => {
  currentSearchTerm.value = searchTerm;
}
const searchCleared = () => {
  currentSearchTerm.value = "";
}

const filterEvents = (eventsToFilter) => {
  console.log(currentSearchTerm.value);
  console.log(eventsToFilter);
  if(currentSearchTerm.value === "")
  {
    console.log("returning all events")
    return eventsToFilter;
  }
  const matches = eventsToFilter
  .filter((item) => item.detail.join("").indexOf(currentSearchTerm.value) !== -1);
  console.log("matches");
  console.log(matches);
  return matches;
}

</script>

<template>
  <main>
    <SearchBar @searchActivated="searchActivated" @searchCleared="searchCleared"/>
    <div>
      <template :key="streams" v-if="streams !== []">
      <div id="master-log-box">
        <EventLog :key="currentSearchTerm" v-if="events !== []" :events="filterEvents(events)" :streams="streams" :stream-title="streamTitle" @play-clip="$emit('play-clip',$event)" :master-log="true"/>
      </div>
    </template>
    </div>
  </main>
</template>

<style scoped>
div {
  padding: 20px;
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
