
<!-- 
    This component provides the search bar 
 -->
<script setup>
import {ref} from 'vue'
const emit = defineEmits(['searchActivated', 'searchCleared'])
// Used to track the current search term - linked to the text input field
const searchTerm = ref("")
const clearSearchTermFromUI = () => {
    // Notify parent and clear value to update the input field and make it blank
    emit('searchCleared')
    searchTerm.value = "";
}
</script>

<template>
<div class="searchbar-wrapper">

    <input outlined v-model="searchTerm" @keyup.enter="$emit('searchActivated', searchTerm)" placeholder="Enter search term here" />
    <button @click="$emit('searchActivated', searchTerm)">Search!</button>
    <button @click="clearSearchTermFromUI">Clear search term</button>

</div>
</template>

<style scoped>
button {
    margin: 5px;
}
input   {
    margin: 5px;
}
.searchbar-wrapper {
    background-color:gray;      
}
</style>

