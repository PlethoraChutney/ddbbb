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
:class="{'grey-out': commentText.length === 0 || commenterName.length === 0}"
@click="sendComment()"
>
    Post
</div>
</template>

<script>

export default {
    'name': 'NewComment',
    data() {
        return {
            commenterName: '',
            commentText: ''
        }
    },
    props: {
        'year': String
    },
    methods: {
        sendComment() {
            let comment = {
                'author': this.commenterName,
                'content': this.commentText.split('\n\n')
            }

            if (this.commentText.length > 0 && comment.author.length > 0) {
                this.$emit('postNewComment', comment);
                this.commentText = '';
            }
        }
    },
    watch: {
        commenterName(value) {
            if (value === 'ddbbbAdmin') {
                this.$emit('isAdmin');
            }
        }
    },
    emits: [
        'postNewComment',
        'isAdmin'
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