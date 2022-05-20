var last_form = null;
document.addEventListener('DOMContentLoaded', function () {

    
    
        like_buttons = document.querySelectorAll('i');
        like_buttons.forEach(function(like_button) {
          like_button.addEventListener('click', function() {
      
            fetch(`/like/${this.dataset.id}`, {
              credentials: 'include',
              method: 'POST',
              mode: 'same-origin',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-CSRFToken': get_cookie('csrftoken') 
              },
            })
            .then(response => response.json())
            .then(result => {
              if (result.liked === "True") {
                document.querySelector(`i[data-id="${this.dataset.id}"]`).className = "fas fa-thumbs-up";
                like_cnt = document.querySelector(`div[data-id="${this.dataset.id}"]`).innerHTML;
                like_cnt = parseInt(like_cnt) + 1;
                like_cnt = document.querySelector(`div[data-id="${this.dataset.id}"]`).innerHTML = like_cnt;
              }
              else {
                document.querySelector(`i[data-id="${this.dataset.id}"]`).className = "far fa-thumbs-up";
                like_cnt = document.querySelector(`div[data-id="${this.dataset.id}"]`).innerHTML;
                like_cnt = parseInt(like_cnt) - 1;
                like_cnt = document.querySelector(`div[data-id="${this.dataset.id}"]`).innerHTML = like_cnt;
              }
            });
          });
        });
        function get_cookie(name) {
            if (!document.cookie) {
              return null;
            }
            
            const token = document.cookie.split(';')
            .map(c => c.trim())
            .filter(c => c.startsWith(name + '='));
          
            if (token.length === 0) {
              return null;
            }
            
            return decodeURIComponent(token[0].split('=')[1]);
          }
    
    if (document.getElementById("btnfollow")) {
        document.querySelector('#btnfollow').addEventListener("click", function (event) {
            fetch(`/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#sp_followers').innerHTML = data.total_followers;
                    if (data.result == "follow") {
                        this.innerHTML = "Following";
                        this.className = "btn btn-primary";
                    } else {
                        this.innerHTML = "Follow";
                        this.className = "btn btn-outline-primary";
                    }
                });

        })

        
        document.querySelector('#btnfollow').addEventListener("mouseover", function (event) {
            if (this.className == "btn btn-primary") {
                this.innerHTML = "Unfollow"
            }
        });

        
        document.querySelector('#btnfollow').addEventListener("mouseleave", function (event) {
            if (this.className == "btn btn-primary") {
                this.innerHTML = "Following"
            }
        });

    }
    
    

    edit_buttons = document.querySelectorAll('.edit_post');
    cancel_buttons = document.querySelectorAll('.cancel-button');
    save_buttons = document.querySelectorAll('.save-button');

    edit_buttons.forEach(function(edit_button) {
        edit_button.addEventListener('click', function() {
            post_id = this.dataset.editid;
            post_ctr = document.querySelector(`div[data-message="${post_id}"]`);
            edit_ctr = document.querySelector(`div[data-edit_ctr="${post_id}"]`);
            
            original_post = document.querySelector(`div[data-message="${post_id}"]`).innerHTML;
            edit_post = document.querySelector(`#text_edit${post_id}`);
            edit_post.value = original_post;
             
            post_ctr.style.display = 'none';
            edit_ctr.style.display = 'block';

            post_box = document.querySelector(`#text_edit${post_id}`);
            setTimeout(function () {
                post_box.focus();
                
            }, 0);

            
        });
    });

    cancel_buttons.forEach(function(cancel_button) {
        cancel_button.addEventListener('click', function() {
            post_id = this.dataset.cancelid;

            post_ctr = document.querySelector(`div[data-message="${post_id}"]`);
            edit_ctr = document.querySelector(`div[data-edit_ctr="${post_id}"]`);

            post_ctr.style.display = 'block';
            edit_ctr.style.display = 'none';
        });
    });

    save_buttons.forEach(function(save_button) {
        save_button.addEventListener('click', function() {
            post_id = this.dataset.saveid;
            
            post_box = document.querySelector(`#text_edit${post_id}`);
            
            text = post_box.value; 

            post_ctr = document.querySelector(`div[data-message="${post_id}"]`);
            edit_ctr = document.querySelector(`div[data-edit_ctr="${post_id}"]`);

            post = document.querySelector(`div[data-message="${post_id}"]`);
           
            fetch(`/post/${post_id}`, {
                credentials: 'include',
                method: 'POST',
                mode: 'same-origin',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken') 
                },
                body: JSON.stringify({message: text}),
            })
            .then(response => response.json())
            .then(result => {
                if (result.message != undefined && result.message.length > 0) {
                    message_ctr = document.getElementById('result-message');
                    message_ctr.innerHTML = result.message;
                    post.innerHTML = text;
                }
                else {
                    message_ctr = document.getElementById('result-message');
                    post.innerHTML = text;
                    post_ctr.style.display = 'block';
                    edit_ctr.style.display = 'none';
                }
            });
        });
    });
    function getCookie(name) {
      if (!document.cookie) {
        return null;
      }
      
      const token = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
    
      if (token.length === 0) {
        return null;
      }
      
      return decodeURIComponent(token[0].split('=')[1]);
    }
});
