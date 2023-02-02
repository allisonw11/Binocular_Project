const nextBtn = (url) =>{
    let body = {url:url}
    fetch("/search/next_page", {
        method:"POST",
        body:JSON.stringify(body),
        headers:{
            "Content-Type":"application/json",
        },
    })
    .then((response)=> console.log(response))

    }
        

