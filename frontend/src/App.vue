<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">

        <v-avatar class="mx-3" size="60">
          <v-img src="https://cdn.midjourney.com/fb5be040-a9f2-4f96-860c-a9d33ebdd243/grid_0.png" contain alt="Logo" />
        </v-avatar>
        <v-toolbar-title>Face recognition</v-toolbar-title>
      </div>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <MainPage />
    </v-main>

    <v-footer app padless color="primary">
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script setup>
import MainPage from '@/components/MainPage.vue'
</script>
