<template>
  <v-row>
    <v-col>
      <v-row dense justify="center" align="center">
        <v-col>
          <core-new-ingredient />
          <v-btn
            type="button"
            color="secondary"
            :loading="loading"
            :disabled="loading"
            @click="onGetIngredients"
          >
            Refresh
          </v-btn>
        </v-col>
        <v-col cols="3">
          <v-autocomplete
            v-model="filters.status"
            :items="['Active', 'Inactive']"
            label="Status*"
            @change="onGetIngredients"
          ></v-autocomplete>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-data-table
            :headers="headers"
            :items="ingredients"
            :items-per-page="15"
            :loading="loading"
            :sort-by="['timestamp.N']"
            :sort-desc="[true]"
            class="elevation-1"
          >
            <template v-slot:[`item.timestamp.N`]="{ item }">
              {{ new Date(item.timestamp.N * 1000).toLocaleString() }}
            </template>
            <template v-slot:[`item.is_active`]="{ item }">
              <v-chip
                color="blue darken-2"
                small
                dark
              >
                {{ item.is_active.S.toUpperCase() }}
              </v-chip>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
              <v-btn
                :loading="item.updating"
                class="mx-1"
                fab
                dark
                x-small
                :color="item.is_active.S === 'active' ? 'orange darken-2' : 'green darken-2'"
                @click="onUpdateIngredient(item)"
              >
                <v-icon v-if="item.is_active.S === 'active'" dark>
                  mdi-cancel
                </v-icon>
                <v-icon v-else dark>
                  mdi-check
                </v-icon>
              </v-btn>
              <v-btn
                :loading="item.deleting"
                class="mx-1"
                fab
                dark
                x-small
                color="red darken-2"
                @click="onDeleteIngredient(item)"
              >
                <v-icon dark>
                  mdi-delete
                </v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import CoreNewIngredient from '~/components/core-new-ingredient.vue'

export default {
  components: {
    CoreNewIngredient
  },
  data () {
    return {
      kinesis: null,
      ingredients: [],
      loading: false,
      filters: {
        status: 'Active'
      },
      headers: [
        { text: 'Ingredient ID', value: 'ingredient_id.S' },
        { text: 'Name', value: 'name.S' },
        { text: 'Status', value: 'is_active' },
        { text: 'Date', value: 'timestamp.N' },
        { text: 'Actions', value: 'actions' }
      ]
    }
  },

  mounted () {
    this.onGetIngredients()
  },

  methods: {
    async onGetIngredients () {
      this.loading = true
      this.ingredients = []

      const request = await this.$axios.get(
        `${process.env.warehouseUrl}/ingredients`, {
          params: {
            status: this.filters.status.toLowerCase()
          }
        }
      )

      if (request.data) {
        this.ingredients = request.data.Items
      }

      this.loading = false
    },

    async onUpdateIngredient (ingredient) {
      this.$set(ingredient, 'updating', true)

      const item = {
        Item: {
          ingredient_id: ingredient.ingredient_id.S,
          name: ingredient.name.S,
          timestamp: ingredient.timestamp.N,
          is_active: ingredient.is_active.S === 'active' ? 'inactive' : 'active'
        }
      }
      await this.$axios.patch(`${process.env.warehouseUrl}/ingredient`, item)
      this.onGetIngredients()
    },

    async onDeleteIngredient (ingredient) {
      this.$set(ingredient, 'deleting', true)

      await this.$axios.delete(
        `${process.env.warehouseUrl}/ingredient/${ingredient.ingredient_id.S}/${ingredient.timestamp.N}`
      )
      this.onGetIngredients()
    }
  }
}
</script>
