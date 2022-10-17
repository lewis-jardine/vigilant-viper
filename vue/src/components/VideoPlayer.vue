<template>
  <video :id="'player' + props.videoid" class="video-js video-box"></video>
</template>

<script setup>
import { onMounted, ref, onUnmounted, watch } from "vue";

// VideoJs import
import videojs from "video.js";

// Video.js css
import "video.js/dist/video-js.min.css";

const player = ref({});

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  videoid: {
    type: String,
    required: true,
  },
});

watch(
  () => props.src,
  (val) => {
    //Reload video source
    player.value?.loadMedia({ src: val, type: props.type }, () => {});
  }
);
onMounted(() => {
  player.value = videojs("player" + props.videoid, {
    autoplay: true,
    muted: true,
    controls: true,
    fluid: true,
    aspectRatio: "16:9",
    fill: true,
    liveui: true,
    sources: [
      {
        src: props.src,
        type: props.type,
      },
    ],
  });
});
onUnmounted(() => {
  player.value?.dispose();
});
</script>
