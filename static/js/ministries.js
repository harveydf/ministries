$(document).on('ready', main);

function backToTop(){
	var animatecss = {
		scrollTop: 0
	};

	$('html, body').animate(animatecss, 'slow');
}

function bodyScrollModal(){
	if($('body').css('overflow') == 'auto'){

		$('body').css('overflow', 'hidden');
	}
	else{
		$('body').css('overflow', 'auto');	
	}
}

function closeModal(){
	var modalCss = {
		'opacity': 0,
		'pointer-events': 'none'
	};

	$('#openModal').css(modalCss);
}

function main (argument) {
	// openModal click event
	$('#events, #htmlcalendar').on('click', 'a', openModal);
	$('#events, #htmlcalendar').on('click', 'a', bodyScrollModal);


	// Upload button 
	$('.input-file').on('change', uploadFile);

	$('.input-file').on('mousedown mouseup', uploadHover);

	// @media queries
	$(window).on('resize', windowResize);
}

function openModal(data){

	var dataset = data.currentTarget.dataset;

	var div = $('<div>');
	var a = $('<a href="#close" title="Close" class="close">').append('X').on('click', closeModal);
	div.on('click', 'a', bodyScrollModal);

	var section = $('<section>');
	var h2 = $('<h2>').append(dataset.day);
	var h3 = $('<h3>').append(dataset.dayname);

	section.append(h2)
	section.append(h3)

	var ul = $('<ul>');

	$('#events a[data-day="'+dataset.day+'"]').each(function(){
		var li = $('<li>');
		var span1 = $('<span>').html($(this).data('hour'));
		var span2 = $('<span>').html($(this).data('title'));
		li.append(span1);
		li.append(span2);
		ul.append(li);
	});

	div.append(a)
	div.append(section)
	div.append(ul)

	var openModalCss = {
		'opacity': 1,
		'pointer-events': 'auto'
	};

	$('#openModal').html(div).css(openModalCss);
	$('body').on('scroll', bodyScrollModal);
}

function uploadFile(data){
	if($('#' + data.currentTarget.id).val() != ''){
		$('#upload_form').trigger('submit');
	}
}

function uploadHover(){
	$('.upload-button').toggleClass('hover') ;
}

function windowResize(){
	var width = $(window).width();
	
	if (width < 500) {
		$('.day a').each(function(){ $(this).html('●') })
	}
	
	else {
		$('.day a').each(function(){ $(this).html($(this).data('title')) })
	}
}




