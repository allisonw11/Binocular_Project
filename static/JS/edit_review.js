'use strict';
function show_edit_form() {
    const edit_btn = document.querySelector("#show-edit-form");
    edit_btn.hidden = false;
};


function cancel_edit_form() {
    const cancel_edit_btn = document.querySelector("#show-edit-form");
    cancel_edit_btn.hidden = true;
};
try{
    document.querySelector("#cancel-submit").addEventListener("click", cancel_edit_form);


    document.querySelector("#edit-review-form").addEventListener("submit", (evt) => {
        evt.preventDefault();
        const editFormInputs = {
            "event_id": document.querySelector("#event-id").value,
            "rating": document.querySelector("#edit-rating-score").value,
            "title": document.querySelector("#edit-review-title").value,
            "review": document.querySelector("#edit-review-description").value,
            "recommendation": document.querySelector("#edit-yes-no").checked,
        };
        console.log(editFormInputs)

    fetch("/edit_review", {
        method:"POST",
        body: JSON.stringify(editFormInputs),
        headers:{
            "Content-Type":"application/json",
        },
    }) 
        .then((response) => response.text())
        .then((responseJson) => {
            const review_id = document.querySelector("#edit-review-id").value;
            document.querySelector(`#title_${ review_id }`).innerHTML=editFormInputs["title"];
            document.querySelector(`#rating_${ review_id }`).innerHTML=editFormInputs["rating"];
            document.querySelector(`#description_${ review_id }`).innerHTML=editFormInputs["review"];
            if (editFormInputs["recommendation"]) {
                document.querySelector(`#recommend_${ review_id }`).innerHTML="Recommendation: Yes"
            }
            else {
                document.querySelector(`#recommend_${ review_id }`).innerHTML="Recommendation: No"
            };
            setTimeout(function() {
                const edit_btn =document.querySelector("#show-edit-form");
                edit_btn.hidden = true;
            }, 200);
        });
    });
}catch{console.log("no reviews")}