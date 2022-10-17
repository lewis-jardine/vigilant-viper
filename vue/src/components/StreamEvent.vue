<template>
  <div class="fade_rule"><br /></div>
  <template v-if="masterLog === true">
    <p>{{streamTitle}}</p>
  </template>
  <p>
    {{ timestamp }}: {{ type }} was detected:
    <br/>
    <template v-for="entry in detail">
      <span>{{entry}}</span>
      <br/>  
    </template>
    <w-button
      v-if="footage.length !== 0 && footage.indexOf('.webm') != -1 && !masterLog"
      @click="$emit('play-clip', footage)"
      class="ma1"
      outline
      color="black"
      >Watch here</w-button
    >
  </p>
</template>

<script setup>
import { defineProps, computed } from "vue";
const props = defineProps({
  timestamp: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true
  },
  detail: {
    type: Array,
    required: true,
  },
  footage: {
    type: String,
    required: false,
  },
  masterLog: {
    type: Boolean,
    required: true,
  },
  streamTitle: {
    type: String,
    required: false
  }
  
});

</script>
