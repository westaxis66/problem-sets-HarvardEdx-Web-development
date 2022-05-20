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
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    document.querySelector('#compose-form').onsubmit = () => {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
      })
      .then(response => response.json())
      .then(() => {
          load_mailbox('sent');
      });
      return false;
    };
  }
  
  function load_mailbox(mailbox) {
    
    
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
  
    
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            console.log(mailbox);

           
              
            
          const headerDiv = document.createElement('div');
          const emailHeader = document.createElement('table');
          emailHeader.setAttribute("style", "color: white;");
          emailHeader.className= "table-responsive";
          emailHeader.innerHTML = `
                  <table class="table table-striped table-hover refresh-container pull-down">
                      <thead class="table">
                        <tr><td class="col-sm-2" style="color: white;"><strong>Email#</strong></td>
                            <td class="col-sm-3" style="color: white;"><strong>from</strong></a></td>
                            <td class="col-sm-1"></td>
                            <td class="col-sm-4" style="color: white;"><strong>Subject</strong></a></td>
                            <td class="col-sm-4" style="color: white;"><strong>Date</strong></a></td>
                            <td class="col-sm-1"></td>
                        </tr></thead>
                    </table>    
                  `;
          document.querySelector('#emails-view').appendChild(emailHeader);
            
          if (emails.length > 0) {
            for (let i = 0; i < emails.length; i++) {
              let email = emails[i];
            
              if (email.archived && mailbox == 'inbox') {
                continue;
              }
              else {
                const inboxMail = document.createElement('div');
                inboxMail.className= "table-responsive";
                
                if (email.read) { inboxMail.style.backgroundColor = 'lightgrey'
                }
                else { inboxMail.style.backgroundColor = 'white';
                }
                
                console.log(email.id, email.archived)
                inboxMail.innerHTML = `
                            <table class="table table-striped table-hover refresh-container pull-down">
								                <tbody><tr>
									                  
                                    <td class="action" style="padding-left: 25px;">${email.id}</td>
									                  <td class="action"></i></td>
									                  <td class="action"></i></td>
									                  <td class="col-sm-4"><b>${email['sender']}</b> </td>
									                  <td class="col-sm-3">${email['subject']}</td>
									                  <td class="col-sm-3"><span><b>${email['timestamp']}</b></td>
								                </tr>
                             </table> 
                             `;

                document.querySelector('#emails-view').appendChild(inboxMail);
                inboxMail.addEventListener('click', () => load_email(email));
                
              }
      
            }
          }
        });
        
      }
  

  function load_email(email, mailbox) {
    
    document.querySelector('#compose-view').style.display = 'none';
    
  
    
    fetch('/emails/'+`${email.id}`)
    .then(response => response.json())
    .then(email => {
        document.querySelector('#emails-view').innerHTML = `<h2>${email.subject}</h2>`;
        
        console.log(`${email.id}`);
        const emailPage = document.createElement('div');
        emailPage.className ="border mt-2";
        emailPage.setAttribute("style", "padding: 20px; background-color: white;")
        emailPage.innerHTML = `
            <span style="font-weight: bold">From: </span>${email["sender"]}<br>
            <span style="font-weight: bold">To: </span>${email["recipients"]}<br>
            <span style="font-weight: bold">Subject: </span>${email["subject"]}<br>
            <span style="font-weight: bold">Sent on: </span>${email["timestamp"]}<br>
        `;
        
  
        const body = document.createElement('div');
        body.className ="border mt-2 mb-2";
        body.setAttribute("style", "padding: 20px; background-color: white;")
        body.innerHTML =`${email.body}`+ "<br>";
        document.querySelector('#emails-view').appendChild(emailPage);
        document.querySelector('#emails-view').appendChild(body);

        console.log(email)
           
        
        const archive = document.createElement('button');
        archive.className = "btn btn-outline-danger";
        archive.setAttribute("style", "margin-right:16px;");
        archive.textContent = email.archived ? "Unarchive" : "Archive";
        document.querySelector('#emails-view').appendChild(archive);
        archive.addEventListener('click', () => {
          console.log(email.archived)
          fetch('/emails/'+`${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !(email.archived)
                  
            })
          }).then(() => load_mailbox("inbox"));
        });
      
        const reply = document.createElement('button'); 
        reply.className ="btn btn-outline-primary";
        reply.setAttribute("style", "margin-right:16px;");
        reply.textContent = "Reply";
        document.querySelector('#emails-view').appendChild(reply);
  
        reply.addEventListener('click', () => {
          compose_email(); 

          if(email["subject"].slice(0,4) != "Re: "){
            email["subject"] = `Re: ${email["subject"]}`;
          }
      
          document.querySelector('#compose-recipients').value = email["sender"];
          document.querySelector('#compose-subject').value = `${email["subject"]}`;
          document.querySelector('#compose-body').value = `\n\n\n\n........On ${email["timestamp"]} \n${email["sender"]}, wrote:...${email["body"]}\n\n`;
        }); 
   
    fetch('/emails/'+`${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
        })
      });

    });  
    
  }  