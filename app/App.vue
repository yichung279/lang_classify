<template lang="pug">
#app
  .ui.active.dimmer
    i.ui.icon.hourglass.half.big#time(v-if="'timing'==status") :{{ countdown }}
    .ui.loader.massive(v-if="'analizing'==status")
    .circular.ui.icon.button(@click="start_record")
      i.microphone.icon.huge
  #uploader


</template>

<script>
import 'semantic-ui-offline/semantic.min.css'
import Recorder from 'recorder-js'
const axios = require('axios')
export default {

  data() { return {
    status: '',
    countdown: 10,
  }},

  methods: {
    start_record () {
      self = this
      navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then((stream)=>{
        self.handleSuccess(stream)
        self.status = 'timing'
        setInterval(() => self.countdown--, 1000)
        setTimeout(() => self.stop_record(), 10000)
      })
    },
    handleSuccess (stream) {
      let context =  new window.AudioContext()
      let recorder = new Recorder(context, {onAnalysed: data=>console.log(data)})
      recorder.init(stream)
      recorder.start()
      setTimeout(()=>{
        recorder.stop()
        .then((blob)=>{
          console.log(blob)
          let form = new FormData(document.getElementById("uploader"))
          form.append("data", blob.blob)
          axios.post(`/upload`, form)
        })
      }, 10000)
    },

    stop_record () {
      this.status = 'analizing'
    }

      // axios.post(`/upload`, speech)
  },

}
</script>

<style lang="sass" scoped>
#app
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif
.button
  position: fixed
  bottom: 10vh
#time
  color: white
</style>`

<!--
  vi:et:sw=2:ts=2
-->
