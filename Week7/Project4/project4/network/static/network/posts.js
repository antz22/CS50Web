document.addEventListener('DOMContentLoaded', function() {

    document.getElementByClassName("posts-view").addEventListener('click', function(event) {
        const element = event.target;
        if (element.classList.containts("edit")) {
            // problem here -- would probably just return the first one
            console.log('Hi!');
            const parent = element.parentNode;
            const content = parentNode.querySelector('#content').value;
            // document.querySelector(`#${element.className}`).innerHTML = '';
            content.innerHTML = `<textarea>${content}</textarea>`;
            const submit = document.createElement('button');
            submit.id = 'submit-edit';
            submit.innerHTML = `Save`;
            document.addEventListener('click', function(e) {
                const el = e.target;
                if (el.id === 'submit-edit') {
                    const newContent = content.value;
                    fetch(`/posts/${post.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            content: newContent
                        })
                    })
                }
            });

            parentNode.append(submit);

            
        }
    })
    // var x = document.getElementsByClassName("example");


});

function load_page(kind) {

    
// how to make it so that clicking the button triggers javascript code? 
// somehow append the button 'edit' to every post in javascript only? but is that the right way to do it?
// after that, can use .innerHTML with wiki 'edit.html' and fetch calls we've done before

}


function load_posts(post) {

    document.querySelector('posts-view').innerHTML = '';
    const post = document.createElement('div');
    post.className = "view-post";
    const user = document.createElement('h6');
    user.innerHTML = `<b> <a href='/profile/{% post.user.id %}/'> ${post.user} </a> </b>`;
    const content = document.createElement('p');
    content.innerHTML = `${post.content}`;
    const timestamp = document.createElement('p');
    timestamp.innerHTML = `${post.datetime}`;
    const likes = document.createElement('p');
    likes.innerHTML = `${post.likes}`;
    likes.id = 'likes';
    let liked = false;
    document.addEventListener('click', function(event) {
        const element = event.target;
        if (element.id === 'likes' && liked === false) {
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: (likes+1)
                })
            })
            liked = true;
            // location.reload()?
        } else if (element.id === 'likes' && liked === true) {
            fetch(`/posts/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: (likes-1)
                })
            })
            liked = false;            
        }
    })

    post.append(user, content, timestamp, likes)
    document.querySelector('#posts-view').append(post)


}




// figure out self.serialize and sending api stuff
// pagination