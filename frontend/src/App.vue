<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">

        <v-avatar class="mx-3" size="60">
          <v-img src="@/assets/logo.svg" class="filter-green" contain alt="Logo" />
        </v-avatar>
        <v-toolbar-title>Blockchain account management</v-toolbar-title>
      </div>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <MainPage />
    </v-main>

    <v-footer app padless color="primary">
      <v-col class="text-center white--text" cols="12">
        {{ new Date().getFullYear() }} — <strong>Vsevolod Slavinskyi</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script setup>
import MainPage from '@/components/MainPage.vue'
</script>

<style scoped>
   .filter-green{
    filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(93deg) brightness(103%) contrast(103%);
    border-radius: 0px;
    }
</style>
