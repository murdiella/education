/*
	Плагин для добавления блоков множественных полей типа <input name="file[passport][4]" в форме. Не только для файлинпутов. 
	
	1. Для добавления блока с полем ищет <template content="заданное имя шаблона"/>.
	
	2. В шаблоне заменяет все цепочки в коде вида <input type="file" name="AttachmentForm[${varname}][${id}]">, кроме varname могут быть 
	какие угодно и сколько угодно переменных. id инкрементируется с каждым новым блоком, если при загрузке 	уже существует какое-либо 
	число блоков плагин вычисляет самый максимальный и добавляет новый блок с максимальным значением + 1 (см. var counter).
	
	3. Созданный блок вставляется в конец элемента, по которому создан плагин	
	
	options 
	{
		templateContentName: название шаблона (<template content="название шаблона">),
		replacements: {
			varname1: имя переменной,
			varname2: имя переменной,
			...
			varnameN: имя переменной
		}
	}
	
	Семантика:
	
	<div class="multiple-list" id="list-id">
		...
		<a href="#list-id" class="remove remove_item">Удалить</a> (находится внутри блока)
		...
	</div>
	...
	<a href="#list-id" class="add add_item" data-max-limit="ограничение">Добавить</a>
	...
	<template content="templateContentName">
		<div class="multiple-list__item" data-item-id="${id}" id="${varname}-${id}">
			<input type="file" id="attachmentform-${varname}-${id}" class="file-input file-upload__input" name="AttachmentForm[${varname}][${id}]">
			<span class="hint">${varname_hint}</span> (Пример с другой переменной)
		</div>
	</template>
*/

;(function($){

	var counter = 0;	//	инкрементируем ${id}
	var re = {};		//	хранит паттерны замены переменных вида /\$\{varname\}/g
	var deleteCounter = 0;
	
	
	function fileinputOnChange(event){

		console.log(event);
		
		var $this = $(event.target);		
		var $textContainer = $this.siblings('.fake-btn');
		var filesCount = $this[0].files.length;
		
		
		if (filesCount > 0) {

			var fileName = $this.val().split('\\').pop();
			console.log(fileName);
			$textContainer.text(fileName);
			console.log('from onchange: '+ event.target.files[0].size);
			var fileSize = event.target.files[0].size;
			fileSize = fileSize / 1048576;
			fileSize = fileSize.toFixed(2);
			$this.after('<a class="file-upload__delete" href="#">Удалить</a>');
			$this.after('<span class="file-upload__size">' + fileSize + ' M</span>');
			$this.siblings('a.file-upload__delete:first').click(function(event){
				removeItem(this);
				event.preventDefault();
			});
			
			$this.parents('.file-upload__group').addClass('loaded');
			$this.parents('.file-upload__area').addClass('loaded');
			
		} else {
			
			$textContainer.text('Загрузить');
		}
	}

	

	function removeItem(eventTarget){
		var $this = $(eventTarget);
		var $fg = $this.parents('.file-group:first');
		
		if ($this.data('fileId')){					
			if ($('#input-delete-'+$this.data('fileId')).length == 0){
				$fg.append(
					'<input id="#input-delete-'+$this.data('fileId')+'" type="hidden" name="deleted['+deleteCounter+']" value="'+$this.data('fileId')+'">'
				);
				deleteCounter++;
			}
		}
		console.log('removeItem: '+$fg);
		$fg.find('.loaded').removeClass('loaded');
		$fg.find('.file-upload__size,.file-upload__delete').remove();
		$fg.find('input[type="file"]').val('').change();
	}
	

	
	var methods = {
		init: function(options){
			
			options = $.extend({
				// options
				
			}, options);
			var $this = $(this);
			var pluginElementId = $this.attr('id');
			var $items = $('#'+pluginElementId+' .multiple-list__item');
			
			//	Сперва ищем есть ли уже какие-либо "срендеренные" сервером
			//	элементы и если есть, то устанавливаем значение counter
			
			if ($items.length > 0){
				
				var values = $items.map(function(){
					return parseInt($this.data('item-id')) || 0;
				}).toArray();
				//values = 1 + Math.max.apply(Math, values);
				//if (values > -Infinity && values > counter){
				values = values.length;
					counter = values;
				//}
				console.log('#'+pluginElementId+' .multiple-list__item', counter, values);
			}
			
			
			$('.add.add_item[href="#'+pluginElementId+'"]').on('click', function(event){
				
				var $this = $(this);
				var $list = $('#'+pluginElementId)
				var replacements = options.replacements;
				var newElemId = 'item-'+replacements.varname+'-'+counter;
				
				if ($list.find('.multiple-list__item').length >= parseInt($(this).data('maxLimit'))){
					return false;
				}
				
				if (options.hasOwnProperty('counterName')){
					replacements[options.counterName] = counter++;
				}
				$list.append(
					getItemTemplateByName(options.templateContentName, replacements)
				);
				console.log('newElemId: '+newElemId);
				$('.remove.remove_item[href="#'+newElemId+'"]', this).click(function(event){
					var $this = $(this);
					var id = $this.attr('href').replace('#', '');
					$('#'+id).slideUp("fast" , function(){
						$(this).remove();
					});					
					event.preventDefault();
				});
								
				$('#'+newElemId).find('.file-input').on('change', fileinputOnChange);
				$('#'+newElemId+' a.file-upload__delete').click(function(event){
					console.log(event);
					removeItem(this);
					event.preventDefault();
				});
				
				event.preventDefault();
			});
			
			return this;
		}
	};
	
	function getRe(varname){
		if (!re.hasOwnProperty(varname)){
			re[varname] = new RegExp('\\$\\{'+varname+'\\}', 'g');
		}	
		return re[varname];		
	}

	function getItemTemplateByName(tmplName, replacements) {
		var html = $('template[content="'+tmplName+'"]:first').html();
		for (key in replacements){
			console.log(getRe(key)+' : '+replacements[key]);
			html = html.replace(getRe(key), replacements[key]);
		}			
		return html;
	}

	$.fn.multipleFormGroup = function(params){
		if (methods[params]){
			return methods[params].apply(this, Array.prototype.slice.call(arguments, 1));
		}else if ( typeof params === 'object' || !params) {
			return methods.init.apply(this, arguments);
		}
		console.info('Метод не существует.');
	};
	$(function(){
		$('#diploma-list').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'education'
			}
		});
		$('#otherdoc-list').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'rest'
			}
		});
		$('#privilege-list_0').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_0'
			}
		});
		$('#privilege-list_1').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_1'
			}
		});
		$('#privilege-list_2').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_2'
			}
		});
		$('#privilege-list_3').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_3'
			}
		});
		$('#privilege-list_4').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_4'
			}
		});
		$('#privilege-list_5').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_5'
			}
		});
		$('#privilege-list_6').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_6'
			}
		});
		$('#privilege-list_7').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_7'
			}
		});
		$('#privilege-list_8').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_8'
			}
		});
		$('#privilege-list_9').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'privilege_9'
			}
		});
		$('#compatriot-list').multipleFormGroup({
			templateContentName: 'item',
			counterName: 'id',
			replacements: {
				varname: 'compatriot'
			}
		});

		$('button[name="button_send"]').click(function(){
			
			if ($('#passport-0').parents('.file-group:first').data('oldBrowserStatus') == '' && 
				$('#passport-1').parents('.file-group:first').data('oldBrowserStatus') == ''){
				console.log('declineSubmit');
				$('#declineSubmit').modal('show');
				event.preventDefault();
				return false;
			}
			var total_size = 0;
			$('input[type="file"]').each(function(index, element) {
				file = element.files[0];
				total_size += file.size;
			});
			if (total_size > 200 * 1024 * 1024) {
				alert('Общий объем загружаемых файлов не должен превышать 200 Мб');
				return false;
			}
		});
		
		$('.file-input').on('change', fileinputOnChange);
		$('.file-upload__delete').click(function(event){
			removeItem(this);
			event.preventDefault();
		});		
	});
	
	
})(jQuery);