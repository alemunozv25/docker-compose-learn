
const http = require("http");

const hostname = '0.0.0.0'; // All network interfaces (better for containers usage)
const port = 8199;

const requestListener = function (req, res) {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello, Node.js Web Server!\n');
};

const server = http.createServer(requestListener);

// SHORTER ALTERNATE WAY
// const server = http.createServer((req, res) => {
//   res.statusCode = 200;
//   res.setHeader('Content-Type', 'text/plain');
//   res.end('Hello, Node.js Web Server!\n');
// });


server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});