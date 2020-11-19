const express = require('express');
const router = express.Router();
const Recommender = require('../lib/recommender');


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
    const postedArgs = [req.query.category, req.query.price, req.query.rating];

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

module.exports = router;