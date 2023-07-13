$.fn.extend({
  AutoTable: function (config) {
    const wrapper = $('.auto-table-wrapper')
    const templateContainer = $('#template-container')
    const djangoConfig = JSON.parse($('#datatables-config').text())
    const layoutConfig = JSON.parse($('#layout-config').text())
    const field_options = JSON.parse($.ajax({
        type: "OPTIONS",
        url: this.data('ajax'),
        async: false
    }).responseText)['data'];
    

    $(this).find('th').each(function (index, element) {
      console.log($(element).data())
    })

    console.log(field_options)

    var choice_fields = {}
    field_options.forEach((o) => { if (o["choices"]) { choice_fields[o["key"]] = o } })



    if ($("#template")) {
      extraConfig = {
          initComplete: function(settings, json) {
            // show new container for data
            templateContainer.insertBefore('#template-container');
            templateContainer.show();
          },
          rowCallback: function( row, data ) {
              // on each row callback
            var template = $("#template").clone().children().first()
            $.each(data, function(key, val){
              template.find(".data-" + key).html($.parseHTML( val ));
            });

            template.appendTo(templateContainer);
          },
          preDrawCallback: function( settings ) {
              // clear list before draw
              templateContainer.empty();
          },
      }
    }

    return $(this).DataTable( {
      ...djangoConfig,
      ...config,
      ...extraConfig,
      // responsive: true,
      columnDefs: [

        // { "width": "20%", "targets": "_all" },
        // {
        //   targets: '_all',
        //   render: function ( data, type, row, meta ) {
        //     return data
        //   }
        // },
        {
          targets: 'status',
          render: function ( data, type, row, meta ) {
            return choice_fields['status']["choices"].find((o) => { return o["value"] === data })["label"]
          }
        },
      ],
      initComplete: function(settings, json) {
        wrapper.addClass('loaded')
        $.each( layoutConfig, function( key, value ) {
          $(key).appendTo($(value))
        });
      },
     } );
  }
});

// $(function () {

//   const templateContainer = $('#template-container')
//   const config = JSON.parse(document.getElementById('datatables-config').textContent)
//   var extraConfig = {}
//   if ($("#template")) {
//     extraConfig = {
//         initComplete: function(settings, json) {
//           // show new container for data
//           templateContainer.insertBefore('#example');
//           templateContainer.show();
//           $('#DataTables_Table_0_info').appendTo($('#appFooter'))
//         },
//         rowCallback: function( row, data ) {
//             // on each row callback
//           var template = $("#template").clone().children().first()
//           $.each(data, function(key, val){
//             template.find(".data-" + key).text(val);
//           });

//           template.appendTo(templateContainer);
//         },
//         preDrawCallback: function( settings ) {
//             // clear list before draw
//             templateContainer.empty();
//         },
//         "createdRow": function( row, data, dataIndex ) {
//           // if ( data[4] == "A" ) {
//             // $(row).addClass( 'bg-primary' );
//           // }
//         }
//     }
//   }


//   var table = $(".datatable").DataTable( {
//     ...config,
//     ...extraConfig,

//  } );

// new $.fn.dataTable.Buttons(table, {
  // buttons: [
  //   {
  //     extend: 'print',
  //     // text: 'Print',
  //     autoPrint: false,
  //     footer: true,
  //     customize: function (win, config, table) {
  //       $(win.document.body).append(templateContainer.clone());
  //       $(win.document.body).append($("#appFooter").clone());
  //     },
  //     exportOptions: {
  //         columns: ':not(.noPrint) :visible'
  //     },
  //     messageBottom: "This is a custom message added to the print view",
  //   },
  //   {
  //     extend: 'collection',
  //     text: 'Export',
  //     buttons: [ 
  //       {
  //         extend: 'csv',
  //         exportOptions: {
  //             columns: ':not(.noPrint) :visible'
  //         }
  //       },
  //       {
  //         extend: 'excel',
  //         exportOptions: {
  //             columns: ':not(.noPrint) :visible'
  //         }
  //       },
  //       {
  //         extend: 'pdf',
  //         exportOptions: {
  //             columns: ':not(.noPrint) :visible'
  //         }
  //       },
  //     ],
  //   },
  //   {
  //     extend: 'colvis',
  //     text: 'Columns',
  //     collectionLayout: 'fixed columns',
  //     collectionTitle: 'Column visibility control',
  //     columns: ':not(.noVis)'
  // },
//   ],
// });

//  table.buttons().container().appendTo( $('.application-menu .btn-toolbar') );

// });