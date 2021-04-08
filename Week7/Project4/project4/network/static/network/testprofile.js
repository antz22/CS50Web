document.querySelector('DOMContentLoaded', function() {

    const profile = "{{ profile }}";
    // let followstatus = "{{ followstatus }}";


    load_profile();

});

function load_profile() {


    fetch(`/profile/${profile.id}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        posts.forEach(load_profposts());
    })
    .catch(error => console.error(error))
        
}


function load_profposts(post) {

    // if (followstatus === true) {
    //     const unfollow = document.createElement('h6');
    //     unfollow.innerHTML = `<b> Unfollow </b>`;        
    //     unfollow.id = 'unfollow';
    // } else if (followstatus === false) {
    //     const follow = document.createElement('h6');
    //     follow.innerHTML = `<b> Follow </b>`;              
    //     follow.id = 'follow';
    // }


    document.querySelector('posts-view').innerHTML = '';
    const post = document.createElement('div');
    post.className = "view-post";
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


    post.append(content, timestamp, likes)
    document.querySelector('#posts-view').append(post)


}