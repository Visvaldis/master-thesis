<template>
  <v-container
  
  style="height: 100%;"
     >
       <v-row
       style="height: 100%;"
       >
       <v-col class="d-flex justify-center align-center"  v-if="(walletId == null)" cols="12">
       <v-btn
       x-large
       rounded
       color="success"
       @click="(authDialog = true)">
         Connect
       </v-btn>
     </v-col>
         <v-col v-else cols="12">
          <v-col class="d-flex justify-end">
                <v-btn
          large
          rounded
          text
          @click="(walletId = null)"
          color="secondary">
            Log out
          </v-btn>
              </v-col>

         <profile-page
         :datastore="dataStore">
 
         </profile-page>
 
       </v-col>
 
       </v-row>
       <auth-dialog 
       :dialog="authDialog"
       @close="(authDialog = false)"
       @authFinished="onAuthFinished"
       >
 
       </auth-dialog>
     </v-container>
 </template>
 
 <script>
 import ProfilePage from './ProfilePage.vue';
 import AuthDialog from './AuthDialog.vue';
 
 export default {
   name: "MainPage",
 
   data: () => ({
     walletId: null,
     authDialog: false,
     edit: false,
     dataStore: null
   }),
   
   components:{
     ProfilePage,
     AuthDialog,
   },
   
   methods: {
     
     onAuthFinished(walletId,  dataStore){
        console.log("onAuthFinished",walletId, dataStore);
       this.walletId = walletId;
       this.dataStore = dataStore
     },
 
      
   },
   computed: {},
 };
 </script>
 <style scoped>
 
 </style>
 