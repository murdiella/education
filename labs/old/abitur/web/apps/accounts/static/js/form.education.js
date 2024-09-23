;(function($, existItems){
	
	var itemIdCounter = 0;
	
	function getExamItemHtml(id) {
		var html = $('template[content="item"]:first').html();
		html = html.replace(/\$\{id\}/g, id);
		return html;
	}

	$(function(){
		
		//	Создаем уже добавленные ранее предметы (восстановлены из бд)
		console.log(existItems)
		if (existItems && Object.keys(existItems).length > 0){

			existItems.forEach(function(item){
				
				$('.achievement-list:first').append(getExamItemHtml(itemIdCounter));
				console.log('yesey');
				
				$('#type_'+itemIdCounter+' option[value='+(item.type < 10 ? '0'+item.type : item.type)+']').prop('selected', true);
				$('#serial_'+itemIdCounter).val(item.doc_series);
				$('#number_'+itemIdCounter).val(item.doc_number);	
				$('#issued_date_'+itemIdCounter).val(item.issued_date);	
				itemIdCounter++;
			});
		}
		
		$('.add.add_item').on('click', function(event){
			var $this = $(this);
			$this.parents('.row:first').prev('.achievement-list').append(
				getExamItemHtml(itemIdCounter++)
			);

			event.preventDefault();
		});
		/*
		if ($('.exam-item').length > 0){
			var values = $(".exam-item").map(function(){
				return parseInt(this.getAttribute('data-item-id')) || -Infinity;
			}).toArray();
			values = 1 + Math.max.apply(Math, values);
			if (values > -Infinity){
				itemIdCounter = values;
			}
		}
		*/
	});
})(jQuery, existItems);

function deleteItem(item) {
	$(item).parents('.exam-item:first').slideUp("fast" , function(){
		$(this).remove();
	})
	event.preventDefault();
}

