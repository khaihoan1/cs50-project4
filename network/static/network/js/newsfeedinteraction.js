newFeed = document.querySelectorAll('.can-like');
newFeed.forEach(element => {
    element.onclick = function() {
        postId = this.parentNode.parentNode.querySelector('input').value;
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", `/interaction/${postId}/like`, true);
        xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        data = JSON.stringify({
            "is_like": this.classList.contains("like-button"),
        })  ;
        xhttp.send(data);
        xhttp.onload = function() {
            response = JSON.parse(this.response);
        }
    }
});

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

function ajaxLike(postId){

};