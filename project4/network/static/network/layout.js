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

        var action =  document.getElementById('follow_button')
        var followers =document.getElementById('u_followers')
        var followers_cont = parseInt(followers.textContent)
        
        if(result.message == 'Unfollow'){
            action.innerHTML = 'Follow';
            action.className = "btn btn-primary";
        }else if (result.message == 'Follow') {
            action.innerHTML = 'Unfollow';
            action.className = 'btn btn-danger';
        }
        if (result.message == 'Unfollow'){
            followers.textContent = followers_cont - 1;
        }else if (result.message == 'Follow'){
            followers.textContent = followers_cont + 1;
        }
    });
  }
