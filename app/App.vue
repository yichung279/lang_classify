<template lang="pug">
#app
  .ui.active.dimmer
    i.ui.icon.hourglass.half.big#time(v-if="'timing'==status") :{{ countdown }}
    .ui.loader.massive(v-if="'analizing'==status")
    .circular.ui.icon.button(@click="start_record")
      i.microphone.icon.huge


</template>

<script>
import 'semantic-ui-offline/semantic.min.css'
const axios = require('axios')
export default {

  data() { return {
    status: '',
    countdown: 10
  }},

  methods: {
    start_record () {
      this.status = 'timing'
      setInterval(() => this.countdown--, 1000)
      setTimeout(() => this.stop_record(), 10000)

      navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(this.handleSuccess)
    },
    handleSuccess (stream) {
      const options = {mimeType: 'audio/webm'}
      const recordedChunks = []
      const mediaRecorder = new MediaRecorder(stream, options)

      mediaRecorder.addEventListener('dataavailable', function(e) {
	if (e.data.size > 0) {
	  recordedChunks.push(e.data)
	}
      })

      mediaRecorder.addEventListener('stop', function() {
        console.log("analizing...")
        // axios.post(`/upload`, recordedChunks)
	// downloadLink.href = URL.createObjectURL(new Blob(recordedChunks))
	// downloadLink.download = 'acetest.wav'
      })

      mediaRecorder.start()
      setTimeout(() => mediaRecorder.stop(), 10000)
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
