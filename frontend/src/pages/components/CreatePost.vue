<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['create-post', 'update:title', 'update:content', 'update:anonymous', 'navigate-to-all-posts']);

const title = ref('');
const content = ref('');
const isAnonymous = ref(true); // Default to anonymous for privacy
const loadingDialog = ref(false); // Add loading dialog ref

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
  loadingDialog.value = true; // Show the loading dialog
  emit('create-post');
  
  // Simulate posting process with 3 seconds delay
  setTimeout(() => {
    loadingDialog.value = false; // Hide the loading dialog
    emit('navigate-to-all-posts'); // Emit event to navigate to all posts
    // Reset form
    title.value = '';
    content.value = '';
  }, 3000);
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
      label="Post anonymously (your identity will be hidden, but you'll still own the post)"
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
    
    <!-- Loading Dialog -->
    <v-dialog v-model="loadingDialog" persistent width="300">
      <v-card>
        <v-card-text class="text-center pa-5">
          <v-progress-circular indeterminate color="#FE4F5A" size="64" class="mb-3"></v-progress-circular>
          <p class="mb-0 mt-2">Posting your content...</p>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.create-post-container {
  max-width: 800px;
  margin: 0 auto;
}
</style>
