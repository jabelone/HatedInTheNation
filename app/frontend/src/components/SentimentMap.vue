<template>
  <div>
    <div id="loader">
      <div class="progress red">
        <div class="indeterminate red lighten-4"></div>
      </div>
    </div>
    <div id="mapid"></div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'SentimentMap',
    data() {
      return {
        refresh: 10000,
        centerCoords: [-27.532239, 134.597291],
        sentiment: "",
        time: "",
        map: "",
        state: {},
        states: [
          ["QLD", [-22.701750, 145.362081]],
          ["NSW", [-30.583624, 146.536988]],
          ["VIC", [-36.748212, 141.768837]],
          ["ACT", [-35.438815, 150.961420]],
          ["TAS", [-42.720286, 146.639640]],
          ["NT", [-22.717294, 134.583124]],
          ["SA", [-32.377240, 133.583124]],
          ["WA", [-24.974424, 121.603931]],
        ]
      }

    },
    methods: {
      getSentimentFromBackend() {
        const path = window.location.origin + `/api/sentiment`;
        axios.get(path)
          .then(response => {
            this.sentiment = response.data;
            this.updateMap();
            document.getElementById("loader").classList.add("hidden");
          })
          .catch(error => {
            console.log(error);
          });
      },

      updateMap() {
        // Loop through the list of states and edit the popup for each
        Object.keys(this.sentiment.states).forEach((key) => {
          let sentimentstate = this.sentiment.states[key];
          let mapstate = this.state[key];

          let headerContent = `<ul class=\"collection with-header no-padding leaflet-stat-box\">` +
            `<h5 class=\"leaflet-stat-box-title\">${key}</h5>\n`;
          let headerFooter = `</ul>`;

          let content = headerContent;
          let position = 0;

          sentimentstate.tags.forEach((tag) => {
            position++;
            let sentiment = tag[1];
            tag = tag[0].displayname;

            content += `        <li class=\"collection-item no-padding\">\n` +
              `            <div class=\"collection-header\"><b>#${position}</b> ${tag}: ${sentiment}%</div>\n</li>`
          });

          mapstate.content = content + headerFooter;
          mapstate.marker.setContent(mapstate.content);
        });

        this.map.setView(this.centerCoords, 5);
        this.map.invalidateSize();
      }
    },
    mounted() {
      document.getElementById("loader").classList.remove("hidden");
      // Init a leaflet js map and center on Australia
      this.map = L.map('mapid').setView(this.centerCoords, 5);
      L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 14,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiamFiZWxvbmUiLCJhIjoiY2pjZDVyYjBhMDl5ZjJxbXQ2Y21nbW83NyJ9.GmU38VLHRzMb17bZMEarDg'
      }).addTo(this.map);

      // Placeholder text to show before data is fetched from backend.
      let content = "<h5>Fetching statistics...</h5>";

      // Loop through the list of states and make a popup for each, saving to vue.js
      this.states.forEach((item) => {
        let stateName = item[0];
        let coords = item[1];

        let marker = L.popup({
          autoClose: false,
          closeButton: false,
          closeOnClick: false
        }).setLatLng(coords).setContent(content);

        this.map.addLayer(marker);

        this.state[stateName] = {
          "marker": marker,
          "content": content,
        };
      });

      this.timer = setInterval(this.getSentimentFromBackend, this.refresh);
      this.getSentimentFromBackend();
    },
  }
</script>
