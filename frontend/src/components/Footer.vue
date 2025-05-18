<template>
  <v-footer class="bg-background">
    <v-container fluid>
      <v-row>
        <!-- Company Info and Description -->
        <v-col cols="12" sm="4" class="mb-4">
          <h2 class="text-h6 font-weight-bold mb-3">GenAss</h2>
          <p class="text-body-2 mb-4">
            Secure messaging platform with end-to-end encryption for students.
            Keep your conversations private and protected.
          </p>
          <div class="d-flex">
            <v-btn
              v-for="icon in socialIcons"
              :key="icon.name"
              :aria-label="icon.name"
              variant="text"
              color="primary"
              icon
              class="me-2"
            >
              <v-icon>{{ icon.icon }}</v-icon>
            </v-btn>
          </div>
        </v-col>

        <!-- Quick Links -->
        <v-col cols="12" sm="2" class="mb-4">
          <h3 class="text-subtitle-1 font-weight-bold mb-3">Quick Links</h3>
          <v-list density="compact" bg-color="transparent" class="pa-0">
            <v-list-item
              v-for="link in quickLinks"
              :key="link.title"
              :to="link.to"
              density="compact"
              class="px-0"
              color="primary"
            >
              <template v-slot:prepend>
                <v-icon size="small" color="primary">{{ link.icon }}</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ link.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Support -->
        <v-col cols="12" sm="2" class="mb-4">
          <h3 class="text-subtitle-1 font-weight-bold mb-3">Support</h3>
          <v-list density="compact" bg-color="transparent" class="pa-0">
            <v-list-item
              v-for="link in supportLinks"
              :key="link.title"
              :to="link.to"
              density="compact"
              class="px-0"
              color="primary"
            >
              <template v-slot:prepend>
                <v-icon size="small" color="primary">{{ link.icon }}</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ link.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Contact Info -->
        <v-col cols="12" sm="4" class="mb-4">
          <h3 class="text-subtitle-1 font-weight-bold mb-3">Contact Us</h3>
          <div class="d-flex mb-3">
            <v-icon color="primary" class="me-3">mdi-map-marker</v-icon>
            <span class="text-body-2">University Campus, Student Center, Room 101</span>
          </div>
          <div class="d-flex mb-3">
            <v-icon color="primary" class="me-3">mdi-phone</v-icon>
            <span class="text-body-2">+1 (555) 123-4567</span>
          </div>
          <div class="d-flex mb-3">
            <v-icon color="primary" class="me-3">mdi-email</v-icon>
            <span class="text-body-2">support@GenASs.edu</span>
          </div>
        </v-col>
      </v-row>

      <!-- Copyright Section -->
      <v-divider class="mb-4"></v-divider>
      <div class="d-flex flex-column flex-sm-row justify-space-between align-center py-2">
        <div class="text-body-2 text-center text-sm-left mb-3 mb-sm-0">
          &copy; {{ new Date().getFullYear() }} GenAss. All rights reserved.
        </div>
        <div>
          <v-btn
            v-for="link in legalLinks"
            :key="link.title"
            :to="link.to"
            variant="text"
            density="compact"
            class="text-body-2"
            color="primary"
          >
            {{ link.title }}
          </v-btn>
        </div>
      </div>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      socialIcons: [
        { name: 'Facebook', icon: 'mdi-facebook' },
        { name: 'Twitter', icon: 'mdi-twitter' },
        { name: 'Instagram', icon: 'mdi-instagram' },
        { name: 'LinkedIn', icon: 'mdi-linkedin' }
      ],
      quickLinks: [
        { title: 'Home', to: '/', icon: 'mdi-home' },
        { title: 'Dashboard', to: '/dashboard', icon: 'mdi-view-dashboard' },
        { title: 'Messages', to: '/messages', icon: 'mdi-message' },
        { title: 'Freedom Wall', to: '/freedom-wall', icon: 'mdi-message-text' }
      ],
      supportLinks: [
        { title: 'FAQ', to: '/faq', icon: 'mdi-frequently-asked-questions' },
        { title: 'Help Center', to: '/help', icon: 'mdi-help-circle' },
        { title: 'Report Issue', to: '/report', icon: 'mdi-alert-circle' },
        { title: 'Feedback', to: '/feedback', icon: 'mdi-comment-text' }
      ],
      legalLinks: [
        { title: 'Privacy Policy', to: '/privacy' },
        { title: 'Terms of Service', to: '/terms' },
        { title: 'Cookie Policy', to: '/cookies' }
      ]
    };
  }
};
</script>

<style scoped>
.v-footer {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.v-list-item--density-compact {
  min-height: 32px;
}

.v-btn.v-btn--density-default.v-btn--variant-text {
  text-transform: none;
}

/* Primary color styling matching your app's theme */
:deep(.v-btn.v-btn--variant-text.text-primary),
:deep(.v-icon.text-primary),
:deep(.v-list-item.text-primary) {
  color: #FE4F5A !important;
}

.primary {
  color: #FE4F5A !important;
}
</style>