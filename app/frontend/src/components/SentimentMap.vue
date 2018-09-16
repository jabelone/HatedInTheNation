<template>
  <div id="mapid"></div>
</template>

<script>
  export default {
    name: 'SentimentMap',
    data() {
      return {
        map: "",
        state: {
          qld: "",
          nsw: "",
          vic: "",
          act: "",
          tas: "",
          sa: "",
          nt: "",
          wa: ""
        }
      }
    },
    methods: {},
    mounted() {
      // Init a leaflet js map and center on Australia
      this.map = L.map('mapid').setView([-27.532239, 134.597291], 5);
      L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 14,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiamFiZWxvbmUiLCJhIjoiY2pjZDVyYjBhMDl5ZjJxbXQ2Y21nbW83NyJ9.GmU38VLHRzMb17bZMEarDg'
      }).addTo(this.map);

      // Because we're using vue we need to give it a sec to render then tell it to invalidate the container's size
      let that = this;
      setTimeout(function () {
        that.map.invalidateSize();
      }, 2000);
      //
      let content = "<h5>Queensland</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.qld = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-20.701750, 145.362081]).setContent(content).openOn(this.map);

      content = "<h5>New South Wales</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.nsw = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-30.583624, 146.536988]).setContent(content).openOn(this.map);

      content = "<h5>A.C.T.</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.act = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-35.438815, 148.961420]).setContent(content).openOn(this.map);

      content = "<h5>Victoria</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.vic = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-35.748212, 142.768837]).setContent(content).openOn(this.map);

      content = "<h5>Tasmania</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.tas = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-42.720286, 146.639640]).setContent(content).openOn(this.map);

      content = "<h5>South Australia</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.sa = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-32.377240, 135.045214]).setContent(content).openOn(this.map);

      content = "<h5>Northern Territory</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.nt = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-18.100700, 133.423292]).setContent(content).openOn(this.map);

      content = "<h5>Western Australia</h5><p>@BillyShort: 67%</p><p>@ScoMo: 54%</p><p>@PaulinePantsdown</p>";
      this.state.wa = L.popup({autoClose: false, closeButton: false, closeOnClick: false}).setLatLng([-24.974424, 121.603931]).setContent(content).openOn(this.map);
    }
  }
</script>
