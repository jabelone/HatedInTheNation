<template>
  <div>
    <div class="row">
      <div class="col s12 m3">
        <p>Random number from backend: {{ randomNumber }}</p>
      </div>
      <div class="col s12 m9">
        <tweets/>
      </div>
    </div>
  </div>
</template>

<script>
  import Tweets from './Tweets'
  import axios from 'axios'

  export default {
    components: {
      Tweets,
    },
    data() {
      return {
        randomNumber: 0
      }
    },
    methods: {
      getRandom() {
        // this.randomNumber = this.getRandomInt(1, 100)
        this.randomNumber = this.getRandomFromBackend();
      },
      getRandomFromBackend() {
        const path = `https://hatedinthenation.com/api/random`;
        axios.get(path)
          .then(response => {
            this.randomNumber = response.data.randomNumber;
          })
          .catch(error => {
            console.log(error);
          })
      }
    },
    created() {
      this.getRandom();

      setInterval(function () {
        this.randomNumber--;
        if (this.randomNumber <= 0) {this.randomNumber=0;}
      }.bind(this), 1000);

    }
  }
</script>
