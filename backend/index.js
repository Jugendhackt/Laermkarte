const express = require('express')
const app = express()
app.use(express.json())
const port = 5000
const cors = require('cors')
const fs = require('fs')

let rawdata = JSON.parse(fs.readFileSync('result.json'))


const fakedata = {
  "location" : "52.532265, 13.343671",
  
  "lautstaerke" :"56", 

  }

const fakedataliste = [
  {
    "long" : "52.532265",
    "lat" : "13.343671",
    "lautstaerke" :"56",  
  },
  {
    "long" : "52.515918",
    "lat" : "13.294888",
    "lautstaerke" :"66",
  },
  {
    "long" : "52.53276",
    "lat" : "13.343803",
    "lautstaerke" :"76",  
  },
  {
    "long" : "53.515918",
    "lat" : "13.292768",
    "lautstaerke":"50",
  },
  {
    "long" : "52.532265",
    "lat" : "13.343671",
    "lautstaerke" :"56",  
  },
  {
    "long" : "52.515918",
    "lat" : " 14.227439",
    "lautstaerke" :"96",
  },
  {
    "long" : "52.992265",
    "lat" : "13.340271",
    "lautstaerke" :"82",  
  },
  {
    "long" : "52.515678",
    "lat" : " 13.203888",
    "lautstaerke" :"78",
  }
]

const fakedata1 = {
 "location" : "52.532265, 13.343671",
 "location" :"52.541322, 13.359684" ,
 "location" :"52.515918, 13.294888" ,
 "location" : "52.531175, 13.381604" ,
 "location" : "52.523750, 13.402122" ,
 "location" : "52.551108, 13.295689" ,
 "location" : "52.367112, 13.487041" ,
 "location" : "52.540917, 13.427747" ,
 "location" : "52.507286, 13.337433" ,
 "location" : "52.504986, 13.338064" ,
 "location" : "52.535135, 13.512334" ,

 "lautstaerke" :"56", 

 "Datum" : "09/10/21",
}
app.use(
  cors({
    origin: '*'
  })
)
app.get('/', (req, res) => {
  res.send('Hello Alpakas!')
})

app.get('/faked', (req, res) => {
  res.send(fakedata)
})

app.get('/laermliste', (req, res) => {
  /*res.send(fakedataliste.map(item => {
    return {lat: Number.parseFloat(item.long) ,
    lng: Number.parseFloat(item.lat),
    count: 13}
  }))*/
  res.send(rawdata)
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

var sensorData 

app.post('/sensordata', (req, res) => {
  sensorData = {
    "lat": req.body.location.latitude,
    "long": req.body.location.longitude,
    "count": req.body.value
  }
})

app.get('/sensordata', (req, res) => {
  if (sensorData){
    return res.json(sensorData).send()
  } 
  return res.status(404).send()
})