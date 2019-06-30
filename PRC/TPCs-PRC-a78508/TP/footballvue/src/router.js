import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/competitions',
      name: 'home',
      component: () => import('./views/listCompetitions.vue')
    },
    {
      path: '/competitions/:id/seasons',
      name: 'seasons',
      component: () => import('./views/listSeasons.vue')
    },
    {
      path: '/classification/:id',
      name: 'classification',
      component: () => import('./views/listClassification.vue')
    },
    {
      path: '/player/:id',
      name: 'player',
      component: () => import('./views/listPlayer.vue')
    },
    {
      path: '/squad/:id',
      name: 'squad',
      component: () => import('./views/listSquad.vue')
    }
  ]
})
