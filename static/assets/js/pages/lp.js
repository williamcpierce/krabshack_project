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
			footerCallback: function(row, data, start, end, display) {

				var api = this.api();
				var i, column, columnArray = [1, 2, 3], len = columnArray.length;
				for (i=0; i<len; ++i) {
					
					column = columnArray[i];

					// Remove the formatting to get integer data for summation
					var intVal = function(val) {
						return typeof val === 'string' ? val.replace(/[\$,]/g, '') * 1 : typeof val === 'number' ? val : 0;
					};

				    $( api.column( column ).footer() ).html(
				        "<div align='right'>" +
				        api.column( column ).data().reduce( function ( a, b ) {
				            return KTUtil.numberString((intVal(a) + intVal(b)).toFixed(0));
				        }, 0 ) +
				        "</div>"
				    );
				};
			}
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
