const express = require('express');
const app = express();
const server = require('http').createServer(app);

let activeConnections = 0;

// server.on('connection', () => {
//   activeConnections++;
//   console.log('New client connected. Total active connections:', activeConnections);
// });

// server.on('close', () => {
//   activeConnections--;
//   console.log('Client disconnected. Total active connections:', activeConnections);
// });

app.use(function(req,res,next){setTimeout(next,1000)});

app.get('/', (req, res) => {
  activeConnections++;
  console.log(req.params);
  res.json({ 'activConnections': activeConnections, 'port': 6000, 'reqNum': req.params.reqNum});
  res.end();
});

server.listen(6000, () => {
  console.log('Server listening on port 6000');
});
