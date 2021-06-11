<template>
  <v-dialog
    v-model="dialog"
    max-width="600px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="primary"
        dark
        v-bind="attrs"
        v-on="on"
      >
        New Ingredient
      </v-btn>
    </template>
    <v-form @submit.prevent="onSaveIngredient" ref="form">
      <v-card>
        <v-card-title>
          <span class="text-h5">New Ingredient</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="ingredient.name"
                  label="Name of the Ingredient*"
                  :rules="[v => !!v || 'Name is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col>
                <v-autocomplete
                  v-model="ingredient.is_active"
                  :items="['Active', 'Inactive']"
                  :rules="[v => !!v || 'Status is required']"
                  label="Status*"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            text
            @click="dialog = false"
            :disabled="creating"
          >
            Close
          </v-btn>
          <v-btn
            type="submit"
            color="blue darken-1"
            text
            :loading="creating"
          >
            Save Ingredient
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      creating: false,
      ingredient: {
        name: '',
        is_active: 'Active'
      }
    }
  },

  methods: {
    async onSaveIngredient () {
      this.$refs.form.validate()

      if (this.ingredient.name && this.ingredient.is_active) {
        this.creating = true
        const ingredient = {
          Item: {
            name: this.ingredient.name,
            is_active: this.ingredient.is_active.toLowerCase()
          }
        }

        await this.$axios.post(`${process.env.warehouseUrl}/ingredient`, ingredient)
      }

      this.dialog = false
      this.creating = false
      this.ingredient = {
        name: '',
        is_active: 'Active'
      }
    }
  }
}
</script>
