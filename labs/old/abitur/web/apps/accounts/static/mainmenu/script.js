(function($){
	
	/*	в содержимом, которое выводит контроллер могут быть кэпшны 
		(/views/messages) выводимые в <template/>, их надо переместить
		в .sidebar .act-caption	*/
	//$('aside .act-caption').html($('template#act-caption').html());
	
	var methods = {
		init: function(options){
			
			//var $modal = $(this);
			$(function(){
				var $sidebar = $('aside .sidebar:first');
				if ($sidebar.length > 0){
					$('#mainmenu-content').html($sidebar.html());
					
					// Временно
					
					$('#mainmenu .block-lk').attr('style','');
				}
			});

			return this;
		}
	};
	
	$.fn.mainmenu = function(params){
		if (methods[params]){
			return methods[params].apply(this, Array.prototype.slice.call(arguments, 1));
		}else if ( typeof params === 'object' || !params) {
			return methods.init.apply(this, arguments);
		}
		console.error('Метод не существует.');
	};
	//$('#mainmenu').mainmenu(); //	.modal
	
})(jQuery);
