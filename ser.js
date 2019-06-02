const { execSync } = require('child_process')
const express = require('express')

const app = express()
const port = 10300

app.listen(port, () => {
  console.log(`Listening on port ${port}`)
})

// vi:et:sw=2:ts=2
