

function postButton(id)
{
    var btn = document.getElementById(id);
    var prevBtn = btn.value;
    if (id == 'btn2')
    {
        var btn1 = document.getElementById('btn');
        prevBtn = btn1.value;
    }
    if (btn.value == 'Accept') var btn2 = document.getElementById('btn2');
    else if (btn.value == 'Unfriend') var chatBtn = document.getElementById('chat-btn');

    var username = document.getElementById('username').innerHTML;
    var btnDiv = document.getElementById('btn-div');

    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    url = (`/profile/${username}`);

    var request = new Request(
        url,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request,
    {
        method: 'POST',
        body: JSON.stringify(
            {
                button: btn.value,
                other_user: username
            })
    })
        .then(response => response.json())
            .then(resObj => 
                {
                    if(btn.value == 'Accept')
                    {
                        btn2.remove();
                        btnDiv.innerHTML += `<a id='chat-btn' class='btn btn-secondary mr-sm-2' href='/chat/${username}'>Chat</a>`;
                    }
                    else if (btn.value == 'Reject') btn.remove();
                    else if (btn.value == 'Unfriend') chatBtn.remove();
                    resBtn = resObj.button;
                    (id == 'btn2') ? btn1.value = resBtn : btn.value = resBtn;
                    if (resBtn == prevBtn) location.reload();
                });
}


function profileEdit()
{
    const profBio = document.getElementById('profile-bio');
    const profAddress = document.getElementById('profile-address');
    const textBio = document.getElementById('id_bio');
    const textAddress = document.getElementById('id_address');

    const form = document.getElementById('profile-form');
    const editBtn = document.getElementById('edit');

    if (form.style.display == 'none')
    {
        form.style.display = 'block';
        textBio.value = profBio.innerHTML;
        textAddress.value = profAddress.innerHTML;
        editBtn.innerHTML = 'Cancel';
    }
    else
    {
        form.style.display = 'none';
        editBtn.innerHTML = 'Edit';
    }
}