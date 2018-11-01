<template>
  <div id="home-container">
    <div class="z-depth-1" id="leftBar">
      <h4>Unpopularity <i class="material-icons title-icon">trending_downward</i></h4>
      <tags/>
      <h4>Overall Stats <i class="material-icons title-icon">equalizer</i></h4>
      <overall-stats/>
    </div>
    <div class="" id="rightContainer">
      <div id="titles" class="">
        <h4 v-on:click="showTweets = 0" v-bind:class="{ activetab: showTweets !== 0}"
            class="waves-effect waves-light tweets-and-map">Show Tweets</h4>
        <h4 class="waves-effect waves-light tweets-and-map">&nbsp;|&nbsp;</h4>
        <h4 v-on:click="showTweets = 1" v-bind:class="{ activetab: showTweets !== 1 }"
            class="waves-effect waves-light tweets-and-map">State Breakdown</h4>
        <h4 class="waves-effect waves-light tweets-and-map">&nbsp;|&nbsp;</h4>
        <h4 v-on:click="showTweets = 2" v-bind:class="{ activetab: showTweets !== 2 }"
            class="waves-effect waves-light tweets-and-map">More Stats</h4>
      </div>

      <transition name="fade-tweets">
        <tweets v-if="showTweets === 0"/>
      </transition>

      <transition name="fade">
        <sentiment-map v-if="showTweets === 1"/>
      </transition>

      <transition name="fade">
        <all-stats v-if="showTweets === 2"/>
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
  import AllStats from "./AllStats";

  export default {
    components: {
      AllStats,
      OverallStats,
      Tweets,
      Tags,
      SentimentMap,

    },
    data() {
      return {
        refresh: 10000,
        enableScraping: false,
        timer: "",
        showTweets: 1,
        scrapes: 0,
      }
    },
    methods: {
      scrapeTags() {
        this.scrapes++;

        const path = window.location.origin + `/crontab/twitter`;
        axios.get(path)
          .then(response => {
            if (response.data.success) {
              console.log("Scraped tweets successfully.");
            } else {
              console.log("Scraped tweets unsuccessfully.");
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted: function () {
      var elems = document.querySelectorAll('.modal');
      var instances = M.Modal.init(elems, {});

      if (this.enableScraping) {
        this.scrapeTags();
        this.timer = setInterval(this.scrapeTags, this.refresh);
      }
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
