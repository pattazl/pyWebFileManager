$(document).ready(function () {
  // init fancybox to view images
  $("a.fancyLink").fancybox({
    openEffect: 'fade',
    prevEffect: 'fade',
    nextEffect: 'fade'
  });
  // and for movies
  $("a.fancyMovie").fancybox({
    minWidth: 640,
    minHeight: 480,
    type: 'iframe'
  });

  // when mouse enter the table : display buttons
  $(".table tr").on('mouseenter', function () {
    var overlay = $(this).find('span.overlay');
    overlay.css('visibility', 'visible');
  });


  // when mouse leave the table : remove buttons
  $(".table tr").on('mouseleave', function () {
    var overlay = $(this).find('span.overlay');
    overlay.css('visibility', 'hidden');
  });


  // on delete : triggered when modal is about to be shown
  $('#deleteModal').on('show.bs.modal', function (event) {
    // get data attribute of the clicked element
    var filePath = $(event.relatedTarget).data('delete-file-path');
    var lineId = $(event.relatedTarget).data('line-id');
    // populate textbox
    let showTxt = $('#inputId'+lineId).val()
    $(event.currentTarget).find('span[id="fileName"]').text(showTxt) ; //(filePath.split('/').slice(-1));
    $(event.currentTarget).find('span[id="filePath"]').text(filePath);
    $(event.currentTarget).find('span[id="lineId"]').val(lineId);
  });


  // on delete : when clicks "yes" from modal
  $('#deleteFile').on('click', function (event) {
    // hide modal, get line id, remove line from table
    $('#deleteModal').modal('hide');
    var lineId = $('#lineId').val();
    thisRow = $('.table tr[id=' + lineId + ']').remove();
    // and trigger file removal
    var filePath = $('#filePath').text();
    $.ajax({
      url: "delete?path=" + filePath,
      context: document.body
    });
  });


  // renaming : disable renaming mode
  var disableRenaming = function (linkId) {
    $('.no-href').attr('class', '');                // remove no-href class
    $('.no-input').attr('class', 'hidden');         // remove no-input class
    $('.no-overlay').css('visibility', 'hidden');   // restore hidden class
    $('.no-overlay').attr('class', 'overlay');      // remove no-overlay class
    // reset input field
    originLink = $('#href' + linkId).text();
    inputArea = $('#input' + linkId);
    inputArea.val(originLink);
  }


  // renaming
  var renamingProcess = function (itemId, srcPath, dstPath) {
    // don't uselessly send request
    if (srcPath == dstPath) {
      return;
    }
    // display loading gif
    showHideLoading(".no-input");
    // send request
    $.ajax({
      url: "rename?itemId=" + itemId + "&srcPath=" + srcPath + "&dstPath=" + dstPath+"&currPath=" + currPath.value,
      context: document.body,
      error: function (result, statut, error) {
        // remove spinner, display message
        showHideLoading();
        displayAlertBox('<strong>Error!</strong> Could not rename this element : something went wrong.');
      },
      complete: function (http_code, statut) {
        // after success/error : remove loading gif
        showHideLoading();
        // update icon, based on file type
        var jsonData = jQuery.parseJSON(http_code.responseText);
        $('#href' + jsonData['itemId'] + ' i').attr('class', 'fa fa-' + jsonData['filetype']);
        if((jsonData.error||'')!='')
        {
          displayAlertBox(jsonData.error)
        }
      }
    });
  }

  // display or hide loading gif
  var showHideLoading = function (selector) {
    if ($("#loading").size() == 0) {
      $(selector).after('<i class="fa fa-spinner fa-spin" alt="loading" id="loading"></i>')
    } else {
      $("#loading").remove();
    }
  }

  var displayAlertBox = function (message) {
    $('#alertMarker').after('<div class="alert alert-warning alert-dismissible" role="alert" id="alertBox">'
      + '<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'
      + message
      + '</div>');
  }

  // renaming : click to rename
  $('.renameElement').on('click', function (event) {
    // disable previous renaming
    disableRenaming();

    // new renaming
    var elementPath = $(this).attr('data-element-path');
    var linkId = $(this).attr('data-link-id');
    $('#href' + linkId).attr('class', 'hidden no-href');      // hide link
    $('#input' + linkId).attr('class', 'no-input');           // enable input
    $('#input' + linkId).select();                            // select text
    $('#overlay' + linkId).attr('class', 'no-overlay hidden');// disable overlay

    // add handler : when leaving input the input field
    $('#input' + linkId).focusout(function () {
      disableRenaming(linkId);
    });

    // add handler : when pressing [ENTER] or [ESC]
    $('#input' + linkId).keypress(function (event) {
      // when [ENTER] is pressed : validate
      if (event.which == 13 || event.keyCode == 13) {
        // get previous name and new name
        srcPath = $('#href' + linkId).text();
        dstPath = $('#input' + linkId).val();
        // rename
        renamingProcess(linkId, srcPath, dstPath);
        // change name on href link
        inputArea = $('#input' + linkId);
        prefixIcon = '<i class="fa fa-file-o" style="margin-right: 5px; color: #000"></i>';
        $('#href' + linkId).html(prefixIcon + inputArea.val());
        // remove input
        disableRenaming(linkId);
      }
      // when [ESC] is pressed : cancel everything
      else if (event.which == 27 || event.keyCode == 27) {
        disableRenaming(linkId);
      }
    });
  });
  // CHANGE NAV link style
  let linkTxt = $('#navlink').html()
  let arr = linkTxt.split('/');
  let arrLink = ['<a href="?path=/#"> / </a>'];
  let preLink = ''
  for (let k of arr) {
    if (k == '') {
      continue
    };
    preLink += '/' + k
    let link = `<a href="?path=${preLink}#">${k}</a>`
    arrLink.push(link)
  }
  $('#navlink').html(arrLink.join('/'))
  // search event
  // convert the size
  document.getElementsByName('fileSizeList').forEach(x=>{
    let size = x.innerHTML ;
    x.innerHTML = renderSize(size)
    x.title = size + ' Bytes'
  })
});
// ajax get foloder size
async function getSize(path, obj) {
  if (obj.handle != null) {
    return;
    //clearInterval(obj.handle)
  }
  let count = 1, maxLen = 7;
  obj.title = '';
  obj.handle = setInterval(function () {
    obj.innerHTML = '.'.repeat(count++ % maxLen).padEnd(maxLen, ' ')
  }, 500)
  let res = await fetch(`getFolderSize?path=${path}`).then(res => {
    return res.json()
  }).catch(err => {
    obj.innerHTML = 'search Error!'+err.message
  })

  clearInterval(obj.handle)
  obj.handle = null

  if (res?.data != null) {
    if (res.data.length == 0) {
      obj.innerHTML ='Not Found!'
    } else {
      obj.innerHTML = renderSize(res.data)
      obj.title = res.data+' Bytes'
    }

  }
}
// 

async function searchFiles(path, obj) {
  if (event.which == 13) {
    if (obj.handle != null) {
      return;
      //clearInterval(obj.handle)
    }
    let hint = $('#alertMarker'); // .html(`${path} search ${val}`)
    let count = 1, maxLen = 15;
    let val = obj.value.trim()
    if (val == '') {
      hint.html('')
      return
    }
    obj.handle = setInterval(function () {
      hint.html('.'.repeat((count++ % maxLen) + 1).padEnd(maxLen, ' '))
    }, 500)
    // search?path=/views/static&key=main
    let res = await fetch(`search?path=${path}&key=${val}`).then(res => {
      return res.json()
    }).catch(err => {
      hint.html('search Error!'+err.message)
    })

    clearInterval(obj.handle)
    obj.handle = null

    if (res?.data != null) {
      if (res.data.length == 0) {
        hint.html('Not Found!')
      } else {
        let count = res?.msg?.count??0, max = res?.msg?.max??0;
        hint.html(`<div style="color:${count>=max?'red':'blue'}">Found ${count}/${max}</div>${res.data.join('<br>')}`)
      }

    }
  }
}
//
function uploadFile()
{
  if(myFile.value=='')
  {
    alert('please select file!')
    return false
  }
  uploadFileName.value = (myFile.value.split(/[/\\]/g).pop())
  return true
}
/// <summary>
/// 格式化文件大小的JS方法
/// </summary>
/// <param name="filesize">文件的大小,传入的是一个bytes为单位的参数</param>
/// <returns>格式化后的值</returns>
function renderSize(filesize){
  if(null==filesize||filesize==''){
      return "0 B";
  }
  var unitArr = new Array("B","KB","MB","GB","TB","PB","EB","ZB","YB");
  var index=0;
  var srcsize = parseFloat(filesize);
  index=Math.floor(Math.log(srcsize)/Math.log(1024));
  var size =srcsize/Math.pow(1024,index);
  size=size.toFixed(2);//保留的小数位数
  return size+unitArr[index];
}