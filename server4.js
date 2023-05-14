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

// app.use(async function(req,res,next){
//   console.log('before wait', new Date());
//   await wait(5*1000);
//   console.log('after wait', new Date());
//   next();

// })

app.get('/', async (req, res) => {
  activeConnections++;
  delay = Number(req.query.pcktSize)/Number(req.query.weight);
  //delay due to processing
  for(let i=0;i<delay*100000000;i++);

  res.json({ 'activConnections': activeConnections, 'port': 6999, 'reqNum': req.query.reqNum });
  console.log('after res', new Date());
  //res.end();
});

server.listen(6999, () => {
  console.log('Server listening on port 6999');
});
