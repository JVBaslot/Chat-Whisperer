<template>
  <v-container fluid>
    <br />
    <br />
    <br />
    <v-row justify="center" align="center">
      <v-col cols="4">
        <login-form class="px-10">
          <template #footer>
            <v-card-text class="text-center mt-3 mb-5">
              <span class="text-center font-weight-light">
                Don't have an account?
              </span>
              <span
                class="text-teal-lighten-2 text-decoration-none cursor-pointer"
                @click="switchToRegister"
              >
                Register
              </span>
            </v-card-text>
          </template>
        </login-form>
      </v-col>
      <v-col cols="1">

      </v-col>
      <v-col cols="5">
        <img src="@/assets/images/1.png" alt="" width="500" />
      </v-col>
    </v-row>
  </v-container>

  <v-dialog v-model="showRegister" persistent>
    <v-row justify="center" align="center">
      <v-col cols="10" lg="4" md="6" sm="6">
        <register-form v-model="showRegister" class="px-10">
          <template #footer>
            <!-- Optional footer content for the register form -->
          </template>
        </register-form>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script setup>
import { ref } from "vue";
import LoginForm from "@/layouts/LoginForm.vue";
import RegisterForm from "@/layouts/RegisterForm.vue";

const showRegister = ref(false);

const switchToRegister = () => (showRegister.value = true);
</script>

<style scoped>
.bg {
  position: absolute;
  height: 100vh;
  width: auto;
  overflow: hidden;
}

:deep(.v-overlay__scrim) {
  background-color: #4db6ac !important; /* Change to your desired color */
}
</style>
