<script>
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const email = ref("");
    const password = ref("");
    const isPasswordVisible = ref(false);

    const handleLogin = async () => {
      const success = await authStore.login(email.value, password.value);
      if (!success) {
        alert("Login failed");
      } else {
        alert("Login successful");
        const redirect =
          router.currentRoute.value.query.redirect || "/dashboard";
        router.push(redirect);
      }
    };

    return { email, password, isPasswordVisible, handleLogin };
  },
};
</script>



<template>
  <v-card class="bg-card" elevation="8">
    <h1 class="text-center pt-5 pb-2">Student</h1>

    <div class="mb-8 mt-2">
      <h4 class="text-h6 mb-1">Welcome Student! 👋🏻</h4>
      <p class="mb-0">Please sign-in to your account to get started</p>
    </div>

    <v-form ref="form" @submit.prevent="handleLogin">
      <v-text-field
        v-model="email"
        color="#FE4F5A"
        placeholder="example@gmail.com"
        label="Email"
        variant="outlined"
        type="email"
        required
      />
      <v-text-field
        v-model="password"
        color="#FE4F5A"
        placeholder="············"
        label="Password"
        variant="outlined"
        :type="isPasswordVisible ? 'text' : 'password'"
        :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="isPasswordVisible = !isPasswordVisible"
        required
      />

      <!-- remember me checkbox -->
      <div class="d-flex align-center justify-space-between flex-wrap mb-3">
        <v-checkbox
          class="d-flex align-center"
          color="#FE4F5A"
          label="Remember me"
        />
        <a class="red" href="javascript:void(0)">
          Forgot Password?
        </a>
      </div>

      <v-btn
        type="submit"
        color="#FE4F5A"
        class="mt-1 rounded"
        size="large"
        block
        >Login</v-btn
      >
    </v-form>
    <slot name="footer" />
  </v-card>
</template>



<style scoped>
.red{
  color: #FE4F5A ;
}
</style>
