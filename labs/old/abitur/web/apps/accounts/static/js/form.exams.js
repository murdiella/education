;(function($, existItems){
	
	var itemIdCounter = 0;
	var today = new Date();
	
	function addYearTab(year){
		
		var $lastSeenTab;	//	Для сортировки
		
		if ($('#tabs-exams .nav-link_year').length == 0){
			$('#tabs-exams').prepend(getTabHtml(year));
			return;
		}
		
		//	Ищем между какими табами вставить 2019..2015..2010
		$('#tabs-exams .nav-link_year').each(function(){
			
			$lastSeenTab = $(this);
			
			if (parseInt($lastSeenTab.data('year')) < year){
				$lastSeenTab.parents('li:first').before(getTabHtml(year));
				$lastSeenTab = null;
				return false;
			}
		});
		
		//	Если значение year ещё меньше, чем у существующих,  то добавляем в конец
		if ($lastSeenTab){
			$lastSeenTab.parents('li:first').after(getTabHtml(year));
		}
		
	}
	function addYearTabPane(year, createExamBlankItem){
		$('#tabcontent-exams').append(getTabPaneHtml(year));
		
		if (createExamBlankItem){
			var $tabpane = $('#tabpane-'+year);
			$tabpane.prepend(getExamItemHtml(itemIdCounter++, year))
				.find('.add.add_item').on('click', function(event){
					var $this = $(this);
					$this.parents('.row:first').before(
						getExamItemHtml(itemIdCounter++, $this.data('yearOf'))
					);
					event.preventDefault();
				});
		}

			
	}
	function getExamItemHtml(id, year) {
		var html = $('template[content="item"]:first').html();
		html = html.replace(/\$\{year\}/g, year);
		html = html.replace(/\$\{id\}/g, id);
		return html;
	}
	function getTabPaneHtml(year){
		return $('template[content="tab-pane"]:first')
			.html().replace(/\$\{year\}/g, year);
	}
	function getTabHtml(year){
		return $('template[content="tab"]:first')
			.html().replace(/\$\{year\}/g, year);
	}
	
	$(function(){
		
		//	Создаем табы для записей, загруженных с сервера (восстановлены из бд)

		if (existItems && Object.keys(existItems).length > 0){

			for (var year in existItems){
				
				addYearTab(year);
				addYearTabPane(year, false);
				
				var $tabpane = $('#tabpane-'+year);			
				
				existItems[year].forEach(function(item){
					
					console.log(item);
					
					$tabpane.find('.row:last').before(getExamItemHtml(itemIdCounter, year));
					$('#subject_'+itemIdCounter+' option[value='+(item.subject)+']').prop('selected', true);
					$('#mark_'+itemIdCounter).val(item.mark);
					$('#type_'+itemIdCounter).val(item.type);
					itemIdCounter++;				
				});
				
				if (year == today.getFullYear()){
					$('#tab-'+year).tab('show');
				}else{
					$('.nav-link_year:first').tab('show');
				}
			}
		}
		
		$('.add.add_item').on('click', function(event){
			var $this = $(this);
			$this.parents('.row:first').before(
				getExamItemHtml(itemIdCounter++, $this.data('yearOf'))
			);
			event.preventDefault();
		});
		
		/*
		
		//	Вычисляем максимальный id у предметов если какие-то уже есть
		//	и устанавливаем максимальный itemIdCounter + 1
		
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
		//	Если нет ни одной вкладки по годам (форма заполняется впервые), то
		//	надо создать пустую вкладку текущего года с одним пустым предметом
		
		if ($('.tab-pane_year').length == 0){
			addYearTab(today.getFullYear());
			addYearTabPane(today.getFullYear(), true);
			$('#tab-'+today.getFullYear()).tab('show');	
		}
		
		//	Создаем обработчик на нажатие кнопок из табы "Добавить за другой  
		//	год", также если имеются табы по каким-то годам, то добавляем 
		//	им класс _aready-exist (opacity: .5)
		
		$('#tabpane-addyear .btn-year:not(.btn-year_earlier)').each(function(){
			
			var $this = $(this);
			
			if ($('#tab-'+this.value).length != 0){
				$this.addClass('_already-exist');
			}
			
			$this.click(function(event){
				
				if ($('#tab-'+this.value).length == 0){
					addYearTab(this.value);
					addYearTabPane(this.value, true);
					$this.addClass('_already-exist');
					$('#tab-'+this.value).tab('show');
				}
				event.preventDefault();
			});
		});
		

	});
	
	
	
})(jQuery, existItems);