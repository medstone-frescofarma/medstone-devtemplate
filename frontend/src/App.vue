<template>
  <v-app>
    <Drawer />
    <v-app-bar app>
      test 2
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
    <v-footer app>
    </v-footer>
  </v-app>
</template>

<script>
import Drawer from './views/Drawer.vue'
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',

  components: {
    Drawer,
    HelloWorld,
  },

  data: () => ({
    //
  }),
}
</script>
