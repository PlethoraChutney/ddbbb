<template>
    <div
    class="comment"
    :class="{'collapsed': isCollapsed}"
    @click="tryDelete()"
    >
        <div class="author">
            <h4>{{this.comment.author}}</h4>
        </div>
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
}

.comment > .author {
    width: 20%;
}

.comment > .content {
    width: 70%;
}
</style>