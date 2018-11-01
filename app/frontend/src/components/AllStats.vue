<template>
  <div class="row left-align">
    <div id="loader">
      <div class="progress red">
        <div class="indeterminate red lighten-4"></div>
      </div>
    </div>

    <div class="col s12 m4">
      <h4 class="center-align">States</h4>
      <ul class="collapsible">
        <li v-for="state in this.sentiment.states" :key="state.name">
          <div class="collapsible-header"><i class="material-icons">map</i>{{state.name}}</div>
          <div class="collapsible-body">
            <h5 class="no-margin">Stats for {{state.name}}</h5>
            <span class="">Average Sentiment: {{state.average}}%</span><br>
            <span class="">Minimum Sentiment: {{state.min}}%</span><br>
            <span class="">Maximum Sentiment: {{state.max}}%</span><br>
            <span class="">Total Tweets: {{state.count}}</span><br>
          </div>
        </li>
      </ul>
      <p class="center-align">Note: This is a <i>subset</i> of the total tweets because not every tweet has a location.
      </p>
    </div>

    <div class="col s12 m4">
      <h4 class="center-align">Tracked Tags</h4>

      <ul class="collection z-depth-1">
        <li v-for="tag in this.sentiment.tags" :key="tag.tag" class="collection-item avatar avatartag">
          <img :src="tag.image" alt="" class="circle z-depth-2">
          <p class="title"><b>{{tag.displayname}}</b>
            (<a :href="'http://twitter.com/' + tag.tag" target="_blank"><i>{{tag.tag}}</i></a>)</p>
          <span class="">Average Sentiment: {{tag.average}}%</span><br>
          <span class="">Minimum Sentiment: {{tag.min}}%</span><br>
          <span class="">Maximum Sentiment: {{tag.max}}%</span><br>
          <span class="">Total Tweets: {{tag.count}}</span><br>
        </li>
      </ul>
    </div>

    <div class="col s12 m4">
      <h4 class="center-align">Other</h4>
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
    </div>
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
      "#": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "##": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "###": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "####": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "#####": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "######": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "#######": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
      "########": {
        "average": 0,
        "count": 0,
        "max": 0,
        "min": 0,
        "name": "",
        "tags": {
          "@": {
            "average": 0,
            "count": 0,
            "displayname": "@",
            "image": "",
            "max": 0,
            "min": 0,
            "tag": "@######"
          },
        }
      },
    },
    "tags": {}
  };

  export default {
    name: 'AllStats',
    data() {
      return {
        refresh: 10000,
        sentiment: placeholder,
        timer: '',
      }
    },
    methods: {
      getSentimentFromBackend() {
        const path = window.location.origin + `/api/sentiment`;
        axios.get(path)
          .then(response => {
            document.getElementById("loader").classList.add("hidden");
            this.sentiment = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted: function () {
      document.getElementById("loader").classList.remove("hidden");
      this.getSentimentFromBackend();
      this.timer = setInterval(this.getSentimentFromBackend, this.refresh);

      setTimeout(function () {
        let elems = document.querySelectorAll('.collapsible');
        let instances = M.Collapsible.init(elems, {});
      }, 0);

    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
