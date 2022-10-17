Parent container for streams
<template>
  <h1>{{ streams[selectedStreamIndex].name }}</h1>
  <div id="PlayerEvent">
    <VideoPlayer :src="playerSrc" :type="playerType" />

    <EventLogWrapper
      :stream-id="streams[selectedStreamIndex]._id"
      :stream-title="streams[selectedStreamIndex].name"
      @play-clip="(clipUrl) => playClip(clipUrl)"
    />
  </div>
  <template v-if="playerType !== 'application/x-mpegURL'">
    <span>
      <label for="back-to-stream-btn">Playing clip</label>
      <w-button
        id="back-to-stream-btn"
        @click="() => playLiveStream()"
        style="margin-top: 20px; width: 20%"
        class="ma1"
        color="black"
        outline
      >
        Back to live stream
      </w-button>
    </span>
  </template>
</template>

<script setup>
import { defineProps, ref } from "vue";
import EventLogWrapper from "./EventLogWrapper.vue";
import VideoPlayer from "./VideoPlayer.vue";
const props = defineProps({
  selectedStreamIndex: {
    type: Number,
    required: true,
  },
  streams: {
    type: Array,
    required: true,
  },
});

const playerSrc = ref(props.streams[props.selectedStreamIndex].url);
const playerType = ref("application/x-mpegURL");

const playLiveStream = () => {
  // videojs is not playing nice with reloading live streams, so just force a refresh
  window.location.reload();
};

const playClip = (clipUrl) => {
  playerSrc.value = "http://localhost:5000/static" + clipUrl;
  playerType.value = "video/mkv";
};
</script>

<style scoped>
label {
  margin-right: 15px;
}
</style>
