<script setup>
import { defineProps } from "vue";
import avatarImage from "@/assets/images/user.png";

const props = defineProps({
  userData: {
    type: Array,
    required: true,
  },
});

const headers = [
  {
    title: "User",
    key: "username",
  },
  {
    title: "Email",
    key: "email",
  },
  {
    title: "Status",
    key: "status",
  },
  {
    title: "Admin",
    key: "is_superuser",
  },
  {
    title: "Staff",
    key: "is_staff",
  },
];

const resolveUserStatusVariant = (stat) => {
  const statLowerCase = stat.toLowerCase();
  if (statLowerCase === "pending") return "warning";
  if (statLowerCase === "active") return "success";
  if (statLowerCase === "inactive") return "secondary";

  return "primary";
};
</script>

<template>
  <v-card class="bg" elevation="10">
    <v-data-table
      :headers="headers"
      :items="userData"
      item-value="id"
      class="text-no-wrap bg"
    >
      <!-- User -->
      <template #item.username="{ item }">
        <div class="d-flex align-center" style="gap: 15px">
          <v-avatar size="34">
            <v-img :src="avatarImage" />
          </v-avatar>

          <div class="d-flex flex-column">
            <h6 class="text-h6 font-weight-medium user-list-name">
              {{ item.username }}
            </h6>
          </div>
        </div>
      </template>
      <!-- Status -->
      <template #item.status="{ item }">
        <v-chip
          :color="resolveUserStatusVariant(item.status)"
          size="small"
          class="text-capitalize"
        >
          {{ item.status }}
        </v-chip>
      </template>

      <!-- Admin -->
      <template #item.is_superuser="{ item }">
        <v-chip
          :color="item.is_superuser ? 'success' : 'error'"
          size="small"
          class="text-capitalize"
        >
          {{ item.is_superuser ? "True" : "False" }}
        </v-chip>
      </template>

      <!-- Staff -->
      <template #item.is_staff="{ item }">
        <v-chip
          :color="item.is_staff ? 'success' : 'error'"
          size="small"
          class="text-capitalize"
        >
          {{ item.is_staff ? "True" : "False" }}
        </v-chip>
      </template>

      <template #bottom />
    </v-data-table>
  </v-card>
</template>

<style scoped>
.bg {
  /* Adjusted to use #FE4F5A as the base color */
  background: rgba(254, 79, 90, 0.15); /* Lightened version of the base color */
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(254, 79, 90, 0.3); /* Softer shadow using base color */
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #FE4F5A; /* Keeping the base color for the border */
}

</style>
