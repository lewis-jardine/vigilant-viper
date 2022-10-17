Yes, the date handling is hideous, but it works
<template>
  <div class="event-box" style="overflow:hidden">
    <div>
      <h3 >Events: {{ streamTitle }}</h3>
      <div class="fade_rule_stream"><br></div>
    </div>
    <div class="event-box_invert">
      <template v-for="item in events" :key="item['eventID']">
      <StreamEvent
        :timestamp="formatDate(new Date(item.timestamp * 1000))"
        :type="item.type"
        :detail="item.detail"
        :footage="item.clip_url"
        @play-clip="$emit('play-clip',$event)"
        :masterLog="masterLog"
        :stream-title="getStreamTitleFromId(item.streamID, streams)"
      />
    </template>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import StreamEvent from "./StreamEvent.vue";

const getStreamTitleFromId = ((streamId, streams) => {
  if(!streams)
  {
    return "";
  }
  const matchingStream = streams.filter((stream)=>stream._id === streamId);
  if(matchingStream.length === 1)
  {
    return matchingStream[0].name;
  }
  return "";
});

defineProps({
  events: {
    type: Array,
    required: true,
  },
  streamTitle: {
    type: String,
    required: true,
  },
  masterLog: {
    type: Boolean,
    required: true,
  },
  streams: {
    type: Array,
    required: false
  }
});



const padTo2Digits = (num) => {
  return num.toString().padStart(2, "0");
};

const formatDate = (date) => {
  return (
    [
      padTo2Digits(date.getDate()),
      padTo2Digits(date.getMonth() + 1),
      date.getFullYear(),
    ].join("/") +
    " " +
    [
      padTo2Digits(date.getHours()),
      padTo2Digits(date.getMinutes()),
      padTo2Digits(date.getSeconds()),
    ].join(":")
  );
};
</script>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}
</style>
