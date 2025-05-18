<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import FDtabs from './components/FDtabs.vue';
import Mypost from './components/Mypost.vue';

const posts = ref([]);
const filteredPosts = ref([]);
const loading = ref(false);
const error = ref(null);
const activeTab = ref('All Posts');
const searchQuery = ref('');

const newPost = ref({
  title: '',
  content: '',
  is_anonymous: true
});

// Pagination variables
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / itemsPerPage));
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredPosts.value.slice(start, end);
});

// Fetch posts from the freedom wall
const fetchPosts = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Updated to use the posts endpoint
    const response = await axios.get('http://127.0.0.1:8000/freedom-wall/api/posts/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    posts.value = response.data || [];
    filterPosts();
    // Reset to first page when posts are loaded
    currentPage.value = 1;
  } catch (err) {
    console.error('Error fetching freedom wall posts:', err.message);
    error.value = 'Failed to load posts. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// Handle search functionality
const handleSearch = (query) => {
  searchQuery.value = query;
  filterPosts();
};

// Handle tab change
const handleTabChange = (tab) => {
  activeTab.value = tab;
  filterPosts();
};

// Filter posts based on active tab and search query
const filterPosts = () => {
  let result = [...posts.value];
  
  // Filter by tab
  if (activeTab.value === 'My Posts') {
    const userId = getCurrentUserId(); // You'll need to implement this function
    result = result.filter(post => post.author_id === userId);
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(post => 
      post.title.toLowerCase().includes(query) || 
      post.content.toLowerCase().includes(query)
    );
  }
  
  filteredPosts.value = result;
  currentPage.value = 1; // Reset to first page when filters change
};

// Get current user ID (placeholder - implement according to your auth system)
const getCurrentUserId = () => {
  // This is a placeholder, replace with your actual implementation
  // For example, you might parse the JWT token or get it from a store
  return localStorage.getItem('userId') || null;
};

// Submit a new post
const submitPost = async () => {
  if (!newPost.value.title.trim() || !newPost.value.content.trim()) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    await axios.post('http://127.0.0.1:8000/freedom-wall/api/posts/', 
      newPost.value,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
    );
    
    // Reset form
    newPost.value = {
      title: '',
      content: '',
      is_anonymous: true
    };
    
    // Refresh posts and switch to All Posts tab
    await fetchPosts();
    activeTab.value = 'All Posts';
    handleTabChange('All Posts');
    
  } catch (err) {
    console.error('Error creating post:', err.message);
    error.value = 'Failed to create post. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// Delete post function
const deletePost = async (postId) => {
  if (!confirm('Are you sure you want to delete this post?')) return;
  
  loading.value = true;
  try {
    await axios.delete(`http://127.0.0.1:8000/freedom-wall/api/posts/${postId}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    await fetchPosts();
  } catch (err) {
    console.error('Error deleting post:', err.message);
    error.value = 'Failed to delete post. Please try again later.';
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
    
    <!-- Tabs Component -->
    <FDtabs 
      @search="handleSearch" 
      @change-tab="handleTabChange"
      @create-post="submitPost"
      @update:title="newPost.title = $event"
      @update:content="newPost.content = $event"
      @update:anonymous="newPost.is_anonymous = $event"
    />
    
    <!-- My Post Component -->
    <Mypost 
      v-if="activeTab !== 'Create Post'"
      :filteredPosts="filteredPosts"
      :loading="loading"
      :searchQuery="searchQuery"
      :activeTab="activeTab"
      :currentPage="currentPage"
      :itemsPerPage="itemsPerPage"
      @delete-post="deletePost"
      @update:currentPage="currentPage = $event"
    />
  </div>
</template>

<style scoped>
.freedom-wall {
  width: 100%;
}
</style>
