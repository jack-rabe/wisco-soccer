const path = require('path');
const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser')
// load routes
const homeRouter = require('./routes/home')

const app = express();
app.use(express.static(path.resolve(__dirname, 'public')));
app.use(morgan('dev'));
app.use(bodyParser.json()) // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

// mount routes
app.use(homeRouter)

const port = 3000;
app.listen(port, () => {
	console.log(`Server listening at http://localhost:${port}`);
});

module.exports = app;