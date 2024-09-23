$(function() {

	/*modalWindow*/
	$('#myModal').on('shown.bs.modal', function () {
	  $('#myInput').trigger('focus')
	})


	/*datepicker*/
	if ($( ".form__input_date" ).length > 0)
		$( ".form__input_date" ).datepicker({
			changeMonth: true,
			changeYear: true,
			yearRange: "c-60:c+60",
			showOn: "both",
			buttonImage: "/static/img/calendar-alt-regular.png",
			buttonImageOnly: true,
			buttonText: "Select date",
		});

	if ($( ".form__input_date" ).length > 0)
		$( ".form__input_date" ).datepicker( $.datepicker.regional[ "ru" ] );

	$(function() {
		$('.form__input_date').each(function() {
			var input = this;
			$(input).attr('maxlength','10');
			var dateInputMask = function dateInputMask(elm) {
			  elm.addEventListener('keypress', function(e) {
			    if(e.keyCode < 47 || e.keyCode > 57) {
			      e.preventDefault();
			    }
			    
			    var len = elm.value.length;
			    
			    // If we're at a particular place, let the user type the slash
			    // i.e., 12/12/1212
			    if(len !== 1 || len !== 3) {
			      if(e.keyCode == 47) {
			        e.preventDefault();
			      }
			    }
			    
			    // If they don't add the slash, do it for them...
			    if(len === 2) {
			      elm.value += '.';
			    }

			    // If they don't add the slash, do it for them...
			    if(len === 5) {
			      elm.value += '.';
			    }
			  });
			};
			  
			dateInputMask(input);
		});
	});

	/*datepicker*/

	/*inputmask*/

	var dangerSpan = ('<span class="form__question" title="Ошибка в заполнении формы. Нажмите для получения подробной информации." data-toggle="modal" data-target="#exampleModal"><i class="fa fa-question-circle" aria-hidden="true"></i></span>');
	var item = '';

	function addDangerSpan() {
		if($(item).val().length > 0)  {
			item.parents('.form-group').addClass('form-group_danger');
			item.prev('label').append(dangerSpan);
		}	else {
			item.parents('.form-group').removeClass('form-group_danger');
			item.prev('label').children('.form__question').remove();
		}
	}

	function removeDangerSpan() {
		item.parents('.form-group').removeClass('form-group_danger');
		item.prev('label').children('span.form__question').remove();
	}
/*
	$("#personalinfoform-passport").inputmask({
		autoUnmask: true,
		mask: "99 99 999999",
		onincomplete: function() {
			item = $(this);
			addDangerSpan();
		},
		oncomplete: function() {
			item = $(this);
			removeDangerSpan();
		}
	});
*/
	$(".phone-number").inputmask({
		autoUnmask: true,
		mask: "+9 (999)999-99-99{1,10}",
		onincomplete: function() {
			item = $(this);
			addDangerSpan();
		},
		oncomplete: function() {
			item = $(this);
			removeDangerSpan();
		}
	});
/*
	$("#personalinfoform-issued_code").inputmask({
		autoUnmask: true,
		mask: "999-999",
		onincomplete: function() {
			item = $(this);
			addDangerSpan();
		},
		oncomplete: function() {
			item = $(this);
			removeDangerSpan();
		}
	});
*/
	$("#personalinfoform-zipcode").inputmask({
		autoUnmask: true,
		mask: "999999",
		onincomplete: function() {
			item = $(this);
			addDangerSpan();
		},
		oncomplete: function() {
			item = $(this);
			removeDangerSpan();
		}
	});

	$(".form__input_point").inputmask({
		autoUnmask: true,
    rightAlign: false,
		mask: "9{0,3}",
    definitions: {
      '*': {
        validator: "[0-9]",
      }
    },
  });

  

	/*inputmask*/

});

	  
	