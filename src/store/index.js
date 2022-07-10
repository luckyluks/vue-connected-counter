import axios from 'axios';
import { createStore } from 'vuex'

let baseUrl = "http://192.168.0.72:8000/counter"

export default createStore({
  state: {
    counter: 0,
    colorCode: 'gray'
  },
  getters: {
  },
  mutations: {
    setCounter(state, newNumber){
      state.counter = newNumber
    },
    setColorCode(state, newValue){
      state.colorCode = newValue
    }
  },
  actions: {
    increaseCounter({ commit }){
      axios(baseUrl).then(
        response => {
          axios.post(baseUrl + `?counter=${(response.data.counter+1)}`).then(
            response => {
              // console.log("new value: ", response.data.counter);
              commit('setCounter', response.data.counter);
              this.dispatch('setColorCode', response.data.counter)
            }
          )
        }
      )
    },
    decreaseCounter({ commit }){
      axios(baseUrl).then(
        response => {
          axios.post(baseUrl + `?counter=${(response.data.counter-1)}`).then(
            response => {
              // console.log("new value: ", response.data.counter);
              commit('setCounter', response.data.counter)
              this.dispatch('setColorCode', response.data.counter)
            }
          )
        }
      )
    },
    fetchCounter({ commit }) {
      axios(baseUrl).then(
        response => {
          commit('setCounter', response.data.counter)
          this.dispatch('setColorCode', response.data.counter)
        }
      )
    },
    setColorCode({ commit }, newValue) {
      
      let newColor = 'black';
      switch (true) {
        // case (newValue == 0):
        //   newColor = 'black';
        //   break;
        case (newValue >= 5):
          newColor = 'green';
          break;
        case (newValue > 0 && newValue < 5):
          newColor = 'lightgreen';
          break;
        case (newValue <= -5):
          newColor = 'red';
          break;
          case (newValue < 0 && newValue > -5):
            newColor = 'orange';
            break;
      }
      commit('setColorCode', newColor)
    }
  },
  modules: {
  }
})
