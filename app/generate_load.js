let http = require('http');
let url = "http://localhost:5000/";
let tagsAPI = url + "api/tags/";
let sentimentAPI = url + "api/sentiment/";
let twitterAPI = url + "api/twitter/";
let requests = 5;
let completedRequests = 0;

function makeRequests() {
    for (let i = 0; i < requests; i++) {
        console.log("requesting #" + i);
        http.get(url, function (res) {
            console.log("Got #" + i + " " + res.statusCode);
            completedRequests++;
            if (completedRequests === requests) {
                completedRequests = 0;
                makeRequests();
            }
        });

        http.get(tagsAPI, function (res) {});
        http.get(sentimentAPI, function (res) {});
        http.get(twitterAPI, function (res) {});

    }
}

makeRequests();