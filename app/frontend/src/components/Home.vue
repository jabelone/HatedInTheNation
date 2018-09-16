<template>
  <div>
    <div class="row">
      <div class="col s12 m3" style="height: 100%; background: rgba(0,0,0,0.05);">
        <h4>Overall Stats <i class="material-icons title-icon">equalizer</i></h4>
        <overall-stats/>
        <h4>Popularity <i class="material-icons title-icon">trending_upward</i></h4>
        <tags/>
        <p>The list is ranked from least to most popular and updates automatically every 30 seconds.</p>
      </div>
      <div class="col s12 m9">
        <h4 v-on:click="showTweets = true" v-bind:class="{ active: !showTweets }" class="waves-effect waves-light tweets-and-map">Show Tweets</h4>
        <h4 class="waves-effect waves-light tweets-and-map">&nbsp;/&nbsp;</h4>
        <h4 v-on:click="showTweets = false" v-bind:class="{ active: showTweets }" class="waves-effect waves-light tweets-and-map">State Breakdown</h4>

        <transition name="fade">
          <tweets v-if="showTweets"/>
        </transition>
        <transition name="fade">
          <sentiment-map v-if="!showTweets"/>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
  import Tweets from './Tweets'
  import Tags from './Tags'
  import SentimentMap from './SentimentMap'
  import axios from 'axios'
  import OverallStats from "./OverallStats";

  export default {
    components: {
      OverallStats,
      Tweets,
      Tags,
      SentimentMap,
    },
    data() {
      return {
        timer: "",
        showTweets: true
      }
    },
    methods: {
      scrapeTags() {
        const path = 'http://localhost:5000/crontab/twitter'; //window.location.origin + `/api/tags`
        axios.get(path)
          .then(response => {
            console.log("scrape tweets task: " + JSON.stringify(response.data));
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted: function () {
      // this.scrapeTags();
      // this.timer = setInterval(this.scrapeTags, 10000);
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
