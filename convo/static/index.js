window.onload = () =>
{
    console.log('here')
    url = (`/notifications`);

    const request = new Request(url);

    fetch(request,
        {
            method: 'GET'
        })
            .then(response => response.json())
                .then(resObj => 
                    {
                        console.log(resObj);
                        if(resObj.new_req == 'true')
                        {
                            requests = document.getElementById('requests');
                            requests.className = "dropdown-item text-dark bg-light";
                        }
                        if(resObj.new_msg == 'true')
                        {
                            chats = document.getElementById('chats');
                            chats.className = "dropdown-item text-dark bg-light";
                        }
                    });
}

// add drop down menu logic