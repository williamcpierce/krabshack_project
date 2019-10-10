"use strict";
var KTDatatablesAdvancedFooterCalllback = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');
		// begin first table
		table.DataTable({
		    scrollResize: true,
		    scrollX: true,
		    scrollY: 100,
		    scrollCollapse: true,
		    paging: false,
		    info: false,
		});
	};

	return {

		//main function to initiate the module
		init: function() {
			initTable1();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesAdvancedFooterCalllback.init();
});

$('#filterField').keyup(function(){
      $('#kt_table_1').DataTable().search($(this).val()).draw() ;
});
