const path = require('path');
const express = require('express');
const morgan = require('morgan');
// load routes
const homeRouter = require('./routes/home.js')

const app = express();
app.use(express.static(path.resolve(__dirname, 'public')));
// log requests
app.use(morgan(':method :url :status'));
// mount routes
app.use('/', homeRouter)

const port = 3000;
app.listen(port, () => {
	console.log(`Server listening at http://localhost:${port}`);
});

module.exports = app;