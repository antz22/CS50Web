document.querySelector('DOMContentLoaded', function() {

    load_page('all');

});

function load_page(kind) {

    if (kind === 'all') {
        fetch('/posts/all')
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            posts.forEach(load_posts());
        })
        .catch(error => console.error(error))

    } else if (kind === 'following') {
        fetch('/posts/following')
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            posts.forEach(load_posts());
        })

    }
        

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