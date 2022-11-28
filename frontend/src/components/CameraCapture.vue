<template>
  <div>
    <v-row class="camera-box">
        <v-col cols="12" v-if="timeShow">
            <div v-if="countDown > 0">
                Please wait for {{countDown}} seconds
            </div>
            <div v-else>
                Success!
            </div>
        </v-col>
      <v-col cols="6">
        <v-card :loading="isLoading">
          <div v-if="isCameraOpen">
            <video
              v-show="!isPhotoTaken"
              ref="camera"
              class="camera"
              autoplay
            ></video>

          </div>
        </v-card>
      </v-col>

      <v-col cols="6">
        <v-card :loading="isLoading">
          <div>
            <canvas
             id="photoTaken"
             ref="canvas" 
             class="camera">
            </canvas>

          </div>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-btn :loading="isLoading" block color="success" @click="recordVideo">
          <v-icon>mdi-camera</v-icon>
        </v-btn>
      </v-col>
      <v-col cols="12">
        <ul>
          <li v-for="c,i in captures" :key="i">
              <img src="{{ c }}" height="50" />
          </li>
        </ul>
      </v-col>
    </v-row>

    <div v-if="isCameraOpen && !isLoading" class="camera-shoot">
      <button type="button" class="button" @click="takePhoto">
        <img
          src="https://img.icons8.com/material-outlined/50/000000/camera--v2.png"
        />
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "CameraCapture",

  data: () => ({
    isCameraOpen: true,
    isPhotoTaken: false,
    isShotPhoto: false,
    isLoading: false,
    link: "#",
    countDown: 5,
    timeShow: false,
    camera_stream: null,
    media_recorder: null,
    blobs_recorded : [], 
    downloadLink: "",
    captures: []
  }),

  mounted() {
    this.createCameraElement();
  },

  unmounted() {
    this.stopCameraStream();
  },
  methods: {
    toggleCamera() {
      if (this.isCameraOpen) {
        this.isCameraOpen = false;
        this.isPhotoTaken = false;
        this.isShotPhoto = false;
        this.stopCameraStream();
      } else {
        this.isCameraOpen = true;
        this.createCameraElement();
      }
    },

    async createCameraElement() {
      this.isLoading = true;

      const constraints = (window.constraints = {
        audio: false,
        video: true,
      });

      this.camera_stream = await navigator.mediaDevices
        .getUserMedia(constraints);
        this.isLoading = false;
        this.$refs.camera.srcObject = this.camera_stream;
    },

    stopCameraStream() {
      let tracks = this.$refs.camera.srcObject.getTracks();

      tracks.forEach((track) => {
        track.stop();
      });
    },

    takePhoto() {
      if (!this.isPhotoTaken) {
        this.isShotPhoto = true;

        const FLASH_TIMEOUT = 50;

        setTimeout(() => {
          this.isShotPhoto = false;
        }, FLASH_TIMEOUT);
      }

      this.isPhotoTaken = !this.isPhotoTaken;

      const context = this.$refs.canvas.getContext("2d");
      context.drawImage(this.$refs.camera, 0, 0, 450, 337.5);
    },

    async recordVideo(){
        this.timeShow = true;
        this.countDown = 5;
        this.record();
    },

    record(){
        for (let i = 0; i < this.countDown; i++) {
            const context = this.$refs.canvas.getContext("2d");
            context.drawImage(this.$refs.camera, 0, 0, 400, 400);
            var dataURL = this.$refs.canvas.toDataURL();
            this.sendPhotosToApi(dataURL);
            this.wait();
        }
    },

    async sendPhotosToApi(url) {
        try {

        let data = {
            'image': url
        }
      await axios.post("post/", data);
    } catch (error) {
                console.log(error)
            }


    },
    wait() {
        if (this.countDown > 0) {
            setTimeout(() => {
                this.countDownTimer()
            }, 1000)
        }
    },
  },
};
</script>

<style scoped>
.camera {
  width: 100%;
  height: 100%;
}

.camera-box {
  width: 400px;
  height: 400px;
}
</style>
