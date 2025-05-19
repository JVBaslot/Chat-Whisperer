<script setup>
import { computed, defineProps, defineEmits, ref, onMounted, watch } from 'vue';

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
const postReactions = ref({});

// Function to generate random number between 0 and 100 (more realistic values)
const generateRandomVotes = () => {
  return Math.floor(Math.random() * 101);
};

// Load reactions from localStorage or initialize with random values if not present
onMounted(() => {
  const savedReactions = localStorage.getItem('postReactions');
  if (savedReactions) {
    postReactions.value = JSON.parse(savedReactions);
  }
  
  // Only initialize reactions for posts that don't have them yet
  props.filteredPosts.forEach(post => {
    if (!postReactions.value[post.id]) {
      postReactions.value[post.id] = {
        thumbsUp: generateRandomVotes(),
        laugh: generateRandomVotes(),
        heart: generateRandomVotes(),
        angry: generateRandomVotes()
      };
    }
  });
  
  // Save to localStorage
  localStorage.setItem('postReactions', JSON.stringify(postReactions.value));
});

// Update postsWithReactions to only ensure reactions exist for each post
const postsWithReactions = computed(() => {
  return paginatedPosts.value.map(post => {
    if (!postReactions.value[post.id]) {
      postReactions.value[post.id] = {
        thumbsUp: generateRandomVotes(),
        laugh: generateRandomVotes(),
        heart: generateRandomVotes(),
        angry: generateRandomVotes()
      };
      // Save to localStorage when new reactions are generated
      localStorage.setItem('postReactions', JSON.stringify(postReactions.value));
    }
    return post;
  });
});

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
  
  // Save updated reactions to localStorage
  localStorage.setItem('postReactions', JSON.stringify(postReactions.value));
};

// Watch for new posts and ensure they have reaction counts
watch(() => props.filteredPosts, (newPosts) => {
  let updated = false;
  newPosts.forEach(post => {
    if (!postReactions.value[post.id]) {
      postReactions.value[post.id] = {
        thumbsUp: generateRandomVotes(),
        laugh: generateRandomVotes(),
        heart: generateRandomVotes(),
        angry: generateRandomVotes()
      };
      updated = true;
    }
  });
  
  if (updated) {
    localStorage.setItem('postReactions', JSON.stringify(postReactions.value));
  }
}, { deep: true });
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
              
              <!-- Laugh -->
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
              
              <!-- Heart -->
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
              
              <!-- Angry -->
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
              v-if="post.can_edit"
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
        color="#151515"
        active-class="pagination-active"
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
.pagination-container {
  background-color: #FE4F5A;
  padding: 8px;
  border-radius: 4px;
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
