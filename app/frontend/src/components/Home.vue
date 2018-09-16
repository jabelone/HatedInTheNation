<template>
  <div id="home-container">
      <div class="z-depth-1" id="leftBar">
        <h4>Overall Stats <i class="material-icons title-icon">equalizer</i></h4>
        <overall-stats/>
        <h4>Unpopularity <i class="material-icons title-icon">trending_upward</i></h4>
        <tags/>
        <p>The list is ranked from least to most popular and updates automatically every few seconds.</p>
      </div>
      <div class="" id="rightContainer">
        <div id="titles" class="">
          <h4 v-on:click="showTweets = true" v-bind:class="{ active: !showTweets }"
              class="waves-effect waves-light tweets-and-map">Show Tweets</h4>
          <h4 class="waves-effect waves-light tweets-and-map">&nbsp;|&nbsp;</h4>
          <h4 v-on:click="showTweets = false" v-bind:class="{ active: showTweets }"
              class="waves-effect waves-light tweets-and-map">State Breakdown</h4>
        </div>

        <transition name="fade">
          <tweets v-if="showTweets"/>
        </transition>

        <transition name="fade">
          <sentiment-map v-if="!showTweets"/>
        </transition>
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
        showTweets: false,
        scrapes: 0,
      }
    },
    methods: {
      scrapeTags() {
        this.scrapes++;

        if (this.scrapes > 20) {
          clearInterval(this.timer);
          alert("We've collected quite a few tweets since you've been on this page. To save server resources we will stop doing this untill you refresh the page.");
          return
        }

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
