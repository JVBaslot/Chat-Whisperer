<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const listings = ref([]);
const loading = ref(false);
const error = ref(null);
const dialog = ref(false);

// Form data for new listing
const newListing = ref({
  title: '',
  description: '',
  price: '',
  category: '',
  contact: ''
});

// Available categories
const categories = [
  'Electronics',
  'Books',
  'Clothing',
  'Furniture',
  'Services',
  'Other'
];

// Fetch all listings
const fetchListings = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Replace with your actual API endpoint
    const response = await axios.get('http://127.0.0.1:8000/api/listings/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    listings.value = response.data.data || [];
  } catch (err) {
    console.error('Error fetching listings:', err.message);
    error.value = 'Failed to load listings. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// Submit a new listing
const submitListing = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Replace with your actual API endpoint
    await axios.post(
      'http://127.0.0.1:8000/api/listings/',
      newListing.value,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
    );
    // Reset form and close dialog
    newListing.value = {
      title: '',
      description: '',
      price: '',
      category: '',
      contact: ''
    };
    dialog.value = false;
    fetchListings(); // Refresh the listings
  } catch (err) {
    console.error('Error submitting listing:', err.message);
    error.value = 'Failed to submit your listing. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchListings();
});
</script>

<template>
  <div class="listings">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2 class="text-h4 font-weight-bold">Listings</h2>
      <v-btn color="#FE4F5A" @click="dialog = true">
        <v-icon left>mdi-plus</v-icon>
        Post New Listing
      </v-btn>
    </div>
    
    <!-- Error Alert -->
    <v-alert v-if="error" type="error" dismissible class="mb-4">
      {{ error }}
    </v-alert>
    
    <!-- Categories Filter -->
    <div class="category-filters mb-4">
      <v-chip-group>
        <v-chip
          filter
          variant="outlined"
          value="all"
        >
          All
        </v-chip>
        <v-chip
          v-for="category in categories"
          :key="category"
          filter
          variant="outlined"
          :value="category"
        >
          {{ category }}
        </v-chip>
      </v-chip-group>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading && !listings.length" class="text-center my-6">
      <v-progress-circular indeterminate color="#FE4F5A"></v-progress-circular>
      <p class="mt-2">Loading listings...</p>
    </div>
    
    <!-- Listings Grid -->
    <v-row v-if="listings.length">
      <v-col
        v-for="(listing, index) in listings"
        :key="index"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="listing-card h-100">
          <v-card-title>{{ listing.title }}</v-card-title>
          <v-chip class="ma-2" color="primary" size="small" label>
            {{ listing.category }}
          </v-chip>
          <v-card-text>
            <p class="text-h6 font-weight-bold primary--text">${{ listing.price }}</p>
            <p>{{ listing.description }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="text" color="#FE4F5A">
              <v-icon left>mdi-phone</v-icon>
              Contact
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn icon>
              <v-icon>mdi-share-variant</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Empty State -->
    <v-card v-else-if="!loading" class="pa-4 text-center">
      <v-card-text>
        <v-icon x-large color="grey lighten-1">mdi-storefront</v-icon>
        <p class="text-h6 mt-2">No listings available</p>
        <p class="text-body-1">Be the first to post a listing!</p>
      </v-card-text>
    </v-card>
    
    <!-- New Listing Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">New Listing</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="newListing.title"
                  label="Title*"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="newListing.description"
                  label="Description*"
                  required
                ></v-textarea>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="newListing.price"
                  label="Price*"
                  prefix="$"
                  type="number"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="newListing.category"
                  :items="categories"
                  label="Category*"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="newListing.contact"
                  label="Contact Information*"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" text @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="#FE4F5A"
            @click="submitListing"
            :loading="loading"
            :disabled="!newListing.title || !newListing.description || !newListing.price"
          >
            Post
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.listings {
  width: 100%;
}

.listing-card {
  transition: transform 0.2s;
  height: 100%;
}

.listing-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.category-filters {
  overflow-x: auto;
}
</style>
