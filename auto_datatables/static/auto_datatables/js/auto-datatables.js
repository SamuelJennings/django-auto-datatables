
String.prototype.format = function(params) {
  const names = Object.keys(params);
  const vals = Object.values(params);
  return new Function(...names, `return \`${this}\`;`)(...vals);
}

renderTemplate = function ( template ) {
  return function ( data, type, row ) {
    if ( type === 'display' & data !== null ) {
      return template.format({'data': data, "object": row})
    }
    return data;
  };
};

renderChoices = function ( choices ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      var c = choices.find((o) => { return o["value"] === data })
      if (c === undefined) {
        return data
      }
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
                '<i class="fas fa-check text-success">✔<span style="display:none">' + data + '</span></i>' :
                '<i class="fas fa-times text-danger">✘<span style="display:none">' + data + '</span></i>';
    }
    // Search, order and type can use the original data
    return data;
  };
};



getKeys = function (array) {
  return array.map((o) => { return o["key"] })
 }

function getRenderedRowValues(obj, arr) {
  // Get the object's property names as an array
  const propNames = Object.keys(obj);

  // Iterate through the property names
  for (let i = 0; i < propNames.length; i++) {
    const propName = propNames[i];

    // Replace the object's property value with the corresponding value from the array
    obj[propName] = arr[i];
  }

  return obj;
}



function buildColumnDefs (config) {
  columnDefs = []

  // applies a template to a specific field
  $.each(config.field_templates, function (key, val) {
    columnDefs.push({
      targets: key,
      render: renderTemplate(val)
    })
  })



  const metadata = config.metadata || []

  if (metadata.length === 0) {
    return columnDefs
  }

  // group metadata objects by type
  var metadata_by_type = {}
  metadata.forEach((o) => { metadata_by_type[o["type"]] = metadata_by_type[o["type"]] || []; metadata_by_type[o["type"]].push(o) })

  // build column defs for select fields if there are any
  if (getMetadataByType(metadata, "select")) {
    // we need to add them indidually because each render function takes a different set of choices
    getMetadataByType(metadata, "select").forEach((field) => {
      columnDefs.push({
        targets: field["key"],
        render:  renderChoices(field["choices"])
      })
    })
  }

  // applies a template to a specified widget type
  $.each(config.widget_templates, function (key, val) {
    if (!getMetadataByType(metadata, key)) {
      return
    }
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, key)),
      render: renderTemplate(val)
    })
  })



  if (getMetadataByType(metadata, "checkbox")) {
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, "checkbox")),
      render: renderBoolean()
    })
  }
  if (getMetadataByType(metadata, "datetime")) {
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, "datetime")),
      render: DataTable.render.datetime(config.datetime_format)
      // render: DataTable.render.datetime(null)
    })
  }

  return columnDefs

}


function getMetadataByType (metadata, type) {
  return metadata.filter((o) => { return o["type"] === type })
}

$.fn.extend({
  AutoTable: function (config) {
    const self = this;
    const templateContainer = $(this).find(".template-container");

    const metadata = config.metadata || []
    const choiceFields = getMetadataByType(metadata, "select");

    var extraConfig = {}

    var source = $(this).find("script").first().html();
    // var source = $('#template-card').html();

    // if (config.row_template) {
    if (source) {
      var template = Handlebars.compile(source);

      extraConfig = {
          initComplete: function(settings, json) {
            // show new container for data
            templateContainer.insertBefore('#template-container');
            $(self).addClass('loaded')
            $.each( config.layout, function( key, value ) {
              $(key).appendTo($(value))
            });
            templateContainer.show();
          },
          // rowCallback: function( row, data ) {
          //   let new_data = JSON.parse(JSON.stringify(data));
          //   $.each(choiceFields, function (key, val) {
          //     var field = val["key"]
          //     new_data[field] = renderChoices(val["choices"])(new_data[field], 'display', new_data)
          //   })

          //   templateContainer.append(config.row_template.format(new_data))
          // },
          rowCallback: function( row, data ) {
            let new_data = JSON.parse(JSON.stringify(data));
            $.each(choiceFields, function (key, val) {
              var field = val["key"]
              new_data[field] = renderChoices(val["choices"])(new_data[field], 'display', new_data)
            })

            templateContainer.append(template(new_data))
          },
          preDrawCallback: function( settings ) {
              // clear list before draw
              templateContainer.empty();
          },
      }
    }

    if (config.debug) {
      console.log(config)
    }

    return $(self).find("table").DataTable( {
      ...config.datatables,
      ajax: {
        url: "/api/v1/samples/",
        headers: {
          "Accept": 'application/datatables+json',
          "Content-Type": "text/json; charset=utf-8",
        }
      },
      columnDefs: [
        ...buildColumnDefs(config),
      ],
      initComplete: function(settings, json) {
        $(self).addClass('loaded')
        $.each( config.layout, function( key, value ) {
          $(key).appendTo($(value))
        });
      },
      ...extraConfig,

     } );
  }
});


