const button = document.querySelector('#submit');

button.addEventListener('click',() => {
    const queryString = new URLSearchParams({'order':orderNum}).toString();
    const url = `/status?${queryString}`;
    fetch(url)
        .then((response) => response.text())
        .then((status)=>{
            document.querySelector('#submit').innerHTML=status;
        });
});