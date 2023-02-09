function deleteReview(review_id) {
    fetch("/delete_review")
        .then((response) => response.json())
        .then((responseData) => {
            document.querySelector().innerText=responseData;
        });
        // Need to work on delete function in server.py!