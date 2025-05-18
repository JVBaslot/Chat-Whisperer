<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const posts = ref([]);
const newPost = ref('');
const loading = ref(false);
const error = ref(null);

// Fetch posts from the freedom wall
const fetchPosts = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Replace with your actual API endpoint
    const response = await axios.get('http://127.0.0.1:8000/api/freedom-wall/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    posts.value = response.data.data || [];
  } catch (err) {
    console.error('Error fetching freedom wall posts:', err.message);
    error.value = 'Failed to load posts. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// Submit a new post to the freedom wall
const submitPost = async () => {
  if (!newPost.value.trim()) return;
  
  loading.value = true;
  error.value = null;
  try {
    // Replace with your actual API endpoint
    await axios.post(
      'http://127.0.0.1:8000/api/freedom-wall/',
      { content: newPost.value },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
    );
    newPost.value = '';
    fetchPosts(); // Refresh the posts
  } catch (err) {
    console.error('Error submitting post:', err.message);
    error.value = 'Failed to submit your post. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPosts();
});
</script>

<template>
  <div class="freedom-wall">
    <h2 class="text-h4 mb-4 font-weight-bold">Freedom Wall</h2>
    
    <!-- Error Alert -->
    <v-alert v-if="error" type="error" dismissible class="mb-4">
      {{ error }}
    </v-alert>
    
    <!-- New Post Form -->
    <v-card class="mb-6 pa-4">
      <v-card-title class="text-h6">Share your thoughts anonymously</v-card-title>
      <v-card-text>
        <v-textarea
          v-model="newPost"
          label="What's on your mind?"
          variant="outlined"
          rows="3"
          counter
          maxlength="500"
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          :loading="loading"
          :disabled="!newPost.trim()"
          color="#FE4F5A"
          @click="submitPost"
        >
          Post Anonymously
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <!-- Loading State -->
    <div v-if="loading && !posts.length" class="text-center my-6">
      <v-progress-circular indeterminate color="#FE4F5A"></v-progress-circular>
      <p class="mt-2">Loading posts...</p>
    </div>
    
    <!-- Posts Display -->
    <div v-if="posts.length">
      <v-card v-for="(post, index) in posts" :key="index" class="mb-4 post-card">
        <v-card-text>
          <p class="text-body-1">{{ post.content }}</p>
        </v-card-text>
        <v-card-subtitle class="pb-0">
          <v-icon small class="mr-1">mdi-clock-outline</v-icon>
          {{ new Date(post.created_at).toLocaleString() }}
        </v-card-subtitle>
      </v-card>
    </div>
    
    <!-- Empty State -->
    <v-card v-else-if="!loading" class="pa-4 text-center">
      <v-card-text>
        <v-icon x-large color="grey lighten-1">mdi-message-text-outline</v-icon>
        <p class="text-h6 mt-2">No posts yet!</p>
        <p class="text-body-1">Be the first to share your thoughts on the freedom wall.</p>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.freedom-wall {
  width: 100%;
}

.post-card {
  border-left: 4px solid #FE4F5A;
  transition: transform 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}
</style>
