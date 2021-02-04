document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
        read: false
      })
    })
    .then(response => response.json())
    .then(result => {
      // log result for now
      console.log(result)

    })
    .catch(error => console.error(error))
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    load_mailbox('sent'); // how to reload this part?

    return false;
  }

}

function reply_to_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Fill out composition fields with preexisting data
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  if (email.subject.includes('Re: ')) {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n----\n`;

  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
        read: false
      })
    })
    .then(response => response.json())
    .then(result => {
      // log result for now
      console.log(result)

    })
    .catch(error => console.error(error))
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    location.reload();
    load_mailbox('sent'); // how to reload this part?
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox == 'inbox') {
    // document.querySelector('#emails-view').style.display = 'none';
    
    
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      // Print email
      console.log(emails);

      emails.forEach(load_emails);


    })
    .catch(error => console.error(error))

  } else if (mailbox === 'sent') {

    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      emails.forEach(load_sent_emails);
    })
    .catch(error => console.error(error))

    
  } else if (mailbox === 'archive') {

    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      emails.forEach(load_archived_emails);
    })
    .catch(error => console.error(error))

  }

}

function load_emails(email) {
  

  const mail = document.createElement('div');
  mail.className = 'view-email';
  if (email.read === true && email.archived === false) {
    mail.innerHTML = `<button class="view read"><b class="view">${email.sender}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  } else if (email.read === false && email.archived === false) {
    mail.innerHTML = `<button class="view unread"><b class="view">${email.sender}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  }
  
  mail.addEventListener('click', function(event) {
    console.log('This element might have been clicked!')
    const element = event.target
    if (element.classList.contains('view')) {
      load_email(email, 'normal');
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    } 
    // code here on what happens when you View Email


  });
  document.querySelector('#emails-view').append(mail);
}

function load_sent_emails(email) {
  const mail = document.createElement('div');
  mail.className = 'view-sent-email';
  if (email.read === true) {
    mail.innerHTML = `<button class="view read">to: <b class="view">${email.recipients}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  } else if (email.read === false) {
    mail.innerHTML = `<button class="view unread">to: <b class="view">${email.recipients}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  }
  
  mail.addEventListener('click', function(event) {
    console.log('This element was clicked!')
    const element = event.target
    if (element.classList.contains('view')) {
      load_email(email, 'sent');
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }
  });

  document.querySelector('#emails-view').append(mail);

}

function load_archived_emails(email) {
  const mail = document.createElement('div');
  mail.className = 'view-email';
  if (email.read === true && email.archived === true) {
    mail.innerHTML = `<button class="view read"><b class="view">${email.sender}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  } else if (email.read === false && email.archived === true) {
    mail.innerHTML = `<button class="view unread"><b class="view">${email.sender}</b>  |  ${email.subject}  |  ${email.timestamp}</button>`;
  }
  
  mail.addEventListener('click', function(event) {
    console.log('This element might have been clicked!')
    const element = event.target
    if (element.classList.contains('view')) {
      load_email(email, 'normal');
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    } 
    // code here on what happens when you View Email


  });
  document.querySelector('#emails-view').append(mail);
}

function load_email(email, type) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  document.querySelector('#email-view').innerHTML = '';

  const sender = document.createElement('p');
  sender.innerHTML = `<b> From: </b> ${email.sender}`;
  const recipients = document.createElement('p');
  recipients.innerHTML = `<b> To: </b> ${email.recipients}`;
  const subject = document.createElement('p');
  subject.innerHTML = `<b> Subject: </b> ${email.subject}`;
  const date = document.createElement('p');
  date.innerHTML = `<b> Timestamp: </b> ${email.timestamp}`;
  const body = document.createElement('p');
  body.innerHTML = `${email.body}`;
  const reply = document.createElement('button');
  reply.id = "reply";
  reply.className = "btn btn-sm btn-outline-primary";
  reply.innerHTML = `Reply`;
  document.addEventListener('click', function(event) {
    const element = event.target
    if (element.id === 'reply') {
      reply_to_email(email);
    }  
  })

  
  
  
  if (type === 'normal') {
    
    if (email.archived === false) {
      
      const archive = document.createElement('button');
      archive.id = "archive";
      archive.className = "btn btn-sm btn-outline-primary";
      archive.innerHTML = 'Archive';
      archive.style.marginLeft = '5px';
      document.addEventListener('click', function(event) {
        const element = event.target
        if (element.id === 'archive') {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          location.reload();
          load_mailbox('inbox');
        }
      })

      hr = document.createElement('hr');

      document.querySelector('#email-view').append(sender);
      document.querySelector('#email-view').append(recipients);
      document.querySelector('#email-view').append(subject);
      document.querySelector('#email-view').append(date);
      document.querySelector('#email-view').append(reply);
      document.querySelector('#email-view').append(archive);
      document.querySelector('#email-view').append(hr);

      document.querySelector('#email-view').append(body);
    } else {
      const unarchive = document.createElement('button');
      unarchive.id = "unarchive";
      unarchive.className = "btn btn-sm btn-outline-primary";
      unarchive.innerHTML = 'Unarchive';
      unarchive.style.marginLeft = '5px';
      document.addEventListener('click', function(event) {
        const element = event.target
        if (element.id === 'unarchive') {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          location.reload();
          load_mailbox('inbox');
        }
      })



      hr = document.createElement('hr');

      document.querySelector('#email-view').append(sender);
      document.querySelector('#email-view').append(recipients);
      document.querySelector('#email-view').append(subject);
      document.querySelector('#email-view').append(date);
      document.querySelector('#email-view').append(reply);
      document.querySelector('#email-view').append(unarchive);
      document.querySelector('#email-view').append(hr);

      document.querySelector('#email-view').append(body);
    }


  } else {
    hr = document.createElement('hr');

    document.querySelector('#email-view').append(sender);
    document.querySelector('#email-view').append(recipients);
    document.querySelector('#email-view').append(subject);
    document.querySelector('#email-view').append(date);
    document.querySelector('#email-view').append(reply);
    document.querySelector('#email-view').append(hr);

    document.querySelector('#email-view').append(body);

  }

  



}


// reply -- how to load whitespace? / ---- then new line
// Get rid of the email from the inbox after replying?
// switch archive to only load_email
// view email -- style the emails on the inbox page correctly
// go through the project and add comments, make it readable and neat.