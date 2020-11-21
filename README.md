# DSCI551-Project
A Ranking System Based on YELP Open Dataset


## Core tech stack
- Node.js
- PySpark
- MySQL / DynamoDB


## Installation
Make sure Node.js and NPM is installed beforeband
```bash
git clone https://github.com/En0chWang/DSCI551-Project.git
cd DSCI551-Project
npm install
npm start
```


## Three Major APIs
| API                                                                         | Description                                                            |
|-----------------------------------------------------------------------------|------------------------------------------------------------------------|
| localhost:5000/recommender/top10users?{catgory, price, rating, city, state} | Get the top 10 restaurants based on category, price, rating, and city. |
| localhost:5000/recommender/reviews?{business_id}                            | Get restaurant reviews given restaurant id.                            |
| localhost:5000/recommender/top10users?{restaurants}                         | Get top 10 user recommendations based on the search result.            |

## License
[MIT](https://choosealicense.com/licenses/mit/)