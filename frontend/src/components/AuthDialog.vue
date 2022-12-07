<!-- eslint-disable vue/no-mutating-props -->
<template>
  <v-dialog
    v-model="dialog"
    eager
    persistent
    max-width="500px"
  >
    <v-card :loading="loading">
      <v-toolbar flat>
        <v-spacer></v-spacer>
        <v-toolbar-title>Login</v-toolbar-title>

        <v-spacer></v-spacer>
        <v-btn
          class="me-1"
          icon
          small
          light
          @click="onClose()"
        >
          <v-icon color="grey darken-2"> mdi-close </v-icon>
        </v-btn>
      </v-toolbar>
      <div v-if="step == 1">
        <blockcain-auth-card 
            @onConnect="walletConnected">
        </blockcain-auth-card>
      </div>

      <div v-if="step == 2">
        <face-recognition 
            @faceRecognized="onFaceRecognized"
            :walletId="walletId"> 
        </face-recognition>
        <v-snackbar
            top
            right
            text
            :color="snackColor"
            v-model="snackbarShow"
            >
                {{ snackbarText }}
        
                <template v-slot:action="{ attrs }">
                <v-btn class="me-1"  icon small light v-bind="attrs" @click="snackbarShow = false"
                >
                    <v-icon  color="grey darken-2" >
                    mdi-close
                    </v-icon>
                </v-btn>
                </template>
            </v-snackbar>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
import FaceRecognitionStatuses from "@/constants/FaceRecognitionStatuses";
import BlockcainAuthCard from "./BlockcainAuthCard.vue";
import FaceRecognition from "./FaceRecognition.vue";

export default {
  name: "AuthDialog",
  components: { BlockcainAuthCard, FaceRecognition },

  data: () => ({
    step: 1,
    walletId: null,
    loading: false,
    snackbarShow: false,
    snackColor: "primary",
    snackbarText: "",
    dataStore: null
  }),

  props: {
    dialog: Boolean,
  },

  mounted() {},

  methods: {
    onClose() {
      this.step = 1;
      this.$emit("close");
    },

    walletConnected(walletId, dataStore) {
      console.log("walletId", walletId);
      this.walletId = walletId;
      this.dataStore = dataStore;
      this.step++;
    },

    onFaceRecognized(recognitionStatus){
        [this.snackbarText, this.snackColor] = this.getSnackbarText(recognitionStatus)
        this.snackbarShow = true;
        if (recognitionStatus == FaceRecognitionStatuses.Valid){
            this.onClose();
            this.$emit("authFinished", this.walletId, this.dataStore);
        }
    },

    getSnackbarText(recognitionStatus){
        console.log("getSnackbarText",recognitionStatus, FaceRecognitionStatuses.Valid, recognitionStatus == FaceRecognitionStatuses.Valid);
        switch(recognitionStatus) {
        case FaceRecognitionStatuses.Valid:
            if(this.profile && this.profile.name)
                return [`Welcome back, ${this.profile.name}!`, "success"];
            else 
                return [`Welcome back!`, "success"];
        case FaceRecognitionStatuses.Invalid:
          return ["You are not the right person, please try again!", "error"];
        case FaceRecognitionStatuses.FaceNotFound:
          return ["Face was not found, please take another photo.", "warning"];
        default:
          return ["Some error happens, please try again.", "info"];
        }
    }
  },

};
</script>

<style></style>
