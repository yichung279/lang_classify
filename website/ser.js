const config = require('./config')
const { execFileSync } = require('child_process')
const express = require('express')
const fs =require('fs')
const https = require('https')
const fileUpload = require('express-fileupload')

const app = express()

const {ca, key, cert} = config.ssl
const options = {
  ca : fs.readFileSync(ca),
  key: fs.readFileSync(key),
  cert: fs.readFileSync(cert)
}

https.createServer(options, app).listen(config.port,
  console.log(`listen on port:  ${config.port}`)
)

app.use(express.static(__dirname+'/dist'))

app.use(express.json())
app.use(fileUpload());

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
  next()
})

app.post('/upload', async (req, res) => {
  await req.files.data.mv('test.wav')
  const result = execFileSync("./predict.py").toString()

  // 0=>Tauwanese, 1=>Chinese
  res.send(result[result.length-2])
})
// vi:et:sw=2:ts=2
