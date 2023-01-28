current_page_index = 0;


document.getElementById('page_' + current_page_index).style.display = 'block';

document.getElementById('next_page_button').addEventListener('click', function() {
    document.getElementById('page_' + current_page_index).style.display = 'none';
    current_page_index += 1;
    if (current_page_index === page_max_index) {
        document.getElementById('next_page_button').style.display = 'none';
        document.getElementById('submit_button').style.display = 'block'
    }
    document.getElementById('page_' + current_page_index).style.display = 'block';
    document.getElementById('previous_page_button').style.display = 'block';
});

document.getElementById('previous_page_button').addEventListener('click', function() {
    document.getElementById('page_' + current_page_index).style.display = 'none';
    current_page_index -= 1;
    if (current_page_index === 0) {
        document.getElementById('previous_page_button').style.display = 'none';
    }
    document.getElementById('page_' + current_page_index).style.display = 'block';
    document.getElementById('next_page_button').style.display = 'block';
    document.getElementById('submit_button').style.display = 'none'

});

document.getElementById('submit_button').addEventListener('click', function() {
    document.getElementById('poll_form').submit();
});