function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$('#checkbox').click(function(){
    const $this = $(this);

    var params = new URLSearchParams(); 
    params.set('answer_id', $this.data('answer'));
    params.set('question_id', $this.data('question'));
    params.set('value', $(this).is(':checked'));

    const request = new Request(
        'http://127.0.0.1:8000/checkbox_vote/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $('checkbox').prop('checked', parsed.value);
        });
    })
});

$(".likes-answer").on('click', function (ev) {
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/answer_vote/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text('Like ' + parsed.new_rating );
        });
    })
})

$(".button-likes").on('click', function (ev) {
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/question_vote/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'question_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text('Like ' + parsed.new_rating );
        });
    })
})