<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useEventsStore } from '@/stores/events';
import StreamPageWrapper from "./components/StreamPageWrapper.vue";
import AppHeader from "./components/AppHeader.vue";
import "@mdi/font/css/materialdesignicons.min.css";
import Sidebar from "./components/Sidebar.vue";

const store = useEventsStore();
const socket = new WebSocket("ws://localhost:5001");

socket.addEventListener("open", (event) => {
  socket.send("Socket open!!");
});

socket.addEventListener("message", (event) => {
  const message = JSON.parse(
    event.data.slice(event.data.indexOf('{'),
    event.data.lastIndexOf('}') + 1)
  );
  store.allEvents.push(message);
});
</script>

<template>
  <w-app>
    <AppHeader />
    <div>
      <Sidebar />
      <RouterView />
    </div>
  </w-app>
</template>

<style scoped>
div {
  display: flex;
  align-content: stretch;
}
</style>
