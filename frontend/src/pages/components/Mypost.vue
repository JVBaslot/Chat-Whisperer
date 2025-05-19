<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { fetchUserPosts, deletePost, updatePost } from '../functions/myPost.js';
import { useAuthStore } from '@/stores/auth';
import EditPost from '../dialogs/EditPost.vue';

const props = defineProps({
  loading: Boolean,
  searchQuery: String,
  currentPage: Number,
  itemsPerPage: Number
});

const emit = defineEmits(['delete-post', 'update:currentPage']);

const authStore = useAuthStore();
const posts = ref([]);
const filteredPosts = ref([]);
const isLoading = ref(false);
const error = ref(null);
const postReactions = ref({});
const showEditDialog = ref(false);
const currentEditPost = ref(null);

// Computed property for paginated posts
const paginatedPosts = computed(() => {
  const start = (props.currentPage - 1) * props.itemsPerPage;
  const end = start + props.itemsPerPage;
  return filteredPosts.value.slice(start, end);
});

// Computed property for total pages
const totalPages = computed(() => 
  Math.ceil(filteredPosts.value.length / props.itemsPerPage)
);

// Generate random reactions for visual effect
const generateRandomVotes = () => {
  return Math.floor(Math.random() * 501);
};

// Fetch user posts
const fetchPosts = async () => {
  isLoading.value = true;
  try {
    const result = await fetchUserPosts();
    
    if (result.success) {
      posts.value = result.data;
      // Initialize reactions for each post
      posts.value.forEach(post => {
        if (!postReactions.value[post.id]) {
          postReactions.value[post.id] = {
            thumbsUp: generateRandomVotes(),
            laugh: generateRandomVotes(),
            heart: generateRandomVotes(),
            angry: generateRandomVotes()
          };
        }
      });
      applyFilters();
    } else {
      error.value = result.error;
    }
  } catch (err) {
    error.value = 'Failed to fetch your posts';
  } finally {
    isLoading.value = false;
  }
};

// Watch for search query changes
watch(() => props.searchQuery, () => {
  applyFilters();
});

// Apply filters based on search query
const applyFilters = () => {
  if (props.searchQuery) {
    const query = props.searchQuery.toLowerCase();
    filteredPosts.value = posts.value.filter(post => 
      post.title.toLowerCase().includes(query) || 
      post.content.toLowerCase().includes(query)
    );
  } else {
    filteredPosts.value = [...posts.value];
  }
  
  // Reset to first page when filters change
  if (props.currentPage !== 1) {
    emit('update:currentPage', 1);
  }
};

// Handle deletion of a post
const handleDeletePost = async (postId) => {
  if (confirm('Are you sure you want to delete this post?')) {
    isLoading.value = true;
    const result = await deletePost(postId);
    
    if (result.success) {
      // Remove the deleted post from the local array
      posts.value = posts.value.filter(post => post.id !== postId);
      applyFilters();
      emit('delete-post', postId);
    } else {
      error.value = result.error;
    }
    isLoading.value = false;
  }
};

// Handle upvoting posts
const upvotePost = (postId, reactionType) => {
  if (!postReactions.value[postId]) {
    postReactions.value[postId] = {
      thumbsUp: 0,
      laugh: 0,
      heart: 0,
      angry: 0
    };
  }
  
  // Increment the selected reaction type
  postReactions.value[postId][reactionType]++;
};

// Handle pagination
const changePage = (page) => {
  emit('update:currentPage', page);
};

// Handle edit button click
const handleEditPost = (post) => {
  currentEditPost.value = { ...post };
  showEditDialog.value = true;
};

// Save edited post
const saveEditedPost = async (updatedPost) => {
  isLoading.value = true;
  try {
    const result = await updatePost(updatedPost.id, {
      title: updatedPost.title,
      content: updatedPost.content
    });
    
    if (result.success) {
      // Update the post in the local array
      const index = posts.value.findIndex(p => p.id === updatedPost.id);
      if (index !== -1) {
        posts.value[index] = { ...posts.value[index], ...updatedPost };
        applyFilters();
      }
      showEditDialog.value = false;
    } else {
      error.value = result.error;
    }
  } catch (err) {
    error.value = 'Failed to update post';
  } finally {
    isLoading.value = false;
  }
};

// Fetch posts when component mounts
onMounted(() => {
  fetchPosts();
});
</script>

<template>
  <div>
    <v-alert v-if="error" type="error" dismissible class="mb-4">
      {{ error }}
    </v-alert>
    
    <div v-if="isLoading || props.loading" class="d-flex justify-center my-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    
    <div v-else-if="filteredPosts.length === 0" class="text-center my-4">
      <v-card class="pa-4 text-center">
        <v-card-text>
          <v-icon x-large color="grey lighten-1">mdi-message-text-outline</v-icon>
          <p class="text-h6 mt-2">No posts found</p>
          <p class="text-body-1" v-if="searchQuery">No results match your search criteria.</p>
          <p class="text-body-1" v-else>You haven't created any posts yet.</p>
        </v-card-text>
      </v-card>
    </div>
    
    <div v-else>
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
                  {{ post.author_name || 'Anonymous' }}
                </div>
                <div>
                  <v-icon small class="mr-1">mdi-clock-outline</v-icon>
                  {{ new Date(post.created_at).toLocaleString() }}
                </div>
              </div>
            </v-card-subtitle>
            <v-card-actions>
              <div class="reactions-container">
                <!-- Thumbs Up -->
                <div class="reaction-item">
                  <v-btn 
                    icon 
                    small 
                    @click="upvotePost(post.id, 'thumbsUp')"
                    class="reaction-btn thumbs-up"
                  >
                    <v-icon>mdi-thumb-up</v-icon>
                  </v-btn>
                  <span class="reaction-count">{{ postReactions[post.id]?.thumbsUp || 0 }}</span>
                </div>
                
                <!-- Other reaction buttons -->
                <div class="reaction-item">
                  <v-btn 
                    icon 
                    small 
                    @click="upvotePost(post.id, 'laugh')"
                    class="reaction-btn laugh"
                  >
                    <v-icon>mdi-emoticon-happy</v-icon>
                  </v-btn>
                  <span class="reaction-count">{{ postReactions[post.id]?.laugh || 0 }}</span>
                </div>
                
                <div class="reaction-item">
                  <v-btn 
                    icon 
                    small 
                    @click="upvotePost(post.id, 'heart')"
                    class="reaction-btn heart"
                  >
                    <v-icon>mdi-heart</v-icon>
                  </v-btn>
                  <span class="reaction-count">{{ postReactions[post.id]?.heart || 0 }}</span>
                </div>
                
                <div class="reaction-item">
                  <v-btn 
                    icon 
                    small 
                    @click="upvotePost(post.id, 'angry')"
                    class="reaction-btn angry"
                  >
                    <v-icon>mdi-emoticon-angry</v-icon>
                  </v-btn>
                  <span class="reaction-count">{{ postReactions[post.id]?.angry || 0 }}</span>
                </div>
              </div>
              
              <v-spacer></v-spacer>
              
              <v-btn 
                icon 
                small 
                color="error" 
                @click="handleDeletePost(post.id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              
              <v-btn 
                icon 
                small 
                color="primary"
                @click="handleEditPost(post)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Pagination -->
      <div class="d-flex justify-center mt-4" v-if="totalPages > 1">
        <v-pagination
          v-model="props.currentPage"
          :length="totalPages"
          :total-visible="5"
          color="#FE4F5A"
          @update:model-value="changePage"
        ></v-pagination>
      </div>
    </div>
    
    <!-- Edit Post Dialog -->
    <EditPost
      v-model:show="showEditDialog"
      :post="currentEditPost"
      @save="saveEditedPost"
    />
  </div>
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

.reactions-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.reaction-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.reaction-btn {
  min-width: 36px;
  height: 36px;
  padding: 0;
}

.reaction-count {
  font-size: 0.875rem;
  font-weight: bold;
  color: #555;
}

.thumbs-up {
  color: #4285F4;
}

.laugh {
  color: #FBBC05;
}

.heart {
  color: #EA4335;
}

.angry {
  color: #F25022;
}

.reaction-btn:hover {
  background-color: #e0e0e0;
  transform: scale(1.1);
  transition: transform 0.2s;
}
</style>
