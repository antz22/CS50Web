document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#posts-view').addEventListener('click', function(event) {
        const element = event.target;
        const parent = event.target.parentNode;
        console.log(element);
        if (element.classList.contains("edit")) {
            const content = element.nextElementSibling;
            const contText = document.createElement('textarea');
            contText.value = content.innerHTML;
            contText.classList.add('form-control');
            content.innerHTML = '';
            content.appendChild(contText);
            const submit = document.createElement('button');
            submit.id = 'submit-edit';
            submit.classList.add('btn');
            submit.classList.add('btn-primary');
            submit.innerHTML = `Save`;
            document.addEventListener('click', function(e) {
                const el = e.target;

                const postId = parent.id;

                if (el.id === 'submit-edit') {
                    const newContent = contText.value;
                    fetch(`/posts/${postId}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            content: newContent
                        }),
                        credentials: 'same-origin',
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    })
                    submit.remove();
                    content.innerHTML = `${newContent}`;
                }
            });

            parent.append(content);
            parent.append(submit);
 
            
        } else if (element.classList.contains("like")) {
            document.addEventListener('click', function(e) {
                const el = e.target;
                const postId = parent.id;
                const likes = element.previousElementSibling;
                const likesVal = parseInt(likes.innerHTML, 10);

                console.log(likes);
                console.log(el);
                console.log(likesVal);

                if (el.classList.contains("unlike")) {
                    fetch(`/posts/${postId}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: likesVal-1
                        }),
                        credentials: 'same-origin',
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    })
                    likes.innerHTML = `${likesVal-1}`;    
                    console.log(likes);
                    console.log(likesVal);
                    location.reload();
                } else {
                    fetch(`/posts/${postId}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: likesVal+1
                        }),
                        credentials: 'same-origin',
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    })
                    console.log(likes);
                    console.log(likesVal);
                    likes.innerHTML = `${likesVal+1}`;       
                    location.reload();                
                }
                
            });

        }
    })



});

function getCookie(c_name) {
    var c_value = " " + document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1) {
        c_value = null;
    }
    else {
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1) {
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start,c_end));
    }
    return c_value;
}
