commenntShowButton = document.querySelectorAll('.comment-show-button');
for (button of commenntShowButton) {
    button.onclick = function(){
        let postId = this.parentNode.parentNode.querySelector('input').value;
        hr = document.querySelector(`#hr-${postId}`);
        timer = document.querySelector(`#timer-roll-${postId}`);
        console.log(timer);
        hr.style.display = "block";
        timer.style.display = "block";
        var xhttp = new XMLHttpRequest();
    }
}