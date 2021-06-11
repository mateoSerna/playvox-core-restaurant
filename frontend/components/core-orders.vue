<template>
  <v-row>
    <v-col>
      <v-row dense justify="center" align="center">
        <v-col cols="1">
          <v-text-field
            v-model="quantity"
            label="Orders"
            class="text-right"
            type="number"
            min="1"
            max="10"
            outlined
            hide-details
            dense
            :disabled="creating"
          />
        </v-col>
        <v-col>
          <v-btn
            type="button"
            color="primary"
            :loading="creating"
            :disabled="creating"
            @click="onNewOrder"
          >
            Send Order(s)
          </v-btn>
          <v-btn
            type="button"
            color="secondary"
            :loading="loading"
            :disabled="loading"
            @click="onGetOrders"
          >
            Refresh
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-data-table
            :headers="headers"
            :items="orders"
            :items-per-page="15"
            :loading="loading"
            class="elevation-1"
            :sort-by="['timestamp.N']"
            :sort-desc="[true]"
          >
            <template v-slot:[`item.timestamp.N`]="{ item }">
              {{ new Date(parseInt(item.timestamp.N) * 1000).toLocaleString() }}
            </template>
            <template v-slot:[`item.status`]="{ item }">
              <v-chip
                color="blue darken-2"
                small
                dark
              >
                {{ item.status.S.toUpperCase() }}
              </v-chip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import AWS from 'aws-sdk'

export default {
  data () {
    return {
      kinesis: null,
      creating: false,
      quantity: 1,
      orders: [],
      loading: false,
      headers: [
        { text: 'Order ID', value: 'order_id.S' },
        { text: 'Ingredients', value: 'ingredients.SS' },
        { text: 'Status', value: 'status' },
        { text: 'Date', value: 'timestamp.N' }
      ]
    }
  },

  mounted () {
    this.kinesis = new AWS.Kinesis()
    this.onGetOrders()
  },

  methods: {
    async onGetOrders () {
      this.loading = true
      this.orders = []
      const request = await this.$axios.get(`${process.env.kitchenUrl}/orders`)

      if (request.data) {
        this.orders = request.data.Items
      }

      this.loading = false
    },

    async onNewOrder () {
      this.creating = true
      const quantity = (this.quantity < 1) ? 1 : ((this.quantity > 10) ? 10 : this.quantity)

      for (let i = 0; i < quantity; i++) {
        const request = await this.$axios.get(`${process.env.warehouseUrl}/recipe/random`)

        if (!request.data.recipe.error) {
          const ingredients = request.data.recipe.ingredients
          const params = {
            Data: JSON.stringify({ ingredients }),
            PartitionKey: 'P1',
            StreamName: 'core-restaurant-orders'
          }
          const response = await this.kinesis.putRecord(params).promise()
          if (response.SequenceNumber) {
            console.log(response)
          }
        }
      }

      this.creating = false
      this.onGetOrders()
    }
  }
}
</script>
