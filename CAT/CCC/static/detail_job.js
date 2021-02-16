var id;
$('#detailModal').on('show.bs.modal', function (event) {

  var button = $(event.relatedTarget)
  var branch = button.data('job_branch') 
  var build_time = button.data('job_time')
  var modules = button.data('job_modules')
  id = button.data('job_id')

  var modal = $(this)

  var title = "Branch - " + branch + '<br>'
  title += "Build Time - " + build_time
  modal.find('.modal-title').html(title)

  tbody = modal.find('.modal-body table tbody')
  tbody_html = ''
  modules = modules.split(' ').slice(0, -1);
  for (var i=0; i<modules.length; i++) {
    let module = modules[i].split('_');
    let module_name = module[0];
    let module_tag = module[1];
    let module_hash = module[2];
    let module_id = module[3];
    let loop = i + 1

    tbody_html += '<tr><td>' + loop + '</td>'
    tbody_html += '<td>' + module_name + '</td>'
    tbody_html += '<td>' + module_tag + '</td>'
    tbody_html += '<td>' + module_hash + '</td>'
    tbody_html += '<td>\
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="deleteModule(' + id + ',' + module_id + ')">\
        delete</button></td></tr>'
  }
  tbody.html(tbody_html)
});

function deleteModule(job_id, module_id) {
  $.ajax({
    url: job_id + '/abort/' + module_id + '/',
    type: "POST",
    data: { job_id : job_id, module_id : module_id },
    success: function(data) {
      alert_message = $(detailModal).find('.footer-alert-messages')
      messages = data['messages']
      if (messages['type'] === 'warning') {
        alert_message.html("<div class='alert alert-warning' role='alret'>" + messages['content'] +"</div>");
      } else {
        alert_message.html("<div class='alert alert-success' role='alret'>" + messages['content'] +"</div>");

        $('.modal-body').load(job_id+'/detail/', function (response, status, xhr) {
          if (status === "success") {
              $(".modalBody").modal('show');
          }
        });
      }
    },
    error: function(request,status,error){
      alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    }
  });
}

$('#detailModal').on('shown.bs.modal', function (event) {
  console.log("shown")
});

$('#detailModal').on('hidden.bs.modal', function (event) {
  console.log("hidden")
});

$('#detailModal').on('loaded.bs.modal', function (event) {
  console.log("loaded")
});

$('#detailModal').on('hide.bs.modal', function (event) {
  console.log("modal close");
  alert_message = $(this).find('.footer-alert-messages')
  alert_message.html('');
  var close_form = document.detailCloseForm[0];
  close_form.action = "";
  close_form.method = "post";
  close_form.submit();
  // var name = module_form.module_name.value
  // var tag = module_form.module_tag.value
  // var hash = module_form.module_hash.value
});

$('#detailAdd').on('click', function(event) {
  $.ajax({
    url: id+'/',
    type: "POST",
    data: $("#moduleAddForm").serialize(),
    success: function(data) {
      alert_message = $(detailModal).find('.footer-alert-messages')
      messages = data['messages']
      if (messages['type'] === 'warning') {
        alert_message.html("<div class='alert alert-warning' role='alret'>" + messages['content'] +"</div>");
      }
      else {
        alert_message.html("<div class='alert alert-success' role='alret'>" + messages['content'] +"</div>");

        $('.modal-body').load(id+'/detail/', function (response, status, xhr) {
          if (status === "success") {
              $(".modalBody").modal('show');
          }
        });
      }
    },
    error: function(request,status,error){
      alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    }
  });
});