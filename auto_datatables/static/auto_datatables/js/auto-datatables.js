

String.prototype.format = function(params) {
  const names = Object.keys(params);
  const vals = Object.values(params);
  return new Function(...names, `return \`${this}\`;`)(...vals);
}

renderTemplate = function ( template ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      return template.format(row)
    }
    // Search, order and type can use the original data
    return data;
  };
};

renderChoices = function ( choices ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      return choices.find((o) => { return o["value"] === data })["label"]
    }
    // Search, order and type can use the original data
    return data;
  };
};

renderBoolean = function ( data, type, row ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      return data === true ?
                '<i class="fas fa-check text-success"><span style="display:none">' + data + '</span></i>' :
                '<i class="fas fa-times text-danger"><span style="display:none">' + data + '</span></i>';
    }
    // Search, order and type can use the original data
    return data;
  };
};



getKeys = function (array) { 
  return array.map((o) => { return o["key"] })
 }


function autoColumnDefs (metadata, config) {
  columnDefs = []

  // group metadata objects by type
  var metadata_by_type = {}
  metadata.forEach((o) => { metadata_by_type[o["type"]] = metadata_by_type[o["type"]] || []; metadata_by_type[o["type"]].push(o) })


  // build column defs for select fields if there are any
  if (metadata_by_type["select"]) {
    // we need to add them indidually because each render function takes a different set of choices
    select_fields.forEach((field) => {
      columnDefs.push({
        targets: field["key"],
        render:  renderChoices(field["choices"])
      })
    })
  }

  if (metadata_by_type["email"]) {
    template = config.email_template || '<a href="mailto:${email}"><i class="fa-solid fa-envelope"></i></a>';
    columnDefs.push({
      targets: getKeys(metadata_by_type["email"]),
      render: renderTemplate(template)
    })
  }

  if (metadata_by_type["checkbox"]) {
    columnDefs.push({
      targets: getKeys(metadata_by_type["checkbox"]),
      render: renderBoolean()
    })
  }

  if (metadata_by_type["datetime"]) {
    columnDefs.push({
      targets: getKeys(metadata_by_type["datetime"]),
      render: DataTable.render.datetime("Do MMM YYYY")
    })
  }

  template = {
    first_name: "<a href='/users/${id}/'>${first_name}</a>",
  }
  if (template) {


    $.each(template, function (key, val) {
      columnDefs.push({
        targets: key,
        render:  renderTemplate(val)
      })
    })
  }

  return columnDefs

}

$.fn.extend({
  AutoTable: function (config) {
    const wrapper = $('.auto-table-wrapper')
    const templateContainer = $('#template-container')
    const djangoConfig = JSON.parse($('#datatables-config').text())
    const layoutConfig = JSON.parse($('#layout-config').text())

    const rowTemplate = String($('#row-template').text())
    const metadata = JSON.parse($.ajax({
        type: "OPTIONS",
        url: this.data('ajax'),
        async: false
    }).responseText)['data'];

    if ($("#template")) {
      extraConfig = {
          initComplete: function(settings, json) {
            // show new container for data
            templateContainer.insertBefore('#template-container');
            templateContainer.show();
          },
          rowCallback: function( row, data ) {
            templateContainer.append(rowTemplate.format(data))
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
        ...autoColumnDefs(metadata, config),
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