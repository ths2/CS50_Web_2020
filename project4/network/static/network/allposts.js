document.addEventListener('DOMContentLoaded', function () {

    //check if an item was clicked
    var descendentes = document.querySelectorAll('#edit_post_button'); 
    for (var i = 0; i < descendentes.length; i++) {
        descendentes[i].addEventListener('click', function (e) {
            teste(this.parentElement);
            edit_post(this.parentElement);
        })
    }
    
    var postButtons= document.querySelectorAll('#post_json');
    for (var i = 0; i < postButtons.length; i++) {
        postButtons[i].addEventListener('click', function (e) {
            var edited_post = this.parentElement.parentElement.parentElement.children[3].children[0][0].value;
            var id_edited_post = this.parentElement.parentElement.parentElement.children[1].value;
            edit_postJson(edited_post, id_edited_post, this.parentElement.parentElement.parentElement);
        })
    }

    // Likes
    var likes = document.querySelectorAll('#likes');
    for (var i = 0; i < likes.length; i++) {
        likes[i].addEventListener('click', function (e) {
            var id_post = this.parentElement.parentElement.children[1].value;
            likes_js(id_post, 'l', this.parentElement);
        })
    }

    // Dislikes
    var dislikes = document.querySelectorAll('#dislikes');
    for (var i = 0; i < dislikes.length; i++) {
        dislikes[i].addEventListener('click', function (e) {
            var pos = dislikes[i];
            var id_post = this.parentElement.parentElement.children[1].value;
            likes_js(id_post, 'd', this.parentElement);
        })
    }

})


function edit_post(y) {
    var mortherDiv = y;

    var post_text = mortherDiv.children[0];
    var post_button = mortherDiv.children[2];
    var content_post_text = post_text.innerHTML;
    post_text.style.display = 'none'
    post_button.style.display = 'none'

    /////////
    var post_form = mortherDiv.children[3]
    var post_form_area = post_form.children[0].children[0];
    post_form_area.value = content_post_text;
    
}

function edit_post_return(y, post) {

    var u = y.getElementsByClassName('form_post');
    u[0].style.display = 'none'

    var mortherDiv = y;

    var post_text = mortherDiv.children[0];
    var post_button = mortherDiv.children[2];

    post_text.innerHTML = post;

    post_text.style.display = 'block'
    post_button.style.display = 'block'
    

}

function teste(t) {
    var u = t.getElementsByClassName('form_post');
    u[0].style.display = 'block'
}

function edit_postJson(editedPost, id, div) {

    fetch('/editpost', {
        method: 'PUT',
        body: JSON.stringify({
            id: id,
            editedPost: editedPost,
        })
    })
        .then(response => response.json())
        .then(result => {
            if(result['status'] == 201 ){
                edit_post_return(div, editedPost) 
            }

            // Print result
            console.log(result['status']);
        });
}

function likes_js(id, func, pos){
    fetch('/likes', {
        method: 'PUT',
        body: JSON.stringify({
            id: id,
            func: func
        })
    })
        .then(response => response.json())
        .then(result => {


            // Modify value like and dislike
            var like_content = parseInt(pos.children[0].textContent);
            var dislike_content = parseInt(pos.children[1].textContent);

            pos.children[0].textContent = like_content + result.l;
            pos.children[1].textContent = dislike_content + result.d;
            
        });
}
