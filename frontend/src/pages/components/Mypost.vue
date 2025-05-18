<script setup>
import { computed, defineProps, defineEmits } from 'vue';

const props = defineProps({
  filteredPosts: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  searchQuery: {
    type: String,
    default: ''
  },
  activeTab: {
    type: String,
    default: 'All Posts'
  },
  currentPage: {
    type: Number,
    default: 1
  },
  itemsPerPage: {
    type: Number,
    default: 6
  }
});

const emit = defineEmits(['delete-post', 'update:currentPage']);

const totalPages = computed(() => Math.ceil(props.filteredPosts.length / props.itemsPerPage));
const paginatedPosts = computed(() => {
  const start = (props.currentPage - 1) * props.itemsPerPage;
  const end = start + props.itemsPerPage;
  return props.filteredPosts.slice(start, end);
});

const goToPage = (page) => {
  emit('update:currentPage', page);
};

const deletePost = (postId) => {
  emit('delete-post', postId);
};
</script>

<template>
  <!-- Loading State -->
  <div v-if="loading && !filteredPosts.length" class="text-center my-6">
    <v-progress-circular indeterminate color="#FE4F5A"></v-progress-circular>
    <p class="mt-2">Loading posts...</p>
  </div>
  
  <!-- Posts Display with Grid Layout -->
  <div v-if="filteredPosts.length">
    <v-row>
      <v-col v-for="post in paginatedPosts" 
             :key="post.id" 
             cols="12" sm="6" md="4">
        <v-card elevation-10 class="mb-4 post-card" height="100%">
          <v-card-title>{{ post.title }}</v-card-title>
          <v-card-text>
            <p class="text-body-1">{{ post.content }}</p>
          </v-card-text>
          <v-card-subtitle>
            <div class="d-flex justify-space-between align-center">
              <div>
                <v-icon small class="mr-1">mdi-account</v-icon>
                {{ post.author_name }}
              </div>
              <div>
                <v-icon small class="mr-1">mdi-clock-outline</v-icon>
                {{ new Date(post.created_at).toLocaleString() }}
              </div>
            </div>
          </v-card-subtitle>
          <v-card-actions v-if="post.can_edit">
            <v-spacer></v-spacer>
            <v-btn 
              icon 
              small 
              color="error" 
              @click="deletePost(post.id)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Pagination Controls -->
    <div class="text-center mt-4">
      <v-pagination
        :model-value="currentPage"
        :length="totalPages"
        :total-visible="5"
        color="#FE4F5A"
        @update:model-value="goToPage"
      ></v-pagination>
    </div>
  </div>
  
  <!-- Empty State -->
  <v-card v-else-if="!loading && !filteredPosts.length" class="pa-4 text-center">
    <v-card-text>
      <v-icon x-large color="grey lighten-1">mdi-message-text-outline</v-icon>
      <p class="text-h6 mt-2">No posts found</p>
      <p class="text-body-1" v-if="searchQuery">No results match your search criteria.</p>
      <p class="text-body-1" v-else-if="activeTab === 'My Posts'">You haven't created any posts yet.</p>
      <p class="text-body-1" v-else>There are no posts on the freedom wall yet.</p>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.post-card {
  border-left: 4px solid #FE4F5A;
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}
</style>
