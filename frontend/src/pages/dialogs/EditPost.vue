<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  post: Object
});

const emit = defineEmits(['update:show', 'save']);

const title = ref('');
const content = ref('');
const loading = ref(false);
const error = ref(null);

// Reset form when dialog opens with new post data
watch(() => props.post, (newPost) => {
  if (newPost) {
    title.value = newPost.title || '';
    content.value = newPost.content || '';
    error.value = null;
  }
}, { immediate: true });

// Close the dialog
const close = () => {
  emit('update:show', false);
};

// Save the updated post
const savePost = () => {
  // Validate
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Title and content are required';
    return;
  }
  
  loading.value = true;
  
  // Emit event to parent with updated data
  emit('save', {
    id: props.post?.id,
    title: title.value,
    content: content.value
  });
  
  // Parent component will handle the actual API call
  loading.value = false;
};
</script>

<template>
  <v-dialog v-model="props.show" max-width="600px" @click:outside="close">
    <v-card>
      <v-card-title class="headline">
        Edit Post
      </v-card-title>
      
      <v-card-text>
        <v-alert v-if="error" type="error" dismissible class="mb-4">
          {{ error }}
        </v-alert>
        
        <v-form @submit.prevent="savePost">
          <v-text-field
            v-model="title"
            label="Title"
            required
            :disabled="loading"
          ></v-text-field>
          
          <v-textarea
            v-model="content"
            label="Content"
            required
            rows="5"
            :disabled="loading"
          ></v-textarea>
        </v-form>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="grey darken-1" 
          text 
          @click="close"
          :disabled="loading"
        >
          Cancel
        </v-btn>
        <v-btn 
          color="primary" 
          @click="savePost"
          :loading="loading"
          :disabled="loading"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
