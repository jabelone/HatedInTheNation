<template>
  <div>
    <table id="data_table" class="highlight striped">
      <thead>
      <tr>
        <th>Username</th>
        <th>Tweet</th>
        <th>Sentiment</th>
        <th>Likes</th>
        <th>Retweets</th>
        <th>Location</th>
      </tr>
      </thead>

      <tbody>
      <tr v-for="tweet in tweets" :key="tweet.snowflake">
        <td>{{tweet.user}}</td>
        <td>{{tweet.text}}</td>
        <td>{{tweet.sentiment}}%</td>
        <td>{{tweet.likes}}</td>
        <td>{{tweet.retweets}}</td>
        <td>{{tweet.state}}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Tweets',
    data() {
      return {
        tweets: []
      }
    },
    methods: {
      getTweets() {
        this.tweets = this.getTweetsFromBackend()
      },
      getTweetsFromBackend() {
        const path = window.location.origin + `/api/tweets`;
        axios.get(path)
          .then(response => {
            this.tweets = response.data.tweets;

            // this clever trick causes the table init code to run after the next frame is rendered. If we do it
            // straight away the dom hasn't been updated yet so it won't be initialised properly.
            setTimeout(function () {
              $.fn.dataTable.ext.classes.sPageButton = 'table-buttons waves-effect waves-light btn blue white-text';

              this.table = $('#data_table').DataTable({
                "lengthChange": true,
                "searching": true,
                "pageLength": 8,
                "paging": true,
                "order": [[2, 'asc']],
              });
            }, 0);
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted: function () {
      this.getTweets()
    }
  }
</script>
