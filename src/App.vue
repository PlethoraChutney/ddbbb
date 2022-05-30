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

  <div id="rules-holder" class="holder">
    <h2>Rules</h2>
    <p>There are always a few rules!</p>
    <h3>You must:</h3>
    <ul>
      <li>Have fun</li>
      <li>Be nice</li>
      <li>Invite anyone you think would enjoy this and get along</li>
    </ul>
    <hr>
    <h3>You are encouraged to:</h3>
    <ul>
      <li>Ride a bike or scooter or other person-powered vehicle</li>
      <li>Come to as many or few bars as you like (do not feel obligated to come to all of them!)</li>
      <li>Drink whatever you want, alcohol or no</li>
    </ul>
    <hr>
    <h3>You may <em>not</em>:</h3>
    <ul>
      <li>
        Drink and drive. If you're planning on having more than one (1) beer,
        do not drive. I don't care what you think your tolerance is.
      </li>
    </ul>
  </div>

  <div id="comments-holder" class="holder">
    <h2>Discussion</h2>
    <NewComment
      @post-new-comment="this.comments.push($event)"
    ></NewComment>
    <CommentBox
      v-for="(comment, index) in comments.reverse()"
      :key="index"
      :comment="comment"
    ></CommentBox>
    <p v-if="comments.length === 0">
      Looks like there aren't any comments yet.
    </p>
  </div>


</template>

<script>
import CommentBox from "./components/CommentBox.vue";
import NewComment from './components/NewComment.vue';

export function sendRequest(body, dest = '/api') {
    return fetch(dest, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(body)
    })
}

export default {
  name: 'App',
  components: {CommentBox, NewComment},
  data() {
    return {
      comments: []
    }
  },
  created() {
    this.getComments();
  },
  methods: {
    getComments() {
      sendRequest({'action': 'get_comments'})
        .then(request => request.json()).then(data => {
          this.comments = data;
        })
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
  width: 90%;
  max-width: 1000px;
  margin: auto;
}

#rules-holder ul{
  text-align: left;
  margin-top: 1rem;
}

#rules-holder h3 {
  margin: 0;
}

#rules-holder hr {
  width: 90%;
}

div.button {
  border: 1px solid black;
  border-radius: 5px;
  user-select: none;
  cursor: pointer;
  width: max-content;
  padding: 0 2rem;
  margin: 10px auto;
}

div.button.grey-out {
  cursor: default;
  border: 1px solid #CCCCCC;
  color: #CCCCCC;
}

@media screen and (max-width: 800px) {
  h1 {
  font-size: 4rem;
  }

  h2 {
    font-size: 3rem;
  }

  h3 {
    font-size: 2rem;
  }

  #page-header > h1 {
    font-size: 5rem;
  }

  .comment h4 {
    font-size: 12pt;
  }

  .comment p {
    font-size: 12pt;
  }
}

</style>
