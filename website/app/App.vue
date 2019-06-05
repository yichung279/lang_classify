<template lang="pug">
#app
  .ui.active.dimmer
    i.ui.icon.hourglass.half.big#time(v-if="'timing'==status") :{{ countdown }}
    .ui.loader.massive(v-if="'analizing'==status")
    .ui.label.huge(v-if="'analized'==status") {{lang}}
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
    countdown: 7,
    lang: '中文',
    time: '',
    recorder: ''
  }},

  methods: {
    start_record () {
      const self = this
      this.countdown = 7
      navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then((stream)=>{
        self.handleSuccess(stream)
        self.status = 'timing'
        self.timer = setInterval(() => self.countdown--, 1000)
        setTimeout(() => self.stop_record(), 7000)
      })
    },
    handleSuccess (stream) {
      let context =  new window.AudioContext()
      this.recorder = new Recorder(context)
      //, {onAnalysed: data=>console.log(data)})
      this.recorder.init(stream)
      this.recorder.start()
    },

    stop_record () {
      this.status = 'analizing'
      this.recorder.stop()
      .then((audio)=>{
        let form = new FormData(document.getElementById("uploader"))
        form.append("data", audio.blob)
        axios.post(`/upload`, form)
        .then(lang => {
          this.status = 'analized'
          if (1 == lang.data) this.lang = '中文'
          else if (0 == lang.data) this.lang = '台語'
        })
      })
      clearInterval(this.timer)
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
