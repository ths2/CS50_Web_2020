var tela = 'inbox';
var teste = null;
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    load_inbox()
  });
  document.querySelector('#sent').addEventListener('click', () => {
    load_mailbox('sent');
    tela = 'sent';
    request_emails();
  });
  document.querySelector('#archived').addEventListener('click', () => {
    load_mailbox('archive')
    tela = 'archive';
    request_emails();
  });
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#reply_button').addEventListener('click', reply_email);


  document.querySelector('#arch_button').addEventListener('click', () => { 
    archive(teste); 
  });

  document.querySelector('#unarch_button').addEventListener('click', () => { 
    archive(teste);
  });

  //Post email
  document.querySelector('#compose-view').onsubmit = function() {
    var t = document.getElementById('compose-recipients').value;
    var s = document.getElementById('compose-subject').value;
    var b = document.getElementById('compose-body').value;
    post_email(t, s, b);
  }; 

    //Reply post email
    document.querySelector('#reply-view').onsubmit = function() {
      var t = document.getElementById('reply-recipients').value;
      var s = document.getElementById('reply-subject').value;
      var b = document.getElementById('reply-body').value;
      post_email(t, s, b);

    }; 

  // By default, load inbox
  load_inbox()
     

});


// *Functions*

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#display-email-inbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#reply-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function reply_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#display-email-inbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'block';

  // Clear out composition fields
  if (teste){
    document.querySelector('#reply-recipients').value = teste.sender;
    if (teste.subject.startsWith("Re: ")){
      document.querySelector('#reply-subject').value = teste.subject;
    }else{
      document.querySelector('#reply-subject').value = 'Re: ' + teste.subject;
    }
    
    document.querySelector('#reply-body').value = teste.timestamp + " " + teste.sender + " wrote: " + "\n\n" + teste.body + " \n-------------------------------------------\n";
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#display-email-inbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function display_email(element){

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email-inbox').style.display = 'block';
  document.querySelector('#reply-view').style.display = 'none';
  console.log("Display E-mail");
  request_an_email(element);
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
      load_mailbox('sent');
      tela = 'sent';
      request_emails();
  });
}

function request_emails(){
  var str = '/emails/' + tela;

  fetch(str)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      const table = document.createElement('table');
      const tbody = document.createElement('tbody');
      table.appendChild(tbody);
      table.setAttribute('class', 'table');

      document.querySelector('#emails-view').append(table);

      emails.forEach(element => {
        // ... do something else with emails ...
        //const email = document.createElement('div');
        //email.innerHTML = element.body;
        var tr = return_email_tr(element);
       
        if (element.read){
          tr.setAttribute('class', 'table-active');
        } 

         
        tr.addEventListener('click', function() {
          display_email(element);
          console.log("Request Emaisl")
        });

        tbody.append(tr);
      });
    });
}

function return_email_tr(element){
  var element_email = element;
  var tr = document.createElement('tr');
  var td_sender = document.createElement('td');
  var td_subject = document.createElement('td');
  var td_date = document.createElement('td');

  if (tela == "inbox" || tela =="archive"){
    td_sender.innerHTML = element_email.sender;
  } else if (tela == "sent"){
    td_sender.innerHTML = element_email.recipients;
  }
  
  td_subject.innerHTML = element_email.subject;
  td_date.innerHTML = element_email.timestamp;


  tr.appendChild(td_sender);
  tr.appendChild(td_subject);
  tr.appendChild(td_date);

  return tr;
}

//Request an email for ID
function request_an_email(element){
  var str = '/emails/' + element.id;

  console.log(str);
  fetch(str)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      // ... do something else with email ...
  
      /*
      var div_sender = document.querySelector('#div_sender');
      var div_recipients = document.querySelector('#div_recipients');
      var div_date = document.querySelector('#div_date');
      var div_subject= document.querySelector('#div_subject');  
      var reply_button = document.querySelector("#reply_button");
      var arch_button = document.querySelector("#arch_button");    
      */
      div_sender.innerHTML = '<b>From:</b> ' + email.sender;
      div_recipients.innerHTML = '<b>To:</b> ' + email.recipients;
      div_date.innerHTML = '<b>Timestamp: </b>' + email.timestamp;      
      div_subject.innerHTML = '<b>Subject: </b>' + email.subject;

      

      if (tela == 'inbox'){
         reply_button.style.display = 'inline';
         arch_button.style.display = 'inline';
         unarch_button.style.display = 'none';

      }else if (tela == 'archive'){
        reply_button.style.display = 'inline';
        arch_button.style.display = 'none';
        unarch_button.style.display = 'inline';

      }else {
        reply_button.style.display = 'none';
        arch_button.style.display = 'none';
        unarch_button.style.display = 'none';
      }

      if(!email.read){ 
        
        fetch(str, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        }) 
      }
      
      teste = element;

      var div_body = document.querySelector('#div_body');
      div_body.innerHTML = email.body;

  });
  
      
}

function archive(element){
  
  if (element.archived){
    fetch('/emails/' + element.id, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    }).then(response => response.json())
    .then(_result => {
        // Print result
        load_inbox() 
    });
  }else{
    fetch('/emails/' + element.id, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    }).then(response => response.json())
    .then(_result => {
        // Print result
        load_inbox() 
    })
  }

}

//load the inbox
function load_inbox(){
      load_mailbox('inbox');
      tela = 'inbox';
      request_emails();       
}