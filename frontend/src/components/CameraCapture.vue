<!-- eslint-disable no-unused-vars -->
<template>
  <div>
    <v-row >
      <v-col cols="12">
        <div v-if="timeShow && countDown > 0">Please wait for {{ countDown }} seconds</div>
        <div v-else>Success!</div>
        <strong >{{result}}</strong>
      </v-col>
      <v-col cols="6">
        <v-card class="camera-box" :loading="isLoading">
          <div>
            <video ref="camera" class="camera" autoplay></video>
          </div>
        </v-card>
      </v-col>

      <v-col cols="6">
            <canvas v-show="false" id="photoTaken" ref="canvas" class="camera" width="640" height="480" > </canvas>
      </v-col>
      

      <v-col cols="5">
        <v-text-field
        label="User Name"
        :rules="rules"
        hide-details="auto"
        class="mb-3"
        v-model="userName"

    ></v-text-field>
    
        <v-btn :loading="isLoading" :disabled="!userName" block color="success" @click="recordSeries()">
          <v-icon>mdi-camera</v-icon>
        </v-btn>
        <v-btn :loading="isLoading" :disabled="!userName" block color="primary" @click="login()">
          <v-icon>mdi-login</v-icon>
        </v-btn>
        
        <span v-if="countDown == 0">Sent!</span>
       
      </v-col>
      <v-col cols="12">
        <ul>
          <li v-for="(src, i) in captures" :key="i">
            <img :src="src" style="height: 80px" />
          </li>
        </ul>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CameraCapture",

  data: () => ({
    isLoading: false,
    captures: [],
    timeShow: false,
    countDown: 15,
    rules: [
        value => !!value || 'Required.',
      ],
    userName: "",
    result: ""
  }),

  mounted() {
    this.isLoading = true;

    const constraints = (window.constraints = {
      audio: false,
      video: true,
    });

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then((stream) => {
        this.isLoading = false;
        this.$refs.camera.srcObject = stream;
      })
      .catch((error) => {
        this.isLoading = false;
        alert("May the browser didn't support or there is some errors.", error);
      });
  },

  unmounted() {},
  methods: {
     
    async sendToApi(){
      console.log(this.captures.length);
      let path = `http://localhost:5000/load_faces`;
        let data = {
            images: this.captures,
            name: this.userName
          };
        console.log(data);
        await axios.post(path, data);
    },

    async recordSeries(){
      this.timeShow = true;
      this.captures = [];
      this.countDown = 15;
      for (this.countDown; this.countDown > 0; this.countDown--){
        let url = await this.makePhotoWithInterval();
        this.captures.push(url);
      }
      await this.sendToApi();
    },

    makePhotoWithInterval(){
      // eslint-disable-next-line no-unused-vars
      return new Promise((resolve, _) => setTimeout(() => { 
                  resolve(this.getCaptureUrl());
      }, 200));

    },

    getCaptureUrl(){
      this.$refs.canvas
                  .getContext("2d")
                  .drawImage(this.$refs.camera, 0, 0, 640, 480);
                  return this.$refs.canvas.toDataURL("image/png");
    },
    
    async login(){
      this.result = ""
      let path = `http://localhost:5000/find_face`;
        let image = this.getCaptureUrl();
        let data = {
            image: image,
            name: this.userName
          };
        console.log(data);
        await axios.post(path, data).then((response) => {

          this.result = JSON.stringify(response.data);
          console.log(this.result);
        }).catch((error) => {
           console.log(error);
        });
    }

  
  },
};
</script>

<style scoped>
.camera {
  width: 100%;
  height: 100%;
}

ul {
  list-style-type:none;
}
ul > li {
    display: inline-block;
    /* You can also add some margins here to make it look prettier */
}

.camera-box {
  width: 400px;
  height: 300px;
}
</style>
