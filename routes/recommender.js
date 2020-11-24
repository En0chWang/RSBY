const { response } = require('express');
const express = require('express');
const router = express.Router();
const Recommender = require('../lib/recommender');
const request = require('request')
const Axios = require('axios');

// @route  GET /recommender/top10restaurants
// @desc   Returns more information about a restaurant
// @access Public
router.get('/top10restaurants', (req, res) => {
  /*
  Sending these exampleArgs as (key, value) pairs in the POST request.
    Looks like this as JSON in the client request
    {
      "category": "Japanese",
      "price": "$$",
      "rating": "3.5"
    }
  */
  const postedArgs = [req.query.category, req.query.price, req.query.rating, req.query.city, req.query.state];

  /*
    @desc Get restaurant info
  */
  Recommender.restaurant_recommender({ args: postedArgs })
    .then(result => res.send(JSON.parse(result[0])))
    .catch(err =>
      res.json({
        errors: {
          error: err,
        },
      })
    );
});

async function fetch(restaurants) {
  const promises = restaurants.map(async restaurant => {
    const response = await Axios({
      method: 'GET',
      url: 'http://3.21.133.7/api/businessId?businessId=' + restaurant
    });
    return response.data[0]["user_id"];
  });
  const results = await Promise.all(promises);
  return [results.toString()];
}

// @route  GET /recommender/top10users
// @desc   Returns recommended users based on restauarants
// @access Public
router.get('/top10users', (req, res) => {

  fetch(req.query.restaurants.split(", ")).then((postedArgs) => {
    /*
      @desc Get restaurant info
    */
    Recommender.user_recommender({ args: postedArgs })
      .then(result => res.send(JSON.parse(result[0])))
      .catch(err =>
        res.json({
          errors: {
            error: err
          },
        })
      );
  })

});

router.get('/reviews', (req, res) => {
  /*
Sending these exampleArgs as (key, value) pairs in the POST request.
  Looks like this as JSON in the client request
  {
    "category": "Japanese",
    "price": "$$",
    "rating": "3.5"
  }
*/
  const business_id = req.query.business_id;
  url = "http://3.21.133.7/api/businessId?businessId=" + business_id

  payload = {}
  headers = {
    'Content-Type': 'application/json',
    'charset': 'UTF-8'
  }

  request(url, (error, response, data) => {
    if (error) {
      res.json(error)
    }
    res.json(JSON.parse(data))
  });
});

module.exports = router;