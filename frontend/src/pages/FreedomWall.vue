<script setup>
import { ref, onMounted } from 'vue';
import { useFreedomWall } from './functions/freedomwall.js';
import FDtabs from './components/FDtabs.vue';
import Allpost from './components/Allpost.vue';
import Mypost from './components/Mypost.vue';

// Get the freedom wall functionality from the composable
const { loading, error, fetchPosts, createPost } = useFreedomWall();

const activeTab = ref('All Posts');
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 6;
const posts = ref([]);
const filteredPosts = ref([]);

const newPost = ref({
  title: '',
  content: '',
  is_anonymous: true
});

// Fetch all posts for the "All Posts" tab
const getAllPosts = async () => {
  try {
    posts.value = await fetchPosts();
    filterPosts();
    // Reset to first page when posts are loaded
    currentPage.value = 1;
  } catch (err) {
    // Error handling is managed by the composable
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
  
  // Only fetch all posts when switching to All Posts tab
  if (tab === 'All Posts') {
    getAllPosts();
  }
  
  // Reset page when switching tabs
  currentPage.value = 1;
};

// Filter posts based on search query (for All Posts tab)
const filterPosts = () => {
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filteredPosts.value = posts.value.filter(post => 
      post.title.toLowerCase().includes(query) || 
      post.content.toLowerCase().includes(query)
    );
  } else {
    filteredPosts.value = [...posts.value];
  }
};

// Submit a new post
const submitPost = async () => {
  if (!newPost.value.title.trim() || !newPost.value.content.trim()) return;
  
  try {
    await createPost(newPost.value);
    
    // Reset form
    newPost.value = {
      title: '',
      content: '',
      is_anonymous: true
    };
    
    // Switch to All Posts tab after creating a post
    activeTab.value = 'All Posts';
    handleTabChange('All Posts');
    
  } catch (err) {
    // Error handling is managed by the composable
  }
};

// Handle post deletion
const handleDeletePost = () => {
  // Refresh the posts for the current tab
  if (activeTab.value === 'All Posts') {
    getAllPosts();
  }
  // My Posts component handles its own refresh
};

onMounted(() => {
  // Initialize the page with All Posts tab
  activeTab.value = 'All Posts';
  getAllPosts();
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
    
    <!-- All Posts Component (used for All Posts tab) -->
    <Allpost 
      v-if="activeTab === 'All Posts'"
      :filteredPosts="filteredPosts"
      :loading="loading"
      :searchQuery="searchQuery"
      :activeTab="activeTab"
      :currentPage="currentPage"
      :itemsPerPage="itemsPerPage"
      @delete-post="handleDeletePost"
      @update:currentPage="currentPage = $event"
    />
    
    <!-- My Posts Component (used for My Posts tab) -->
    <Mypost 
      v-if="activeTab === 'My Posts'"
      :loading="loading"
      :searchQuery="searchQuery"
      :currentPage="currentPage"
      :itemsPerPage="itemsPerPage"
      @delete-post="handleDeletePost"
      @update:currentPage="currentPage = $event"
    />
    
    <!-- Create Post tab is handled by FDtabs component -->
  </div>
</template>

<style scoped>
.freedom-wall {
  width: 100%;
}
</style>