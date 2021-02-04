document.querySelector('DOMContentLoaded', function() {

    load_page('all');

});

function load_page(type) {

    if (type === 'all') {
        fetch('/posts/all')
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            posts.forEach(load_posts);
        })
        .catch(error => console.error(error))

    } else if (type === 'following') {
        fetch('/posts/following')
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            posts.forEach(load_posts);
        })

    }
        

}


function load_posts() {

    

}