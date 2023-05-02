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

//app.use(function(req,res,next){setInterval(next,10000)});

async function wait (ms) {
  return new Promise((resolve, reject) => {
    setTimeout(resolve, ms)
  });
}

app.get('/', async(req, res) => {
  activeConnections++;
  await wait(5*1000);
  console.log(req.query);
  res.json({ 'activConnections': activeConnections, 'port': 6000, 'reqNum': req.query.reqNum});
  res.end();
});

server.listen(6000, () => {
  console.log('Server listening on port 6000');
});
