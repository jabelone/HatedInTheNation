<template>
  <div class="tags">
    <ul class="collection z-depth-1">
      <li class="collection-item">
        <span><b>Average National Sentiment:</b></span>
        <span v-if="this.sentiment.overall.average < 20" class="title"> Very Negative ({{this.sentiment.overall.average}}%)</span>
        <span v-else-if="this.sentiment.overall.average < 40" class="title">Negative ({{this.sentiment.overall.average}}%)</span>
        <span v-else-if="this.sentiment.overall.average < 60" class="title">Neutral ({{this.sentiment.overall.average}}%)</span>
        <span v-else-if="this.sentiment.overall.average < 80" class="title">Positive ({{this.sentiment.overall.average}}%)</span>
        <span v-else-if="this.sentiment.overall.average <= 100" class="title">Very Positive ({{this.sentiment.overall.average}}%)</span>
      </li>

      <li class="collection-item">
        <span><b>Scanned Tweets:</b> {{this.sentiment.overall.count}}</span>
      </li>
    </ul>
    <p>Data on this page automatically updates.</p>
    <p id="last-update">Last update at: {{this.lastUpdate}}</p>
  </div>
</template>

<script>
  import axios from 'axios'

  let placeholder = {
    "overall": {
      "average": 0,
      "count": 0
    },
    "states": {
      "ACT": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "ACT",
        "tags": {}
      },
      "NSW": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "NSW",
        "tags": {}
      },
      "NT": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "NT",
        "tags": {}
      },
      "QLD": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "QLD",
        "tags": {}
      },
      "SA": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "SA",
        "tags": {}
      },
      "TAS": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "TAS",
        "tags": {}
      },
      "VIC": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "VIC",
        "tags": {}
      },
      "WA": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "WA",
        "tags": {}
      }
    },
    "tags": {}
  };

  export default {
    name: 'OverallStats',
    data() {
      return {
        refresh: 5000,
        lastUpdate: "none",
        sentiment: placeholder,
        timer: '',
      }
    },
    methods: {
      getSentimentFromBackend() {
        let d = new Date();
        this.lastUpdate = d.toLocaleTimeString();
        document.getElementById("last-update").classList.add("flash-text");
        setTimeout(function () {
          document.getElementById("last-update").classList.remove("flash-text");
        }, 200);

        const path = window.location.origin + `/api/sentiment/`;
        axios.get(path).then(response => {
            this.sentiment = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted: function () {
      this.getSentimentFromBackend();
      this.timer = setInterval(this.getSentimentFromBackend, this.refresh);
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
