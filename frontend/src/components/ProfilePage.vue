<template>
  <v-form
    ref="form"
    v-model="valid"
    v-if="profileToEdit"
    lazy-validation
    :loading="loading"
  >

    <div class="text-h3 text-center mb-4">
      Blockchain user profile
    </div>
    <v-text-field
      v-model="profileToEdit.name"
      prepend-inner-icon="mdi-account"
      label="Name"
      :readonly="!edit"
    ></v-text-field>

    <v-text-field
      v-model="profileToEdit.gender"
      label="Gender"
      prepend-inner-icon="mdi-gender-male-female-variant"
      :readonly="!edit"
    ></v-text-field>

    <v-textarea
      v-model="profileToEdit.description"
      rows="2"
      prepend-inner-icon="mdi-account-details"
      label="Short description"
      :readonly="!edit"
    ></v-textarea>

    <v-text-field
      v-model="profileToEdit.emoji"
      label="Emoji"
      prepend-inner-icon="mdi-emoticon-cool-outline"
      :readonly="!edit"
    ></v-text-field>

    <v-menu ref="menu"
            v-model="menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="auto"
            :disabled="!edit">
        <template v-slot:activator="{ on, attrs }">
            <v-text-field :value="profileToEdit.birthDate"
                          label="Date Of Birth"
                          prepend-inner-icon="mdi-calendar"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                         ></v-text-field>
        </template>
        <v-date-picker ref="picker"
                       no-title
                       v-model="profileToEdit.birthDate"
                       :max="new Date().toISOString().substr(0, 10)"
                       min="1900-01-01"
                       @change="saveDOB"></v-date-picker>
    </v-menu>




    <div  v-if="(edit == true)">

      <v-btn
      color="danger"
      outlined
      rounded
      large
      class="me-3"
      @click="cancel()"
     >
      Cancel
    </v-btn>

    <v-btn
      color="success"
      outlined
      rounded
      large
      @click="update()"
     >
      Update
    </v-btn>
    
  </div>
  <div v-else>

    <v-btn
      color="warning"
      outlined
      rounded
      large
      @click="(edit = true)"
     >
      Edit profile
    </v-btn>
  </div>
  </v-form>
</template>

<script>
import BasicProfile from "@datamodels/identity-profile-basic";
import { DIDDataStore } from "@glazed/did-datastore";

export default {
  name: "ProfilePage",

  data: () => ({
    valid: true,
    profileToEdit: null,
    loading: false,
    edit: false,
    menu: false,

  }),

  props: {
    profile: BasicProfile,
    datastore: DIDDataStore,
  },

  async mounted() {
    this.profileToEdit = await this.datastore.get("BasicProfile")

  },

  watch: {
    profile(newVal) {
      console.log("watch--profile", newVal);
      this.profileToEdit = newVal;
    },
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },

    saveDOB(date){
      this.$refs.menu.save(date);
    },

    cancel(){
      console.log(this.profileToEdit, this.profile);
      this.profileToEdit = this.profile;
      this.edit = false;
    },

    async update(){
      this.edit = false;
      await this.onSubmit();
    },

    async onSubmit() {
        try {
          this.loading = true;
        //use the DIDDatastore to merge profile data to Ceramic
        await this.datastore.merge('BasicProfile', this.profileToEdit)

        //use the DIDDatastore to get profile data from Ceramic
        this.profileToEdit = await this.datastore.get('BasicProfile')

        this.loading = false;
        } catch (error) {
          this.loading = false;
        console.error(error)
        }
    },
  },
  computed: {},
};
</script>
<style scoped></style>
