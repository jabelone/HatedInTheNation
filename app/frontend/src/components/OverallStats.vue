<template>
  <div class="tags">
    <ul class="collection">
      <li class="collection-item">
        <span><b>National Sentiment:</b></span>
        <span v-if="this.data.national_sentiment < 20" class="title"> Very Low ({{this.data.national_sentiment}}%)</span>
        <span v-else-if="this.data.national_sentiment < 40" class="title">Low ({{this.data.national_sentiment}}%)</span>
        <span v-else-if="this.data.national_sentiment < 60" class="title">Average ({{this.data.national_sentiment}}%)</span>
        <span v-else-if="this.data.national_sentiment < 80" class="title">High ({{this.data.national_sentiment}}%)</span>
        <span v-else="this.data.national_sentiment" class="title">Very High ({{this.data.national_sentiment}}%)</span>
      </li>

      <li class="collection-item">
        <span><b>Highest Sentiment:</b> {{this.data.highest_sentiment.state}}</span>
        <span v-if="this.data.highest_sentiment.value < 20" class="title"> (Very Low {{this.data.highest_sentiment.value}}%)</span>
        <span v-else-if="this.data.highest_sentiment.value < 40" class="title">(Low {{this.data.highest_sentiment.value}}%)</span>
        <span v-else-if="this.data.highest_sentiment.value < 60" class="title">(Average {{this.data.highest_sentiment.value}}%)</span>
        <span v-else-if="this.data.highest_sentiment.value < 80" class="title">(High {{this.data.highest_sentiment.value}}%)</span>
        <span v-else="this.data.highest_sentiment.value" class="title">(Very High {{this.data.highest_sentiment.value}}%)</span>
      </li>

      <li class="collection-item">
        <span><b>Lowest Sentiment:</b> {{this.data.lowest_sentiment.state}}</span>
        <span v-if="this.data.lowest_sentiment.value < 20" class="title">(Very Low {{this.data.lowest_sentiment.value}}%)</span>
        <span v-else-if="this.data.lowest_sentiment.value < 40" class="title">(Low {{this.data.lowest_sentiment.value}}%)</span>
        <span v-else-if="this.data.lowest_sentiment.value < 60" class="title">(Average {{this.data.lowest_sentiment.value}}%)</span>
        <span v-else-if="this.data.lowest_sentiment.value < 80" class="title">(High {{this.data.lowest_sentiment.value}}%)</span>
        <span v-else="this.data.lowest_sentiment.value" class="title">(Very High {{this.data.lowest_sentiment.value}}%)</span>
      </li>

      <li class="collection-item">
        <span><b>Scanned Tweets:</b> {{this.data.total_tweets}}</span>
      </li>
    </ul>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'OverallStats',
    data() {
      return {
        tags: [],
        timer: '',
        data: {
          national_sentiment: 50,
          total_tweets: 510,
          lowest_sentiment: {
            state: "QLD",
            value: 37
          },
          highest_sentiment: {
            state: "NSW",
            value: 76
          },
        }
      }
    },
    methods: {
      getTagsFromBackend() {
        const path = 'http://localhost:5000/api/tags'; //window.location.origin + `/api/tags`
        axios.get(path)
          .then(response => {
            this.tags = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted: function () {
      this.getTagsFromBackend();
      this.timer = setInterval(this.getTagsFromBackend, 2000);
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
