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
      <v-container fluid class="main-container pa-8 rounded-lg">
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
                <UserTable :userData="users" />
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
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import UserTable from "@/views/dashboard/UserTable.vue";
import ChatBox from "@/components/ChatBox.vue";
import avatarImage from "@/assets/images/user.png";
import MessagesTable from "@/views/dashboard/MessagesTable.vue";

const users = ref([]);
const totalUsers = ref(0);
const totalAdmins = ref(0);
const activeTab = ref(localStorage.getItem("activeTab") || "dashboard");
const messages = ref([]);
const messageError = ref(null); // Variable to store error messages

const fetchUsers = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    users.value = response.data.data.users.map((user) => ({
      username: user.name,
      email: user.email,
      status: "active",
      is_superuser: user.is_superuser,
    }));
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

const fetchMessages = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/chat/api/messages/",
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      }
    );
    console.log("API Response:", response);
    messages.value = response?.data || []; // Adjusted to directly use the response data
    messageError.value = null; // Clear error if the fetch is successful
  } catch (err) {
    console.error("Error fetching messages:", err.message);
    messageError.value = "Failed to load messages."; // Set error message
  }
};

const fetchUserCounts = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/user-counts/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    totalUsers.value = response.data.total_users;
    totalAdmins.value = response.data.total_admins;
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
</script>

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
</style>
