<template>
  <div class="tags">
    <ul class="collection z-depth-1">
      <li v-for="tag in tags" :key="tag.tag" class="collection-item avatar avatartag">
        <img :src="tag.image" alt="" class="circle z-depth-2">
        <span class="title left"><b>#{{tag.place}} - {{tag.displayname}}</b></span><br>
        <div class="tagbox">
          <a :href="'http://twitter.com/' + tag.tag" target="_blank" class="left">Profile</a>
          <span class="left">&nbsp; | &nbsp;</span>
          <a href="#" :onclick="'$(\'#data_table\').DataTable().search(\'' + tag.tag + '\').draw();'" class="left">See
            Tweets &nbsp;&nbsp;&nbsp;➡</a>
        </div>
        <span class="left">Avg Sentiment: {{tag.average}}%</span><br>
      </li>
    </ul>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Tags',
    data() {
      return {
        refresh: 5000,
        tags: [
          {
            "average": 0,
            "count": 0,
            "displayname": "",
            "image": "/static/images/avatar.png",
            "max": 0,
            "min": 0,
            "place": 0,
            "tag": ""
          },
          {
            "average": 0,
            "count": 0,
            "displayname": "",
            "image": "/static/images/avatar.png",
            "max": 0,
            "min": 0,
            "place": 0,
            "tag": ""
          },
          {
            "average": 0,
            "count": 0,
            "displayname": "",
            "image": "/static/images/avatar.png",
            "max": 0,
            "min": 0,
            "place": 0,
            "tag": ""
          },
          {
            "average": 0,
            "count": 0,
            "displayname": "",
            "image": "/static/images/avatar.png",
            "max": 0,
            "min": 0,
            "place": 0,
            "tag": ""
          }
        ]
        ,
        timer: ''
      }
    },
    methods: {
      getTagsFromBackend() {
        const path = window.location.origin + `/api/tags`;
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
      this.timer = setInterval(this.getTagsFromBackend, this.refresh);
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>
