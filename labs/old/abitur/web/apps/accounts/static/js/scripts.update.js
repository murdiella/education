(function($){
	
	/*	в содержимом, которое выводит контроллер могут быть кэпшны 
		(/views/messages) выводимые в <template/>, их надо переместить
		в .sidebar .act-caption	*/
	$('aside .act-caption').html($('template#act-caption').html());
	
	$(function(){
		//	инициализация главного меню (для отображения на мобильной версии)		
		if (typeof $.fn.mainmenu == 'function'){
			$('#mainmenu').mainmenu();
			
		}
	});
	
	if (typeof $.fn.wizard == 'function'){
		$('#wiz .swiper-container').wizard();
	}

	$(function() {
		$(".btn-group-toggle input[type='radio']:checked").parent().addClass('active');
		
		$("body").on("click", ".form__input_point", function () {
			$('.form__input_point').change(function(){
				if ($(this).val() > 100 ) {
					$(this).val('100');
				}
			});
		});
		
 	});

	
	

	
	
	
})(jQuery);
	