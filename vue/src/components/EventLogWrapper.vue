<template>
  <EventLog v-if="events !== []" :events="events" :stream-title="streamTitle" @play-clip="$emit('play-clip',$event)" :master-log="false"/>
  <h1 v-else>Loading event log...</h1>
</template>

<script setup>
import { ref, computed, defineProps, onMounted, onUnmounted } from "vue";
import { useEventsStore } from '@/stores/events';
import EventLog from "./EventLog.vue";
const eventsStore = useEventsStore();

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

const events = computed(() => eventsStore.allEvents.slice()
.reverse()
.filter((event) => event.type.indexOf("movement") === -1)  // ignore start stream events to declutter
.filter((event) => event.streamID == props.streamId)); // only take events for the chosen stream

const socket = ref(null);

onMounted(() => {
  // fetch event details from API
  const domainParts = window.location.origin.split(":");
  const domain = `${domainParts[0]}:${domainParts[1]}`;
  const port = 5000;
  const url = `${domain}:${port}/stream/${props.streamId}/events`;
  fetch(url).then((jsonData) => {
    jsonData.json().then((data) => {
      eventsStore.allEvents = eventsStore.allEvents.concat(data.events);
    });
  });
});

onUnmounted(() => {
  if(socket.value !== null)
  {
    socket.value.close();
  }
})
</script>
