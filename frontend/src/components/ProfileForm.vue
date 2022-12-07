<template>
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
  >
    <v-text-field
      v-model="profileToEdit.name"
      label="Name"
      :filled="!edit"
    ></v-text-field>

    <v-text-field
      v-model="profileToEdit.description"
      label="Short description"
      :filled="!edit"
    ></v-text-field>

    <v-text-field
      v-model="profileToEdit.emoji"
      label="Emoji"
      :filled="!edit"
    ></v-text-field>

    <v-text-field
      v-model="profileToEdit.name"
      label="First Name"
      :filled="!edit"
    ></v-text-field>

    <v-text-field
      v-model="profileToEdit.name"
      label="First Name"
      :filled="!edit"
    ></v-text-field>
  </v-form>
</template>

<script>
import { BasicProfile } from "@datamodels/identity-profile-basic";

export default {
  name: "ProfileForm",

  data: () => ({
    valid: true,
    profileToEdit: null,
  }),

  props: {
    profile: BasicProfile,
    edit: Boolean,
  },

  mounted() {
    this.profileToEdit = this.profile;
    console.log("this.profileToEdit", this.profileToEdit);
  },

  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
  computed: {},
};
</script>
<style scoped></style>
