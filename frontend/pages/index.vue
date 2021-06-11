<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="10" md="10">
      <v-card>
        <v-card-text>

          <v-tabs
            v-model="tab"
            background-color="blue darken-2"
            centered
            dark
            icons-and-text
          >
            <v-tabs-slider></v-tabs-slider>

            <v-tab href="#tab-1">
              Orders
              <v-icon>mdi-clipboard-list-outline</v-icon>
            </v-tab>

            <v-tab href="#tab-2">
              Ingredients
              <v-icon>mdi-fruit-cherries</v-icon>
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item value="tab-1" class="py-4">
              <core-orders />
            </v-tab-item>
            <v-tab-item value="tab-2" class="py-4">
              <core-ingredients />
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import AWS from 'aws-sdk'
import CoreOrders from '~/components/core-orders.vue'
import CoreIngredients from '~/components/core-ingredients.vue'

AWS.config.update({
  region: process.env.awsRegion,
  accessKeyId: process.env.awsAccessKeyId,
  secretAccessKey: process.env.awsSecretAccessKey
})

export default {
  components: {
    CoreOrders,
    CoreIngredients
  },

  data () {
    return {
      tab: null
    }
  },

  mounted () {
    console.log(process.env)
  }
}
</script>
