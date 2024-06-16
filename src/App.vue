<template>
  <div id="page-header">
    <h1 class="mondo">DDBBB {{ yearInfo.header_info.roman_numeral }}</h1>
    <p style="margin-top: 0;">Drop-in Drop-out Birthday Beer Bike {{ yearInfo.header_info.arabic_numeral }}</p>
    <h2>{{ yearInfo.header_info.date }}<sup>{{ yearInfo.header_info.cardinal }}</sup> {{ year }}</h2>
    <h2>Start at noon</h2>
  </div>

  <div id="map-holder" class="holder">
    <iframe
      :src="yearInfo.map_embed"
      width="100%"
      height="820"
    ></iframe>
  </div>

  <div id="rules-holder" class="holder">
    <h2 class="mondo">Rules</h2>
    <h3>You must:</h3>
    <ul>
      <li
      v-for="(rule, index) in yearInfo.rules.must"
      :key="index"
      >
        {{ rule }}
      </li>
    </ul>
    <hr>
    <h3>You are encouraged to:</h3>
    <ul>
      <li
      v-for="(rule, index) in yearInfo.rules.may"
      :key="index"
      >
        {{ rule }}
      </li>
    </ul>
    <hr>
    <h3>You may <em>not</em>:</h3>
    <ul>
      <li
      v-for="(rule, index) in yearInfo.rules.not"
      :key="index"
      >
        {{ rule }}
      </li>
    </ul>
  </div>

  <div id="comments-holder" class="holder">
    <h2>Discussion</h2>
    <NewComment
      @post-new-comment="newComment($event)"
      @is-admin="this.isAdmin = true"
    ></NewComment>
    <CommentBox
      v-for="(comment, index) in comments"
      :key="index"
      :comment="comment"
      :is-admin="isAdmin"
      @delete-comment="deleteComment($event)"
    ></CommentBox>
    <p v-if="comments.length === 0">
      Looks like there aren't any comments yet.
    </p>
  </div>


</template>

<script>
import CommentBox from "./components/CommentBox.vue";
import NewComment from './components/NewComment.vue';

import io from 'socket.io-client'

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
      year: '2023',
      yearInfo: {
        "year": null,
        "header_info": {
            "roman_numeral": null,
            "arabic_numeral": null,
            "date": null,
            "time": null
          },
          "rules": {
              "must": null,
              "may": null,
              "not": null
          },
          "map_embed": null
      },
      comments: [],
      isAdmin: false,
      socket: io('/')
    }
  },
  created() {
    this.setYear();
    this.getYearInfo();
    this.getComments();

    this.socket.on('write_to_log', msg => {
      console.log(msg.data);
    });

    const vm = this;
    this.socket.on('new_comment', function(data) {
      if (data.year == vm.year) {
        vm.comments.unshift(data.comment);
      }
    })
    this.socket.on('delete_comment', function(data) {
      if (data.year == vm.year) {
        vm.removeComment(data.comment);
      }
    })
  },
  computed: {
    commentTS() {
      let toReturn = [];
      this.comments.forEach(e => toReturn.push(e.timestamp));
      return toReturn;
    }
  },
  methods: {
    setYear() {
      this.year = window.location.href.match(/\/([0-9]{4})\//)[1];
    },
    getYearInfo() {
      sendRequest({'action': 'get_year_info', 'year': this.year})
        .then(request => request.json()).then(data => {
          Object.assign(this.yearInfo, data);
        })
    },
    getComments() {
      sendRequest({'action': 'get_comments', year: `${this.year}`})
        .then(request => request.json()).then(data => {
          this.comments = data.reverse();
        })
    },
    newComment(comment) {
      this.socket.emit('newComment', {"year": this.year, "comment": comment});
    },
    deleteComment(comment) {
      this.socket.emit('deleteComment', {"year": this.year, "comment": comment});
    },
    removeComment(comment) {
      let indexToRemove = this.commentTS.indexOf(comment.timestamp);
      if (indexToRemove != -1) {
        this.comments.splice(indexToRemove, 1);
      }
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
  display: grid;
  grid-template-areas: "header header" "map rules" "comments comments";
  grid-template-rows: max-content max-content max-content;
  grid-template-columns: 1fr 1fr;
}

#page-header {
  grid-area: header;
}

#page-header h2 {
  margin: 0;
}

.mondo {
  margin: 0;
  padding: 0;
}

h1.mondo {
  font-size: 160pt;
  line-height: 100%;
}

h2.mondo {
  font-size: 100pt;
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
  margin-top: -70px;
}

#map-holder {
  overflow: hidden;
  grid-area: map;
}

.holder {
  width: 90%;
  max-width: 1000px;
  margin: auto;
}

#rules-holder ul{
  text-align: left;
  margin-top: 1rem;
  grid-area: rules;
}

#rules-holder h3 {
  margin: 0;
}

#rules-holder hr {
  width: 90%;
}

#comments-holder {
  grid-area: comments;
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

@media screen and (max-width: 1000px) {

  #app {
    display: block;
  }

  h1 {
  font-size: 4rem;
  }

  h2 {
    font-size: 3rem;
  }

  h3 {
    font-size: 2rem;
  }

  h1.mondo {
    font-size: 5rem;
  }

  h2.mondo {
    font-size: 4rem;
  }
}

</style>
