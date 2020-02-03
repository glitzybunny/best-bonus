'use strict'

// Elements
// Search
const search_input = $("#search-field-text");
const search_field_button = $('#search-field-button');
const search_group = $('#search-field-text, #search-field-button');
const clear_button = $('#clear_button');

// Content
const paginator_button = $('#paginatorButton1');
const cardblock_div = $('#replaceable-cardblock');
const cardblock_content = $('.card-block')


// Filter
const deposit_slider_jqobj = $("#deposit-js-range-slider");
const bonus_slider_jqobj = $("#bonus-js-range-slider");
const wager_slider_jqobj = $("#wager-js-range-slider");

const deposit_range_input_from = $('#deposit_range_input_from');
const deposit_range_input_to = $('#deposit_range_input_to');

const bonus_range_input_from = $('#bonus_range_input_from');
const bonus_range_input_to = $('#bonus_range_input_to');

const wager_range_input_from = $('#wager_range_input_from');
const wager_range_input_to = $('#wager_range_input_to');

const filter_form = $('#filter-form');
const filter_refresh_button = $('#filter-refresh-button');

const filterbox = $('aside');
const floating_filter_button = $('#floating-filter-button');

// Organization of relations between range slider and their inputs 
const range_sliders = [
    {'slider': deposit_slider_jqobj, 'input_from': deposit_range_input_from, 'input_to': deposit_range_input_to },
    {'slider': bonus_slider_jqobj, 'input_from': bonus_range_input_from, 'input_to': bonus_range_input_to },
    {'slider': wager_slider_jqobj, 'input_from': wager_range_input_from, 'input_to': wager_range_input_to },
];


// For AJAX Search
const delay_by_in_ms = 700;
let scheduled_function = false;

//Endpoints
const paginator_endpoint = '/';
// const search_endpoint = 'ajax-search/';

const filter_endpoint = 'ajax-filter/'
const search_endpoint = 'ajax-search/'

// Next page number variable for AJAX Paginator
let current_page = 2;


// ionRangeSlider
// Initialization of range sliders

// Deposit range slider
deposit_slider_jqobj.ionRangeSlider({
    skin: "flat",    
    type: "double",
    min: 0,
    from: 0,
});

// Bonus range slider
bonus_slider_jqobj.ionRangeSlider({
    skin: "flat",
    type: "double",
    min: 0,
    from: 0,
});

// Wager range slider
wager_slider_jqobj.ionRangeSlider({
    skin: "flat",
    type: "double",
    min: 0,
    from: 0,
});


// Handling filter form
let ajax_call = function (endpoint, request_parameters) {

    $.getJSON(endpoint, request_parameters)
    .done(response => {
        cardblock_div.fadeTo('slow', 0).promise().then(() => {
            // replace the HTML contents
            cardblock_div.html(response['html_from_view'])
            cardblock_div.fadeTo('slow', 1)
        })
    })
};


// Event handlers

// Floating button event
floating_filter_button.on('click', function (e) {

    filterbox.toggle("slow");
    
    document.getElementById("filterbox-anchor").scrollIntoView({
        behavior: 'smooth',
        block: 'start' //scroll to top of the target element
    });

});

// Search clear button event
clear_button.on('click', function(e) {
    e.preventDefault();
    search_input.val('');
    ajax_call(search_endpoint, {'q':''});
    
});

// Filter submit event
filter_form.on('submit', function(e){
    e.preventDefault();
    let form_data = $(this).serializeArray();
    ajax_call(filter_endpoint, {'filter': true, 'form_data': JSON.stringify(form_data)});
        
});

// Filter refresh event
filter_refresh_button.on('click', function(e){
    e.preventDefault();
    document.getElementById('filter-form').reset();

    // Calls ionRangeSlider reset method for all existing sliders
    // Check out ionRangeSlider docs
    for (let r = 0; r < range_sliders.length; r++) {
        range_sliders[r].slider.data("ionRangeSlider").reset();    
    };
});


// Events for from input, to input and range slider. Sync values between range slider and inputs
// When range slider value changes it writes current values to inputs.
let slidersEventInit = function (slider, from_input, to_input) {
    from_input.on('keyup', function() {
        slider.data("ionRangeSlider").update({from : $(this).val()});
    });
    
    to_input.on('keyup', function () {
        slider.data("ionRangeSlider").update({to : $(this).val()});
    });
    
    slider.on('change', function() {
        let slider_values = $(this).val().split(';');
        from_input.val(slider_values[0]);
        to_input.val(slider_values[1]); 
    });
};

// Iterates through slider ranges
for (let e = 0; e < range_sliders.length; e++) {
    slidersEventInit(range_sliders[e].slider, range_sliders[e].input_from, range_sliders[e].input_to); 
};


// Search handler
search_input.on('keyup', function (e) {
    let request_parameters = {
        // value of user_input
        q: $(this).val(),
    };
    if (scheduled_function) {
        clearTimeout(scheduled_function);
    };
    // ajax_call(endpoint, request_parameters)
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, search_endpoint, request_parameters);    
});

// Paginaton
paginator_button.on('click', function() {
    
    let request_parameters = {
        'paginator_enabled' : true,
        'page' : current_page,
    };
    
    let ajax_handler = $.getJSON(paginator_endpoint, request_parameters)
        .done( response =>  {
            // console.log("success");
            if (response.paginator_hiding) {
                paginator_button.remove();
            };
            // Takes html of cardblock div from server response 
            let content_to_show = $(response.html_from_view).filter(".card-block").html();  
            //Adding response cardblock to current cardblock
            $(cardblock_content[0]).append(content_to_show);            
            current_page++;
        })
        .fail(function() {
          console.log( "error" );
        })
});