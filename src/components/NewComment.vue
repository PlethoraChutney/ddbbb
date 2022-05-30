<template>
<h3>Write a new comment</h3>
<div id="input-zone">
    <input
        type="text"
        v-model="commenterName"
        placeholder="Name"
    >
    <textarea
        cols="30"
        rows="2"
        placeholder="Comment"
        v-model="commentText"
    ></textarea>
</div>
<div class="button"
@click="sendComment()"
>
    Post
</div>
</template>

<script>
import { sendRequest } from "@/App.vue";

export default {
    'name': 'NewComment',
    data() {
        return {
            commenterName: null,
            commentText: null
        }
    },
    methods: {
        sendComment() {
            let comment = {
                'author': this.commenterName,
                'content': this.commentText.split('\n\n')
            }

            if (comment.content.length !== 0) {
                sendRequest({
                    'action': 'new_comment',
                    'comment': comment
                });

                this.$emit('postNewComment', comment);
                this.commentText = '';
            }
        }
    },
    emits: [
        'postNewComment'
    ]
}
</script>

<style scoped>

#input-zone {
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

#input-zone input {
    border: 1px solid #AAAAAA;
    font-family: Sentient-Bold, serif;
    width: 15%;
    padding: 1rem;
}

#input-zone textarea {
    width: 60%;
    padding: 1rem;
    font-family: unset;
    resize: none;
}

</style>