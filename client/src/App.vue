<template>
    <div id="app">
        <img alt="Vue logo" src="./assets/logo.png" />
        <HelloWorld msg="Welcome to Your Vue.js App" />
    </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import io from 'socket.io-client';

const socket = io('https://localhost:5000/test');

export default {
    name: "app",
    components: {
        HelloWorld
    },
    methods: {
        connect() {
            socket.on('my response', { data: 'Hi!' })
            socket.emit('error event')
        }
    },
    created() {
        this.connect();
    }
};
</script>

<style>
#app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
