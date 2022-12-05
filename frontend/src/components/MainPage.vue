<template>
 <v-container
 fluid
 style="height: 100%;"
    >
      <v-row
      style="height: 100%;"
      >
      <v-btn @click="tt()">
        lol
      </v-btn>
        <v-col cols="12">
          <blockcain-auth  v-if="trigger" :walletId.sync="walletId">

          </blockcain-auth>
         <camera-capture v-if="!trigger">

         </camera-capture>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

import CameraCapture from './CameraCapture.vue';
import BlockcainAuth from './BlockcainAuth.vue';

export default {
  name: "MainPage",

  data: () => ({
      smart: false,
    loading: false,
    ifResult: false,
    result: {},
    title: "",
    trigger: true, 
    walletId: ""
  }),
  
  components:{
    CameraCapture,
    BlockcainAuth
  },
  
  methods: {
    photoUploaded(file) {
      console.log(file);
      this.predictedCategory = '';
      if (file) {
        this.photoUrl = URL.createObjectURL(file);
      }
    },
    tt(){
      console.log(this.walletId);
    },

      get(){
      let path = `http://localhost:5000/get/4`;
     
      this.loading = true; 
      axios.get(path)
        .then((response) => {
          this.loading = false; 
          this.ifResult = true;
          this.title = "GET"
          this.result = JSON.stringify(response.data);
          console.log(this.result);
        }).catch((error) => {
           this.ifResult = false;
           console.log(error);
        });

     
    },
    post(){
      let path = `http://localhost:5000/post`;

      this.loading = true; 
      let data = {
        title: "test",
        text: "test test"
      }
      axios.post(path, data)
        .then((response) => {
          this.loading = false; 
          this.ifResult = true;
          this.title = "POST"
          this.result = JSON.stringify(response.data);
          console.log(this.result);
        }).catch((error) => {
           this.ifResult = false;
           console.log(error);
        });

     
    }

  },
  computed: {},
};
</script>
<style scoped>

</style>
