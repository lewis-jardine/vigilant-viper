<template>
  <div id="margin">
    <div id="fix" class="side_bar">
      
      <w-list :key="menuItemsLength" :items="items" nav color="grey">
        <template #item="{ item }">
          <span>{{ item.label }}</span>
          <div class="spacer"></div>
          <w-icon md>{{ item.icon }}</w-icon>
        </template>
      </w-list>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getStreams } from "../services/StreamsService";

const items = ref([
  {
    label: "Overview",
    id: "overview",
    icon: "mdi mdi-camera-burst",
    route: "/",
  },
  {
    label: "Master Log",
    id: "masterlog",
    icon: "mdi mdi-book-open",
    route: "/master",
  }
]);

const menuItemsLength = ref(1);

onMounted(() => {
  getStreams((streams) => {
    let newNavBarItems = items.value;
    streams.forEach(function (obj) {
      var id = obj._id;
      newNavBarItems.push({
        label: obj.name,
        id: "stream" + id,
        icon: "mdi mdi-cctv",
        route: "/stream/" + obj.name,
      });
    });
    items.value = newNavBarItems;

    // update this to force rerender
    menuItemsLength.value= items.value.length;
  });
});
</script>

<style scoped>
#margin {
  margin: 75px;
}
#fix {
  display: block;
  font-size: 16px;
  position: fixed;
  top: 50px;
  left: 0;
  width: 150px;
}
</style>
