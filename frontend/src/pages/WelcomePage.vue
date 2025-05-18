<!-- WelcomePage.vue -->
<template>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="6" class="text-center">
          <v-card class="pa-6" elevation="2">
            <v-card-title class="headline">Welcome to Our App!</v-card-title>
            <v-card-subtitle class="mb-4">Please log in to continue.</v-card-subtitle>
            
            <v-btn to="/login" color="primary" class="mt-4" large>
              Go to Login
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: "WelcomePage",
  };
  </script>
  
  <style scoped>
  .headline {
    font-size: 2em;
    font-weight: bold;
  }
  </style>
  