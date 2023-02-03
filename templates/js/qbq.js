current_page_index = 0;


document.getElementById('page_' + current_page_index).style.display = 'block';

if(page_max_index === current_page_index) {
    document.getElementById('next_page_button').style.display = 'none';
    document.getElementById('submit_button').style.display = 'block'
}

document.getElementById('next_page_button').addEventListener('click', function() {
    document.getElementById('page_' + current_page_index).style.display = 'none';
    current_page_index += 1;
    if (current_page_index === page_max_index) {
        document.getElementById('next_page_button').style.display = 'none';
        document.getElementById('submit_button').style.display = 'block'
    }
    document.getElementById('page_' + current_page_index).style.display = 'block';
    document.getElementById('previous_page_button').style.display = 'block';

    current_page_number_element = document.getElementById('current_page_number');
    
    if (current_page_number_element !== null) {
        current_page_number_element.innerHTML = current_page_index + 1;

    }
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

    current_page_number_element = document.getElementById('current_page_number');
    
    if (current_page_number_element !== null) {
        current_page_number_element.innerHTML = current_page_index + 1;

    }

});

document.getElementById('submit_button').addEventListener('click', function() {
    document.getElementById('poll_form').submit();
});

max_page_number_element = document.getElementById('max_page_number');
if (max_page_number_element !== null) {
    max_page_number_element.innerHTML = page_max_index + 1;

}