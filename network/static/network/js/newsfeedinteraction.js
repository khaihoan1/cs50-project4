likeInteracationCreateButtons = document.querySelectorAll('.can-like');
likeInteracationCreateButtons.forEach(element => {
    element.addEventListener('click', addLikeHandler); 
});
likeInteractionRemoveButton = document.querySelectorAll('.like-interaction-clicked');
likeInteractionRemoveButton.forEach(element => {
    element.addEventListener('click', removeLikeHandler)
})
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addLikeHandler() {
    let postId = this.parentNode.parentNode.querySelector('input').value; // input -> postID
    let isLike = this.classList.contains("is-like");
    let likeOrDislike = isLike ? "like" : "dislike";
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", `/interaction/${postId}/${likeOrDislike}`, true);
    xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    data = JSON.stringify({
        "is_like": isLike,
    })  ;
    xhttp.send(data);
    var buttonBeingClicked = this;
    xhttp.onload = function() {
        res = JSON.parse(this.response);
        buttonBeingClicked.classList.add('like-interaction-clicked');
        buttonBeingClicked.classList.remove('can-like');
        if (res['data']['is_like']) {
            buttonBeingClicked.classList.add('post_like_already');
        } else {
            buttonBeingClicked.classList.add('post_dislike_already');
        }
        buttonBeingClicked.parentNode.children[0].innerText = res['data']['like_count_updated'];
        twin = buttonBeingClicked.parentNode.parentNode.querySelector('.can-like');
        twin.classList.remove('.can-like');
        twin.classList.add('like-cannot-click');
        buttonBeingClicked.removeEventListener('click', addLikeHandler);
        buttonBeingClicked.addEventListener('click', removeLikeHandler)
    }
}

function removeLikeHandler() {
    let userId = document.getElementById('user-id').value;
    let postId = this.parentNode.parentNode.querySelector('input').value; // input -> postID
    let isLike = this.classList.contains("is-like");
    let likeOrDislike = isLike ? "like" : "dislike";
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", `/interaction/${postId}/${likeOrDislike}/${userId}`, true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.send();
    var buttonBeingClicked = this;
    xhttp.onload = function() {
        buttonBeingClicked.classList.add('can-like');
        buttonBeingClicked.classList.remove('like-interaction-clicked');
        if (isLike) {
            buttonBeingClicked.classList.remove('post_like_already');
        } else {
            buttonBeingClicked.classList.remove('post_dislike_already');
        }
        currentCount = parseInt(buttonBeingClicked.parentNode.children[0].innerText);
        buttonBeingClicked.parentNode.children[0].innerText = currentCount - 1;
        twin = buttonBeingClicked.parentNode.parentNode.querySelector('.like-cannot-click');
        twin.classList.remove('like-cannot-click');
        twin.classList.add('.can-like');
        buttonBeingClicked.removeEventListener('click', removeLikeHandler);
        buttonBeingClicked.addEventListener('click', addLikeHandler);
    }
} 