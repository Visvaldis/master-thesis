<template>
  <v-card
  class="d-flex flex-column justify-center align-center pb-5"
  flat
  height="250">
    <v-img class="ml-n5" width="500" contain src="@/assets/auth_process.png"></v-img>

    <v-btn
      x-large
      :outlined="!blockchainProfile"
      :loading="loading"
      color="success"
      class="mb-3"
      rounded
      @click="connect()"
    >
      {{ btnText }}
      <v-icon
        v-if="blockchainProfile"
        right
      >
        mdi-check
      </v-icon>
    </v-btn>
    
  </v-card>
</template>

<script>
import { CeramicClient } from "@ceramicnetwork/http-client";
import { EthereumAuthProvider } from "@ceramicnetwork/blockchain-utils-linking";
import { DIDDataStore } from "@glazed/did-datastore";
import { DIDSession } from "@glazed/did-session";

export default {
  name: "BlockcainAuthCard",

  data: () => ({
    loading: false,
    ceramic: new CeramicClient("https://ceramic-clay.3boxlabs.com"),
    blockchainProfile: null,
    aliases: {
      schemas: {
        basicProfile:
          "ceramic://k3y52l7qbv1frxt706gqfzmq6cbqdkptzk8uudaryhlkf6ly9vx21hqu4r6k1jqio",
      },
      definitions: {
        BasicProfile:
          "kjzl6cwe1jw145cjbeko9kil8g9bxszjhyde21ob8epxuxkaon1izyqsu8wgcic",
      },
      tiles: {},
    },
    datastore: null,
  }),



  components: {},
  mounted() {
    this.datastore = new DIDDataStore({
      ceramic: this.ceramic,
      model: this.aliases,
    });
  },

  methods: {
    async authenticateWithEthereum(ethereumProvider) {
      const accounts = await ethereumProvider.request({
        method: "eth_requestAccounts",
      });

      const authProvider = new EthereumAuthProvider(
        ethereumProvider,
        accounts[0]
      );
      const session = new DIDSession({ authProvider });
      const did = await session.authorize();
      console.log("my did", did);
      this.ceramic.did = did;
    },

    async connect() {
      if (window.ethereum == null) {
        console.error("No injected Ethereum provider found");
      }
      try {
        this.loading = true;
        await this.authenticateWithEthereum(window.ethereum);
        await this.getProfileFromCeramic();
        this.loading = false;
      } catch (error) {
        console.error(error);
        this.loading = false;
      }
    },

    async getProfileFromCeramic() {
      try {
        //use the DIDDatastore to get profile data from Ceramic
        console.log("getProfileFromCeramic", this.datastore);
        let did = this.datastore.id;
        did = did.substring(did.lastIndexOf(":") + 1);
        
        this.blockchainProfile = await this.datastore.get("BasicProfile");
        this.$emit("onConnect", did, this.datastore);

      } catch (error) {
        console.error(error);
      }
    },
  },
  computed: {
    btnText() {
      if (this.blockchainProfile) return "Connected";
      else return "Sign in with the wallet";
    },
  },
};
</script>
<style scoped></style>
