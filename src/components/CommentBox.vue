<template>
    <div
    class="comment"
    :class="{'collapsed': isCollapsed}"
    @click="tryDelete()"
    >
        <div class="author">
            <h4>{{this.comment.author}}</h4>
            <p>{{ this.comment.parsed_timestamp }}</p>
        </div>
        <hr>
        <div class="content">
            <p
            v-for="(para, index) in this.comment.content"
            :key="index"
            >{{para}}</p>
        </div>
    </div>
</template>

<script>
export default {
    'name': 'CommentBox',
    props: {
        'comment': Object,
        'isAdmin': Boolean
    },
    data() {
        return {
            isCollapsed: false
        }
    },
    methods: {
        tryDelete() {
            if (this.isAdmin) {
                this.$emit('delete-comment', this.comment)
            }
        }
    },
    emits: ['delete-comment']
}
</script>

<style scoped>
.comment {
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    border: 1px solid #AAAAAA;
    border-radius: 10px;
    margin-bottom: 10px;
}

.comment h4 {
    margin: 0;
    color: #AAAAAA;
    overflow-wrap: break-word;
}

.comment > .author {
    width: 20%;
}

.comment > .author > p {
    font-size: 1rem;
    opacity: 0.75;
    padding: 0;
    margin: 0;
}

.comment > .content {
    width: 70%;
    white-space: pre-wrap;
}

hr {
    visibility: hidden;
    display: none;
}

@media screen and (max-width: 1000px) {

    .comment {
        flex-direction: column;
    }

    .comment .author {
        width: max-content;
        max-width: 100%;
        margin-bottom: -0.5rem;
    }

    .author p {
        color: #AAAAAA;
    }

    .comment h4 {
    font-size: 12pt;
    }

    .comment p {
    font-size: 12pt;
    width: 100%;
    }

    hr {
        visibility: unset;
        display: unset;
        border: none;
        background-color: #AAAAAA;
        height: 1px;
        width: 90%;
        margin-bottom: -0.5rem;
    }
}
</style>