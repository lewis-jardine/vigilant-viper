import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useEventsStore = defineStore("the_events", () => {
  const allEvents = ref([]);
  
  return { allEvents };
});
