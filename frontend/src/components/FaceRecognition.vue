<template>
    <v-card height="580" :loading="cameraLoad">
        <v-card class="camera-box">
            <div>
                <video ref="camera" class="camera" autoplay></video>
            </div>
            <v-overlay
          absolute
          opacity="0.55"
          :value="overlay"
        >
        <div class="d-flex flex-column justify-center align-center" v-if="(countDown > 0)" >

          <div class="text-center text-h6" style="margin-bottom: 180px"> Please stay still while we collecting <br> and processing your biometry information</div>
          <span class="text-h1 font-weight-thin" style="color:rgba(255, 255, 255, 0.5)">{{countDown}}</span>
        </div>
        <v-progress-circular
        v-else
        indeterminate
        size="64"
      ></v-progress-circular>
        </v-overlay>
        </v-card>
        <canvas v-show="false" id="photoTaken" ref="canvas" class="camera" width="640" height="480" > </canvas>
  
    <div class="d-flex flex-column justify-center align-center"  v-if="shouldRegister">
        <v-alert
            color="warning"
            outlined
            class="mt-4 mx-3"
            type="info"
            >
            Seems you not register two-factor authentification. <br>

            Please be sure that you are the only person in the camera and press <strong>Register</strong> button
        </v-alert>
        <v-btn
          @click="register()"
          x-large
          outlined
          :loading="overlay"
          color="success"
          class="mb-3"
          rounded 
          >
            Register
        </v-btn>

    </div>

    <div class="d-flex flex-column justify-center align-center"  v-else>
      <v-alert
            outlined
            class="mt-4 mx-3"
            type="info"
            >
            Please be sure that you are the only person in the camera and press <strong>Login</strong> button
        </v-alert>
      <v-btn
          @click="login()"
          x-large
          outlined
          :loading="loginLoading"
          color="success"
          rounded 
          >
          Login
        </v-btn>
    </div>
    </v-card>
</template>

<script>
import axios from 'axios';

export default {
    name: "FaceRecognition",
    data: () => ({
        shouldRegister: false,
        overlay: false,
        loginLoading: false,
        countDown: 15,
        captures: [],
        cameraLoad: false

    }),

    props: {
        walletId: String,
    },

    async mounted() {
      this.cameraLoad = true; 
       await this.checkTFARegistration();
       this.setupCamera();
       this.cameraLoad = false;
    },

    methods:{

    setupCamera(){
        const constraints = (window.constraints = {
          audio: false,
          video: true,
        });

        navigator.mediaDevices
          .getUserMedia(constraints)
          .then((stream) => {
            this.$refs.camera.srcObject = stream;
          })
          .catch((error) => {
            alert("May the browser didn't support or there is some errors.", error);
          });
    },

    async checkTFARegistration(){
        let path = `http://localhost:5000/check/${this.walletId}`;
        
        await axios.get(path)
        .then((response) => {
            this.shouldRegister = !response.data.data;
            console.log(this.shouldRegister);
        }).catch((error) => {
            console.log(error);
        });
    },
    
    async register(){
      try{
        this.overlay = true;
        await this.recordSeries();
        await this.checkTFARegistration();
        this.overlay = false;
      }
      catch(error) {
        console.log(error);
        this.overlay = false;
      }
    },


    async recordSeries(){
      this.captures = [];
      this.countDown = 15;
      for (this.countDown; this.countDown > 0; this.countDown--){
        let url = await this.makePhotoWithInterval();
        this.captures.push(url);
      }
      await this.sendBiometryInformation();
    },

    makePhotoWithInterval(){
      return new Promise((resolve) => setTimeout(() => { 
                  resolve(this.getCaptureUrl());
      }, 200));

    },

    getCaptureUrl(){
      this.$refs.canvas
                  .getContext("2d")
                  .drawImage(this.$refs.camera, 0, 0, 640, 480);
                  return this.$refs.canvas.toDataURL("image/png");
    },

    async sendBiometryInformation(){
      console.log(this.captures.length);
      let path = `http://localhost:5000/load_faces`;
        let data = {
            images: this.captures,
            name: this.walletId
          };
        console.log(data);
        await axios.post(path, data);
    },

    async login(){
      console.log("this.walletId", this.walletId);
      let path = `http://localhost:5000/find_face`;
        let image = this.getCaptureUrl();
        let data = {
            image: image,
            name: this.walletId
          };
        await axios.post(path, data).then((response) => {
          console.log(response.data);
          let recognitionStatus = response.data.data;
          this.$emit("faceRecognized", recognitionStatus)
          console.log(recognitionStatus);
        }).catch((error) => {
           console.log(error);
        });
    }

    },
   
};


</script>

<style>

.camera {
  width: 100%;
  height: 100%;
}


.camera-box {
  width: 500px;
  height: 375px;
}
</style>