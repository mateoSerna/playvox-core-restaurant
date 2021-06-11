import Vue from 'vue'
import { wrapFunctional } from './utils'

const components = {
  CoreIngredients: () => import('../../components/core-ingredients.vue' /* webpackChunkName: "components/core-ingredients" */).then(c => wrapFunctional(c.default || c)),
  CoreNewIngredient: () => import('../../components/core-new-ingredient.vue' /* webpackChunkName: "components/core-new-ingredient" */).then(c => wrapFunctional(c.default || c)),
  CoreOrders: () => import('../../components/core-orders.vue' /* webpackChunkName: "components/core-orders" */).then(c => wrapFunctional(c.default || c))
}

for (const name in components) {
  Vue.component(name, components[name])
  Vue.component('Lazy' + name, components[name])
}
