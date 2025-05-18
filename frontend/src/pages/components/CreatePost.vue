<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['create-post', 'update:title', 'update:content', 'update:anonymous']);

const title = ref('');
const content = ref('');
const isAnonymous = ref(true);

const updateTitle = (event) => {
  title.value = event.target.value;
  emit('update:title', title.value);
};

const updateContent = (event) => {
  content.value = event.target.value;
  emit('update:content', content.value);
};

const updateAnonymous = (event) => {
  isAnonymous.value = event.target.checked;
  emit('update:anonymous', isAnonymous.value);
};

const createPost = () => {
  emit('create-post');
};
</script>

<template>
  <div class="create-post-container">
    <v-text-field
      v-model="title"
      label="Title"
      variant="outlined"
      counter
      maxlength="100"
      class="mb-3"
      @input="updateTitle"
    ></v-text-field>
    
    <v-textarea
      v-model="content"
      label="What's on your mind?"
      variant="outlined"
      rows="4"
      counter
      maxlength="500"
      class="mb-3"
      @input="updateContent"
    ></v-textarea>
    
    <v-checkbox
      v-model="isAnonymous"
      label="Post anonymously"
      hide-details
      class="mb-4"
      @change="updateAnonymous"
    ></v-checkbox>
    
    <div class="text-right">
      <v-btn 
        color="#FE4F5A" 
        @click="createPost"
        :disabled="!title.trim() || !content.trim()"
      >
        Post
      </v-btn>
    </div>
  </div>
</template>

<style scoped>
.create-post-container {
  max-width: 800px;
  margin: 0 auto;
}
</style>
