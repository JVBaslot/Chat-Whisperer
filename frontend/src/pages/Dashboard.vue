// Changes to Dashboard.vue script section
<script setup>
import { ref, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import UserTable from "@/views/dashboard/UserTable.vue";
import ChatBox from "@/components/ChatBox.vue";
import avatarImage from "@/assets/images/user.png";
import MessagesTable from "@/views/dashboard/MessagesTable.vue";
import FreedomWall from "@/pages/FreedomWall.vue";
import Listings from "@/pages/Listings.vue"
import Footer from "@/components/Footer.vue"
import { 
  fetchUsers as apiFetchUsers, 
  fetchUserCounts as apiFetchUserCounts,
  fetchMessages as apiFetchMessages,
  createUser,
  updateUser,
  deleteUser as apiDeleteUser
} from "@/pages/functions/dashboard.js";

const users = ref([]);
const totalUsers = ref(0);
const totalAdmins = ref(0);
const activeTab = ref(localStorage.getItem("activeTab") || "dashboard");
const messages = ref([]);
const messageError = ref(null); // Variable to store error messages

// User CRUD operations
const userDialogOpen = ref(false);
const editingUser = ref(null);
const userFormData = ref({
  name: '',
  email: '',
  password: '',
  is_superuser: false,
  is_staff: false
});

const fetchUsers = async () => {
  try {
    users.value = await apiFetchUsers();
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

const fetchMessages = async () => {
  try {
    messages.value = await apiFetchMessages();
    messageError.value = null; // Clear error if the fetch is successful
  } catch (err) {
    console.error("Error fetching messages:", err.message);
    messageError.value = "Failed to load messages."; // Set error message
  }
};

const fetchUserCounts = async () => {
  try {
    const counts = await apiFetchUserCounts();
    totalUsers.value = counts.totalUsers;
    totalAdmins.value = counts.totalAdmins;
  } catch (err) {
    console.error("Error fetching user counts:", err.message);
  }
};

const logout = () => {
  const authStore = useAuthStore();
  authStore.logout();
};

onMounted(() => {
  fetchUsers();
  fetchMessages();
  fetchUserCounts();
});

watch(activeTab, (newTab) => {
  localStorage.setItem("activeTab", newTab);
});

const isActiveTab = (tab) => activeTab.value === tab;

const openAddUserDialog = () => {
  editingUser.value = null;
  userFormData.value = {
    name: '',
    email: '',
    password: '',
    is_superuser: false,
    is_staff: false
  };
  userDialogOpen.value = true;
};

const openEditUserDialog = (user) => {
  editingUser.value = user;
  userFormData.value = {
    name: user.name || user.username, // Just for display - won't be editable
    email: user.email, // Just for display - won't be editable
    is_superuser: user.is_superuser,
    is_staff: user.is_staff
  };
  userDialogOpen.value = true;
};

const saveUser = async () => {
  try {
    if (editingUser.value) {
      // Update existing user - only send the superuser and staff fields
      const updateData = {
        is_superuser: userFormData.value.is_superuser,
        is_staff: userFormData.value.is_staff
      };
      await updateUser(editingUser.value.id, updateData);
    } else {
      // Create new user - send all fields
      await createUser(userFormData.value);
    }
    userDialogOpen.value = false;
    await fetchUsers();
    await fetchUserCounts();
  } catch (err) {
    console.error("Error saving user:", err.message);
    alert("Error saving user: " + (err.response?.data?.detail || err.message));
  }
};

const deleteUser = async (userId) => {
  if (!confirm('Are you sure you want to delete this user?')) return;
  
  try {
    await apiDeleteUser(userId);
    await fetchUsers();
    await fetchUserCounts();
  } catch (err) {
    console.error("Error deleting user:", err.message);
    alert("Error deleting user: " + (err.response?.data?.detail || err.message));
  }
};
</script>


<template>
  <v-app class="app-container">
    <!-- Top Navigation Bar -->
    <v-app-bar app class="px-5">
      <v-toolbar-title class="text-h5 font-weight-black">GenAss</v-toolbar-title>

      <!-- Navigation Tabs -->
      <v-tabs v-model="activeTab" class="mx-5" color="#FE4F5A">
        <v-tab
          :class="{ 'active-tab': isActiveTab('dashboard') }"
          value="dashboard"
        >
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('dashboard') }"
          >
            mdi-view-dashboard
          </v-icon>
          <span :class="{ 'active-text': isActiveTab('dashboard') }">
            Dashboard
          </span>
        </v-tab>
        <v-tab :class="{ 'active-tab': isActiveTab('chats') }" value="chats">
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('chats') }"
          >
            mdi-chat
          </v-icon>
          <span :class="{ 'active-text': isActiveTab('chats') }">
            Send a Message
          </span>
        </v-tab>
        <v-tab :class="{ 'active-tab': isActiveTab('freedom-wall') }" value="freedom-wall">
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('freedom-wall') }"
          >
            mdi-message-text
          </v-icon>
          <span :class="{ 'active-text': isActiveTab('freedom-wall') }">
            Freedom Wall
          </span>
        </v-tab>
       <!--  <v-tab :class="{ 'active-tab': isActiveTab('listings') }" value="listings">
          <v-icon
            left
            class="me-1"
            :class="{ 'active-icon': isActiveTab('listings') }"
          >
            mdi-format-list-bulleted
          </v-icon>
          <span :class="{ 'active-text': isActiveTab('listings') }">
            Listings
          </span>
        </v-tab> -->
      </v-tabs>

      <v-spacer></v-spacer>

      <!-- Notification Icon with Badge -->
      <v-btn size="x-small" variant="tonal" icon class="mr-3">
        <v-badge color="#FE4F5A" dot>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>

      <!-- User Settings Menu -->
      <v-menu transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar :image="avatarImage"></v-avatar>
          </v-btn>
        </template>

        <v-sheet class="pa-0 mt-2 me-1 menu-card" color="#EEEEEE">
          <v-btn
            class="justify-start"
            rounded="0"
            variant="text"
            size="large"
            block
            @click="logout"
            style="text-transform: none"
          >
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                <v-icon class="me-3" left>mdi-logout</v-icon>
              </v-col>
              <v-col>Logout</v-col>
            </v-row>
          </v-btn>
        </v-sheet>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="custom-main">
      <v-container fluid class="main-container pa-8 rounded-lg" style="min-height: 80vh">
        <!-- Dashboard Tab -->
        <v-row justify="start" v-if="activeTab === 'dashboard'" class="mb-4">
          <v-col cols="2">
            <v-card class="bg-card">
              <v-container class="px-12 py-8">
                <h1>{{ totalUsers }}</h1>
                <h4 class="font-weight-regular">User</h4>
              </v-container>
            </v-card>

            <v-card class="bg-card my-5">
              <v-container class="px-12 py-8">
                <h1>{{ totalAdmins }}</h1>
                <h4 class="font-weight-regular">Admin</h4>
              </v-container>
            </v-card>
          </v-col>

          <v-col cols="10">
            <v-row justify="center">
              <v-col cols="12">
                <div class="d-flex align-center justify-space-between mb-4">
                  <h2 class="text-h5">Users</h2>
                  <v-btn 
                    color="#FE4F5A" 
                    prepend-icon="mdi-plus"
                    @click="openAddUserDialog"
                  >
                    Add User
                  </v-btn>
                </div>
                <UserTable 
                  :userData="users" 
                  @edit-user="openEditUserDialog" 
                  @delete-user="deleteUser"
                />
              </v-col>
              <v-col cols="12">
                <v-row v-if="messageError">
                  <!-- Error message row -->
                  <v-col cols="12">
                    <v-alert type="error" dismissible>
                      {{ messageError }}
                    </v-alert>
                  </v-col>
                </v-row>
                <v-row v-else>
                  <v-col cols="12">
                    <MessagesTable :messages="messages" />
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <!-- Chats Tab -->
        <v-row v-else-if="activeTab === 'chats'">
          <v-col cols="12">
            <ChatBox />
          </v-col>
        </v-row>

        <!-- Freedom Wall Tab -->
        <v-row v-else-if="activeTab === 'freedom-wall'">
          <v-col cols="12">
          
             <FreedomWall />
          
          </v-col>
        
        </v-row>

        <!-- Listings Tab -->
        <v-row v-else-if="activeTab === 'listings'">
          <v-col cols="12">
          <Listings/>
          </v-col>
        </v-row>

         
      </v-container>
       <Footer />
    </v-main>

    <!-- User Form Dialog -->
    <v-dialog v-model="userDialogOpen" max-width="500px">
      <v-card>
        <v-card-title class="bg-light-pink text-white">
          {{ editingUser ? 'Edit User' : 'Add New User' }}
        </v-card-title>
        <v-card-text class="pt-4">
          <v-form @submit.prevent="saveUser">
            <v-text-field
              v-model="userFormData.name"
              label="Name"
              required
              variant="outlined"
              class="mb-2"
              :disabled="!!editingUser"
            ></v-text-field>
            <v-text-field
              v-if="!editingUser"
              v-model="userFormData.email"
              label="Email"
              type="email"
              required
              variant="outlined"
              class="mb-2"
            ></v-text-field>
            <v-text-field
              v-else
              v-model="userFormData.email"
              label="Email"
              variant="outlined"
              class="mb-2"
              disabled
            ></v-text-field>
            <v-text-field
              v-if="!editingUser"
              v-model="userFormData.password"
              label="Password"
              type="password"
              required
              variant="outlined"
              class="mb-2"
            ></v-text-field>
            <v-switch
              v-model="userFormData.is_superuser"
              label="Admin User"
              color="#FE4F5A"
              hide-details
              class="mb-2"
            ></v-switch>
            <v-switch
              v-model="userFormData.is_staff"
              label="Staff User"
              color="#FE4F5A"
              hide-details
              class="mb-4"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="userDialogOpen = false" color="grey" variant="text">Cancel</v-btn>
          <v-btn @click="saveUser" color="red" class="text-white">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<style scoped>
.custom-main {
  padding-top: 64px;
}
.active-icon {
  color: #fe4f5a !important;
}
.active-text {
  color: #fe4f5a !important;
}
.bg-card {
  background: rgba(254, 79, 90, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(254, 79, 90, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #fe4f5a;
}
.bg-light-pink {
  background-color: #FE4F5A;
}
</style>
