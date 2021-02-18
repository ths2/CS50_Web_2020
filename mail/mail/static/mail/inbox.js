document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    load_mailbox('inbox');
    request_emails('inbox');
  });
  document.querySelector('#sent').addEventListener('click', () => {
    load_mailbox('sent')
    request_emails('sent');
  });
  document.querySelector('#archived').addEventListener('click', () => {
    load_mailbox('archive')
    request_emails('archive');
  });
  document.querySelector('#compose').addEventListener('click', compose_email);


  //Post email
  document.querySelector('#compose-form').onsubmit = function() {
    var t = document.getElementById('compose-recipients').value;
    var s = document.getElementById('compose-subject').value;
    var b = document.getElementById('compose-body').value;
    post_email(t, s, b);
    
  }; 

    // By default, load the inbox
    load_mailbox('inbox');
});


// *Functions*

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function post_email(recipients, subjects, body){
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subjects,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  load_mailbox('sent');
}

function request_emails(title){
  var m = title;
  var str = '/emails/' + title;
  console.log(str);
  fetch(str)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      //console.log(emails);

      emails.forEach(element => {
        console.log(element);
        // ... do something else with emails ...
        const email = document.createElement('div');
        email.innerHTML = element.body;
        email.addEventListener('click', function() {
            console.log('This element has been clicked!')
        });
        console.log(element.body);
        document.querySelector('#emails-view').append(email);
      });
    });
}