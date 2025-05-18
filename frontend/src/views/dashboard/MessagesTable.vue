<script setup>
import { defineProps } from "vue";

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  currentUserId: {
    type: Number,
    required: true,
  },
});

const resolveMessageVariant = (senderId, currentUserId) => {
  return senderId === currentUserId ? "success" : "secondary";
};
</script>

<template>
  <v-card class="bg" elevation="10">
    <v-data-table
      :headers="[
        { title: 'Message', key: 'content' },
        { title: 'Timestamp', key: 'timestamp' },
        { title: 'Sender', key: 'sender_id' },
        { title: 'Receiver', key: 'receiver_id' }
      ]"
      :items="messages"
      item-value="id"
      class="text-no-wrap bg"
    >
      <!-- Message Content -->
      <template #item.content="{ item }">
        <div class="d-flex align-center">
            <v-chip :color="resolveMessageVariant(item.sender, currentUserId)" size="small">
            <p>Content Encrypted Please Use Decrypt System <a href="http://localhost:3050/" target="_blank">http://localhost:3050/</a>😌</p>
            </v-chip>
        </div>
      </template>

      <!-- Timestamp -->
      <template #item.timestamp="{ item }">
        <div class="text-caption">
          {{ new Date(item.timestamp).toLocaleString() }}
        </div>
      </template>

      <!-- Sender -->
      <template #item.sender_id="{ item }">
        <div class="text-body-2">
          {{ item.sender }}
        </div>
      </template>

      <!-- Receiver -->
      <template #item.receiver_id="{ item }">
        <div class="text-body-2">
          {{ item.receiver }}
        </div>
      </template>

      <template #bottom />
    </v-data-table>
  </v-card>
</template>

<style scoped>
.bg {
  background: rgba(254, 79, 90, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(254, 79, 90, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #FE4F5A;
}
</style>
