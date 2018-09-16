<template>
  <div class="tags">
    <ul class="collection">
      <li v-for="tag in tags" :key="tag.tag" class="collection-item avatar">
        <img :src="tag.image" alt="" class="circle">
        <span class="title">{{tag.displayname}}</span>
        <p>Username: {{tag.tag}}</p>
        <div style="max-width: 90%; margin: 0 auto;">
          <a :href="'http://twitter.com/' + tag.tag" target="_blank" class="left">Profile<i class="material-icons right">link</i></a>
          <a href="#" :onclick="'$(\'#data_table\').DataTable().search(\'' + tag.tag + '\').draw();'" class="right"> Filter &nbsp;&nbsp;&nbsp;➡</a>
        </div>
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
        tags: [],
        timer: ''
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
