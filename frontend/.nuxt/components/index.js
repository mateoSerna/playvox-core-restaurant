import { wrapFunctional } from './utils'

export { default as CoreIngredients } from '../../components/core-ingredients.vue'
export { default as CoreNewIngredient } from '../../components/core-new-ingredient.vue'
export { default as CoreOrders } from '../../components/core-orders.vue'

export const LazyCoreIngredients = import('../../components/core-ingredients.vue' /* webpackChunkName: "components/core-ingredients" */).then(c => wrapFunctional(c.default || c))
export const LazyCoreNewIngredient = import('../../components/core-new-ingredient.vue' /* webpackChunkName: "components/core-new-ingredient" */).then(c => wrapFunctional(c.default || c))
export const LazyCoreOrders = import('../../components/core-orders.vue' /* webpackChunkName: "components/core-orders" */).then(c => wrapFunctional(c.default || c))
