document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('#follow_button').addEventListener('click', () => {
        var username = document.getElementById('username').innerText
        post_follow(username);
    });


})


function post_follow(idUserFollow){
    
    fetch('/follow', {
      method: 'POST',
      body: JSON.stringify({
          idUser: idUserFollow,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        var username = document.getElementById('#follow_button')
        var action =  document.getElementById('follow_button')

        if(result.message == 'Unfollow'){
            action.innerHTML = 'Follow';
        }else if (result.message == 'Follow') {
            action.innerHTML = 'Unfollow';
        }
        console.log(action)
    });
  }
