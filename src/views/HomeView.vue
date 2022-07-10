<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <p class="counter">
      <!-- <span v-bind:class="{greentextclass: $store.state.counter > 5}">{{ getCounter }}</span> -->
      <span :style="{color: $store.state.colorCode}">{{ getCounter }}</span>
    </p>
    <div class="buttons">
      <button @click="$store.dispatch('decreaseCounter')">-</button>
      <button @click="$store.dispatch('increaseCounter')">+</button>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  computed: {
    getCounter() {
        return this.$store.state.counter
    },
    colorCode: {
      get() {
        return this.$store.state.colorCode
      }

    }
  },
  mounted() {
    this.$store.dispatch("fetchCounter");
}
}
</script>

<style>
  div {
    margin-bottom: 10px;
  }
  .counter {
    font-size: 80px;
  }
  .buttons button {
    font-size: 40px;
    width: 100px;
    margin: 0 10px;
  }
  .greentextclass {
    color: green
  }
</style>