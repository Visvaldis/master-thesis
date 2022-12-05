<template>
  <div class="MainCont">

    <div class="HeaderContainer">
      <v-btn @click="connect()">{{walletText}}</v-btn>
    </div>

    <div class="DataBlocks">
      <div class="DataBlock">
        <div id="basicProfile">
          <div class="BodyContainer">
            <h2>Basic Profile</h2>
            <p>Read from Ceramic Datamodel</p>
            <br />
            <div v-if="blockchainProfile">
              
              <v-text-field
              readonly
            v-model="blockchainProfile.name"
            label="User name"
          ></v-text-field>
          <v-text-field
          readonly
            v-model="blockchainProfile.description"
            label="Bio"
          ></v-text-field>
          
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="ProfileForm">
      <div class="BodyContainer">
        <h2>Update Basic Profile on Ceramic</h2>
        <br />
          <v-form v-model="valid">
            <v-text-field
            v-model="formName"
            hint="John Doe"
            label="User name"
          ></v-text-field>
            <v-text-field
            v-model="formBio"
            hint="I am from USA"
            label="Bio"
          ></v-text-field>
           <v-btn @click="onSubmit()" >{{submitBtnText}}</v-btn>
          </v-form>
      </div>
    </div>
  </div>
</template>

<script>

import { CeramicClient } from '@ceramicnetwork/http-client'
import { EthereumAuthProvider } from '@ceramicnetwork/blockchain-utils-linking'
import { DIDDataStore } from '@glazed/did-datastore'
import { DIDSession } from '@glazed/did-session'

export default {
  name: "BlockcainAuth",

  data: () => ({
    ceramic: new CeramicClient("https://ceramic-clay.3boxlabs.com"),
    walletText: "Connect",
    submitBtnText: "Submit",
    formName: "",
    formBio: "",
    valid: true,
    blockchainProfile: null,
    aliases: {
      schemas: {
          basicProfile: 'ceramic://k3y52l7qbv1frxt706gqfzmq6cbqdkptzk8uudaryhlkf6ly9vx21hqu4r6k1jqio',

      },
      definitions: {
          BasicProfile: 'kjzl6cwe1jw145cjbeko9kil8g9bxszjhyde21ob8epxuxkaon1izyqsu8wgcic',
      },
      tiles: {},
    },
    datastore: null,
  }),

  props:{
    walletId: String,
  },
  
  components: {},
  mounted() {
    this.datastore = new DIDDataStore({ ceramic: this.ceramic, model: this.aliases })
  },

  methods: {

    
    async authenticateWithEthereum(ethereumProvider) {
        const accounts = await ethereumProvider.request({
        method: 'eth_requestAccounts',
        })

        const authProvider = new EthereumAuthProvider(ethereumProvider, accounts[0])
        const session = new DIDSession({ authProvider })
        const did = await session.authorize()
        console.log("my did", did);
        this.ceramic.did = did
    },


    async connect(){
      if (window.ethereum == null) {
        console.error("No injected Ethereum provider found")
      }
      try{
        this.walletText = "Connecting..."
        await this.authenticateWithEthereum(window.ethereum);
        await this.getProfileFromCeramic();
        this.walletText = "Wallet Connected"
        
      } catch (error) {
        console.error(error)
      }
    },

    async getProfileFromCeramic() {
    try {
        
        //use the DIDDatastore to get profile data from Ceramic
        console.log("getProfileFromCeramic", this.datastore);
        let did = this.datastore.id;

        did = did.substring(did.lastIndexOf(':')+1);
        this.$emit('update:walletId', did);

        this.blockchainProfile = await this.datastore.get('BasicProfile')
        console.log("walletId", this.walletId);
    } catch (error) {
        console.error(error)
        }
    },


    async onSubmit() {
        try {

        const updatedProfile = {
          name: this.formName,
          description: this.formBio
        }
        this.submitBtnText = "Updating..."

        //use the DIDDatastore to merge profile data to Ceramic
        await this.datastore.merge('BasicProfile', updatedProfile)

        //use the DIDDatastore to get profile data from Ceramic
        this.blockchainProfile = await this.datastore.get('BasicProfile')

        this.submitBtnText = "Submit"
        } catch (error) {
        console.error(error)
        }
    },


  },
  computed: {},
};
</script>
<style scoped>
.SiteHeader {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: orange;
}

.HeaderContainer {
  display: flex;
  align-items: center;
}

.MainCont {
  display: flex;
  justify-content: space-around;
  padding: 10px;
}

.DataBlock {
  margin-bottom: 10px;
}

.BodyContainer {
  background-color: lightsalmon;
  border: 1px solid black;
  border-radius: 30px;
  padding: 20px;
  min-width: 250px;
}

.ProfileForm {
  min-width: 400px;
}

.formfield {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.forminput {
  min-width: 150px;
}

#submitBtn {
  display: block;
  margin: auto;
  width: auto;
}

.ProfileData {
  font-weight: bold;
}
input, select {
    border: 1px solid blue;
    background-color: white;
}
</style>
