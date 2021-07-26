commentForm = `<div class="row" id="comment-area-{{ post.id}}">
<div class="col-1 avatar-post-form-container">
    <img class="avatar-post-comment-form rounded-circle"
    src="{% if user.avatar_pic %}{{ user.avatar_pic.url }}{% else %}/media/user.svg{% endif %}">
</div>
<div class="col-11 comment-div">
    <div class="comment-container">
    <span><b>khaihoan1</b></span>
    <span class="comment-content"></span>
    </div>
</div>
</div>`
commenntShowButton = document.querySelectorAll('.comment-show-button');
for (button of commenntShowButton) {
    button.addEventListener('click', comment);
}
textAreaComments = document.querySelectorAll('.text-area-comment');
for (textAreaComment of textAreaComments) {
    textAreaComment.addEventListener('keyup', commentFormKeyUpHandler)
}

// This function handler the loader icon (spinner), deal with first-time rendering
// for first Ajax call to get comments, then detach the function from the comment icon.
// That means the comment icon button doesn't have onclick event anymore.
function comment(){
    comment_icon = this;
    let postId = this.parentNode.parentNode.querySelector('input').value;
    hr = document.querySelector(`#hr-${postId}`);
    timer_div = document.querySelector(`#timer-roll-${postId}`);
    timer = 0;
    var timer_interval = setInterval(()=>{timer += 100}, 100);
    hr.style.display = "block";
    timer_div.style.display = "block";
    var xhttp = new XMLHttpRequest();
    url = `/interaction/${postId}/comments`;
    xhttp.open('GET', url);
    xhttp.send();
    xhttp.onload = function() {
        res = JSON.parse(this.response);
        var response_interval = setInterval(render_comment, 100);
        function render_comment(){
            if (timer >= 1000) {
                clearInterval(timer_interval);
                clearInterval(response_interval);
                comments = res["results"];
                newCommentsId = [];

                str = makeMainCommentsString(newCommentsId, comments, postId);
                if (res['next']) {
                    str += `
                    <div class="load-more-comment row" id="load-more-comment-${postId}" next="${res['next']}" postId="${postId}">
                        <span class="hover-underline">
                            <i class="fas fa-home link-item"></i>Load more
                        </span>
                    </div>
                    `
                }
                timer_div.insertAdjacentHTML("beforebegin", str);
                loadMoreCommentButton = document.getElementById(`load-more-comment-${postId}`);
                if (loadMoreCommentButton){
                    loadMoreCommentButton.onclick = loadMoreComment;
                }
                timer_div.style.display = "none";
                commentArea = document.getElementById(`comment-area-${postId}`);
                commentArea.classList.remove("post-comment-form");
                textAreaComment = document.getElementById(`text-area-comment-${postId}`);
                textAreaComment.style.height = '35px';
                comment_icon.removeEventListener('click', comment);
                comment_icon.onclick = function() {
                    textAreaComment.focus();
                };
                attachEventForReplyButtons(newCommentsId);
            }
        }
    }
}

function commentFormKeyUpHandler(ev){
    if (!this.value) {
        // Resize the comment textarea when empty
        this.style.height = '35px'; 
        return;
    } else {
        if (ev.key == 'Enter') {
            console.log('ok');
        }
    }
}

// function showReplyForm(){
//     // Check if there are replies of the main comment, call the function that show them.
//     console.log('hihi');
//     if (this.parentNode.querySelector(".load-more-reply")) {
//         console.log(this.parentNode.querySelector(".load-more-reply"));
//     }
// }

function loadMoreReplies() {
    loadMoreRepliesButton = this;
    commentId = this.getAttribute('next');
    url = this.getAttribute("next");
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', url);
    xhttp.send();
    xhttp.onload = function() {
        res = JSON.parse(this.response);
        newRepliesString = makeRepliesString(res['results']);
        loadMoreRepliesButton.insertAdjacentHTML('beforebegin', newRepliesString);
        if (res['next']) {
            loadMoreRepliesButton.setAttribute('next', res['next']);
        } else {
            loadMoreRepliesButton.remove();
        }
    }
}

function firstLoadReplies() {
    avatarUrl = document.getElementById('user-avatar').getAttribute('src');
    postId = this.getAttribute('postId');
    commentId = this.getAttribute('commentId');
    loadRepliesButton = document.getElementById(`load-more-reply-button-${commentId}`);
    beClicked = this;
    beClicked.removeEventListener('click', firstLoadReplies);
    url = `/interaction/${postId}/subcomments/${commentId}`;
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', url);
    xhttp.send();
    xhttp.onload = function() {
        res = JSON.parse(this.response);
        newRepliesString = makeRepliesString(res['results']);

        // Insert reply form
        beClicked.parentNode.insertAdjacentHTML('beforeend', `
        <div class="row">
            <div class="col-1 avatar-post-form-container">
                <img class="avatar-post-comment-form rounded-circle"
                src="${avatarUrl}">
            </div>
            <div class="col-11 comment-div">
                <form class="comment-form">
                    <textarea class="text-area-input text-area-comment"
                    placeholder="Answer this comment..."></textarea>
                    <input type="hidden" name="post-parent" postId="${postId}" commentId="${commentId}">
                </form>
            </div>
        </div>`);
        // Add event for reply form
        replyForm = beClicked.parentNode.getElementsByTagName('TEXTAREA')[0];
        replyForm.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
        // replyForm.setAttribute('style', 'px;overflow-y:hidden;');
        replyForm.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
            if (!this.value) {
                this.style.height = '35px';
            }
          })
        replyForm.onkeyup = makeReply;
        // Onclick handle, first time and only once
        if (beClicked.innerHTML == 'Reply') {
            if (beClicked.nextElementSibling) {
                beClicked.nextElementSibling.removeEventListener('click', firstLoadReplies);
            }
            beClicked.insertAdjacentHTML('afterend', newRepliesString);
            beClicked.onclick = function() {
                replyForm.focus();
            }
        } else {
            beClicked.previousElementSibling.removeEventListener('click', firstLoadReplies);
            beClicked.previousElementSibling.onclick = () => {
                replyForm.focus();
            }
            beClicked.insertAdjacentHTML('beforebegin', newRepliesString);
        }
        if (loadRepliesButton) {
            if (res['next']) {
                loadRepliesButton.innerHTML = "View more replies";
                loadRepliesButton.setAttribute('next', res['next']);
                loadRepliesButton.onclick = loadMoreReplies;
            } else {
                loadRepliesButton.remove();
            }
        }
    }
}

function makeRepliesString(arrayReplies) {
    subComments = arrayReplies.map(subComment => { 
        return `
            <div>                        
            <div class="row each-comment reply" id="reply-area-{{ post.id}}">
                <div class="col-1 avatar-post-form-container">
                    <img class="avatar-post-comment-form rounded-circle"
                    src="${subComment["avatar_pic"] ? subComment["avatar_pic"] : "/media/user.svg"}">
                </div>
                <div class="col-11 comment-div">
                    <div class="comment-container">
                        <span><b>${subComment['owner']['username']}</b></span>
                        <span class="comment-content">${subComment['content']}</span>
                    </div>
                </div>
            </div>
        </div>                        
        `
    });
    return subComments.join("");
}

function makeMainCommentsString(commentIds, arrayComments, postId) {
    comments = arrayComments.map(comment => {
        commentIds.push(comment['id']);
        return `            
            <div class="row each-comment">
                <div class="col-1 avatar-post-form-container">
                    <img class="avatar-post-comment-form rounded-circle"
                    src="${comment['avatar_pic'] ? comment['avatar_pic']:"/media/user.svg"}">
                </div>
                <div class="col-11 comment-div">
                    <div class="comment-container">
                        <span><b>${comment['owner']['username']}</b></span>
                        <span class="comment-content">${comment['content']}</span>
                    </div>
                    <span class="reply-button hover-underline" id="reply-button-${comment['id']}" commentId=${comment['id']} postId=${postId}>Reply</span>
                    ${comment['has_reply'] ? `<span commentId="${comment['id']}" postId=${postId}
                    class="load-more-reply hover-underline" id="load-more-reply-button-${comment['id']}"
                    >
                    <i class="fas fa-home link-item"></i>View reply</span>`:""}
                </div>
            </div>`
    });
    str = comments.join("");
    return str;
}

function loadMoreComment() {
    loadMoreCommentButton = this;
    postId = this.getAttribute('postId');
    url = this.getAttribute("next");
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', url);
    xhttp.send();
    xhttp.onload = function() {
        res = JSON.parse(this.response);
        console.log(res);
        commentIds = [];
        str = makeMainCommentsString(commentIds, res['results'], postId);
        loadMoreCommentButton.insertAdjacentHTML('beforebegin', str);
        attachEventForReplyButtons(commentIds);
        if (res['next']) {
            loadMoreCommentButton.setAttribute('next', res['next']);
        } else {
            loadMoreCommentButton.remove();
        }
    }
}
function attachEventForReplyButtons(newCommentsId) {
    newCommentsId.map(newCommentId => {
        replyButton = document.getElementById(`reply-button-${newCommentId}`);
        replyButton.addEventListener('click', firstLoadReplies);
        loadMoreRepliesButton = document.getElementById(`load-more-reply-button-${newCommentId}`);
        if (loadMoreRepliesButton) {
            loadMoreRepliesButton.addEventListener('click', firstLoadReplies);
        }
    })
}
function makeReply() {
    console/log('Making reply...');
};