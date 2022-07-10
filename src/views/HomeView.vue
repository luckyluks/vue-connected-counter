<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <p class="counter">
      <!-- <span v-bind:class="{greentextclass: $store.state.counter > 5}">{{ getCounter }}</span> -->
      <span :style="{color: $store.state.colorCode}">{{ getCounter }}</span>
    </p>
    <div class="buttons">
      <button id="decrease" @click="updateOtherClients">-</button>
      <button id="increase" @click="updateOtherClients">+</button>
    </div>
  </div>
</template>

<script>


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
    // setup ws connection
    let wsId = this.$uuid('small');
    this.connection = new WebSocket(`ws://192.168.0.72:8000/ws/${wsId}`);
    this.connection.onopen = () => console.log(`WS connection established (${wsId})`);
    this.connection.onmessage = (event) => {
      let json = JSON.parse(event.data)
      // only act on update events
      if (json.type == "database-update-event"){
        this.processUpdate(event)
      } else {
        console.log("unknown event type: ", event)
      }
    }

    // update data on first load
    this.$store.dispatch("fetchCounter");
  },
  methods: {
    /**
     * trigger the data update -> backend will publish ws broadcast
     * @param {*} event 
     */
    updateOtherClients(event) {
      // detect action and trigger local update
      if (event.target.id == "decrease") {
        this.$store.dispatch('decreaseCounter')
      } else if (event.target.id == "increase") {
        this.$store.dispatch('increaseCounter')
      }
      // broadcast update to other connected clients
      // this.sendUpdate() - not necessary anymore - server broadcasts update
    },

    /**
     * Publish a ws json message
     */
    // sendUpdate() {
    //   // push json with data
    //   this.connection.send(JSON.stringify({
    //     "counter": this.$store.state.counter
    //   }));
    // },

    /**
     * Handle ws update event
     * @param {*} event 
     */
    processUpdate(event) {
      // parse json of event and send commit to store
      let data = JSON.parse(event.data);
      this.$store.commit('setCounter', data.counter)
    }
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
  .magicColor {
    color: purple;
    font-size: 99px;
  }
</style>