/*
  @desc Recommendations library
  @docs https://www.npmjs.com/package/python-shell
*/
const { PythonShell } = require('python-shell');
const defaultOptions = require('./options');

/*
@desc Contains all example functions so they can be imported as a package
*/
const Recommender = {
    /*
    @desc Top 10 recommendations from user weights
    @return the recommendations after the script finishes
    */
    restaurant_recommender: args => {
        return new Promise((resolve, reject) => {
            PythonShell.run(
                '/restaurant.py',
                { ...defaultOptions, ...args },
                (err, res) => {
                    if (err) reject(err);
                    resolve(res);
                }
            );
        });
    },

    /*
    @desc Top 10 recommendations from user weights
    @return the recommendations after the script finishes
    */
    user_recommender: args => {
        return new Promise((resolve, reject) => {
            PythonShell.run(
                '/user.py',
                { ...defaultOptions, ...args },
                (err, res) => {
                    if (err) reject(err);
                    resolve(res);
                }
            );
        });
    }
};

module.exports = Recommender;