<template>
  <div>
    <div id="mapid"></div>
  </div>
</template>

<script>
  export default {
    name: 'SentimentMap',
    data() {
      return {
        map: ""
      }
    },
    methods: {
    },
    mounted() {
      this.map = L.map('mapid').setView([-27.532239, 134.597291], 5);
      L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 14,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiamFiZWxvbmUiLCJhIjoiY2pjZDVyYjBhMDl5ZjJxbXQ2Y21nbW83NyJ9.GmU38VLHRzMb17bZMEarDg'
      }).addTo(this.map);
      let that = this;
      setTimeout(function(){that.map.invalidateSize();},100)
    }
  }
</script>
