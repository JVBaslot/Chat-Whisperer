<script setup>
import { ref, defineEmits } from 'vue';
import CreatePost from './CreatePost.vue';

const emit = defineEmits(['search', 'change-tab', 'create-post', 'update:title', 'update:content', 'update:anonymous']);

const tab = ref(0);
const tabs = ['All Posts', 'My Posts', 'Create Post'];
const searchQuery = ref('');

const handleSearch = () => {
  emit('search', searchQuery.value);
};

const handleTabChange = (newTab) => {
  tab.value = newTab;
  emit('change-tab', tabs[newTab]);
};

const clearSearch = () => {
  searchQuery.value = '';
  emit('search', '');
};

const createPost = () => {
  emit('create-post');
};

const handleUpdateTitle = (value) => {
  emit('update:title', value);
};

const handleUpdateContent = (value) => {
  emit('update:content', value);
};

const handleUpdateAnonymous = (value) => {
  emit('update:anonymous', value);
};
</script>

<template>
  <v-card flat class="mb-6">
    <v-card-text>
      <div class="d-flex flex-wrap justify-space-between align-center mb-4">
        <v-tabs
          v-model="tab"
          background-color="transparent"
          color="#FE4F5A"
          @update:model-value="handleTabChange"
        >
          <v-tab v-for="(item, i) in tabs" :key="i" :value="i">
            {{ item }}
          </v-tab>
        </v-tabs>
        
        <v-text-field
          v-if="tab !== 2"
          v-model="searchQuery"
          density="compact"
          variant="outlined"
          label="Search posts"
          prepend-inner-icon="mdi-magnify"
          clearable
          @click:clear="clearSearch"
          @keyup.enter="handleSearch"
          class="max-width-300 mt-2 mt-sm-0"
          hide-details
        ></v-text-field>
      </div>
      
      <!-- Create Post Component - Only shown when on the Create Post tab -->
      <CreatePost 
        v-if="tab === 2"
        @create-post="createPost"
        @update:title="handleUpdateTitle"
        @update:content="handleUpdateContent"
        @update:anonymous="handleUpdateAnonymous"
      />
      
    </v-card-text>
  </v-card>
</template>

<style scoped>
.max-width-300 {
  max-width: 300px;
}

@media (max-width: 600px) {
  .max-width-300 {
    max-width: 100%;
  }
}
</style>
