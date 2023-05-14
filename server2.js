const express = require('express');
const app = express();
const server = require('http').createServer(app);

let activeConnections = 0;


app.get('/', async(req, res) => {
  activeConnections++;
  console.log(req.query);
  delay = Number(req.query.pcktSize)/Number(req.query.weight);
  //delay due to processing
  for(let i=0;i<delay*100000000;i++);
  
  res.json({ 'activConnections': activeConnections, 'port': 8080, 'reqNum': req.query.reqNum });
  res.end();
});

server.listen(8080, () => {
  console.log('Server listening on port 8080');
});
