// Web server framework
const express = require('express');

// Library to help parse requests
const bodyParser = require('body-parser');

// Route
const recommender = require('./routes/recommender');

// Our express application
const app = express()

// Body Parser Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(bodyParser.text());


// API Route
app.use('/recommender', recommender);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on PORT ${PORT}`));