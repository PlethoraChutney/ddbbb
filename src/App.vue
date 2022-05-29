<template>
  <div id="page-header">
    <h1>DDBBB VI</h1>
    <p style="margin-top: 0;">Drop-in Drop-out Birthday Beer Bike Seven</p>
  </div>

  <div id="map-holder" class="holder">
    <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1mq2U0ZQVUbaGDvMJXL1dT2Ay1FZrVYY&ehbc=2E312F"
      width="100%"
      height="820"
    ></iframe>
  </div>

  <div id="comments-holder" class="holder">
    <h2>Discussion</h2>
    <CommentBox
      v-for="(comment, index) in comments"
      :key="index"
      :comment="comment"
    ></CommentBox>
  </div>


</template>

<script>
import CommentBox from "./components/CommentBox.vue";

export default {
  name: 'App',
  components: {CommentBox},
  data() {
    return {
      comments: [
        {
          'author': 'Rich',
          'content': ['Hi everyone. Time for another year of riding around to celebrate my birth.']
        },
        {
          'author': 'Rich',
          'content': ['As always, there are a few rules.']
        },
        {
          'author': 'Rich',
          'content': ['You must:', 'Have fun.', 'Be nice', 'Invite anyone you think would enjoy this, and that I \'d like.']
        },
        {
          'author': 'Rich',
          'content': ['You are encouraged to:', 'Ride a bike or scooter or other person-powered vehicle (if you wanna bus or lyft or w/e go for it)', 'Come to as many or few bars as you like (don\'t feel obligated to be there all day! It\'s...a lot)', 'Drink whatever you want. It doesn\'t have to be alcohol!']
        },
        {
          'author': 'Rich',
          'content': ['You may NOT:', 'Drink and drive. If you\'re planning on having more than one beer don\'t drive!!! I don\'t care what your tolerance is!']
        }
      ]
    }
  }
}
</script>

<style>
@font-face {
  font-family: 'Chillax-Regular';
  src: url('@/assets/fonts/Chillax-Regular.woff2') format('woff2'),
       url('@/assets/fonts/Chillax-Regular.woff') format('woff'),
       url('@/assets/fonts/Chillax-Regular.ttf') format('truetype');
       font-weight: 400;
       font-display: swap;
       font-style: normal;
}

@font-face {
  font-family: 'Sentient-Regular';
  src: url('@/assets/fonts/Sentient-Regular.woff2') format('woff2'),
       url('@/assets/fonts/Sentient-Regular.woff') format('woff'),
       url('@/assets/fonts/Sentient-Regular.ttf') format('truetype');
       font-weight: 400;
       font-display: swap;
       font-style: normal;
}

@font-face {
  font-family: 'Sentient-Bold';
  src: url('@/assets/fonts/Sentient-Bold.woff2') format('woff2'),
       url('@/assets/fonts/Sentient-Bold.woff') format('woff'),
       url('@/assets/fonts/Sentient-Bold.ttf') format('truetype');
       font-weight: 700;
       font-display: swap;
       font-style: normal;
}

#app {
  font-family: Chillax-Regular, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  padding: 0;
  margin: 0;
  font-size: 18pt;
}

#page-header > h1 {
  font-size: 120pt;
  margin: 0;
  padding: 0;
}

h1, h2, h3, h4 {
  font-family: Sentient-Bold, serif;
  margin-bottom: 0;
}

h1 {
  font-size: 5rem;
}

h2 {
  font-size: 4rem;
}

h3 {
  font-size: 3rem;
}

iframe {
  border: none;
  margin-top: -60px;
}

#map-holder {
  overflow: hidden;
}

.holder {
  width: 100%;
  max-width: 1000px;
  margin: auto;
}

</style>
