var reloadable = null;
var messageTimeout = null

document.addEventListener("DOMContentLoaded", function(e) {

});

function scrollIntoViewWithOffset(element){
  window.scrollTo({
    behavior: 'smooth',
    top:
      element.getBoundingClientRect().top -
      document.body.getBoundingClientRect().top
  })
}

function request(method, url, callback, data){
    const token = localStorage.getItem('token');
    var headers = {'Accept': 'application/json'}
    if(token) headers['Authorization'] = 'Token '+token;
    url = url.replace(document.location.origin, '');
    if(url.indexOf(API_URL) == -1) url = API_URL + url;
    var params = {method: method, headers: new Headers(headers)};
    if(data) params['body'] = data;
    var httpResponse = null;
    var contentType = null;
    fetch(url, params).then(
        function (response){
            httpResponse = response;
            contentType = httpResponse.headers.get('Content-Type');
            if(contentType=='application/json') return response.text();
            else if(contentType.indexOf('text')<0 || contentType.indexOf('csv')>=0) return response.arrayBuffer();
            else response.text()
        }
    ).then(result => {
            if(contentType=='application/json'){
                var data = JSON.parse(result||'{}');
                if(data.token){
                    localStorage.removeItem("application");
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', data.user.username);

                }
                if(data.redirect){
                    if(data.message) setCookie('message', data.message);
                    document.location.href = data.redirect;
                } else {
                    if(data.message && !data.task)  showMessage(data.message);
                    callback(data, httpResponse);
                }
            } else if(contentType.indexOf('text')<0 || contentType.indexOf('csv')>=0){
                var file = window.URL.createObjectURL(new Blob( [ new Uint8Array(result) ], { type: contentType }));
                var a = document.createElement("a");
                a.href = file;
                if (contentType.indexOf('excel') >= 0) a.download = 'Download.xls';
                else if (contentType.indexOf('pdf') >= 0) a.download = 'Download.pdf';
                else if (contentType.indexOf('zip') >= 0) a.download = 'Download.zip';
                else if (contentType.indexOf('json') >= 0) a.download = 'Download.json';
                else if (contentType.indexOf('csv') >= 0) a.download = 'Download.csv';
                else if (contentType.indexOf('png') >= 0) a.download = 'Download.png';
                document.body.appendChild(a);
                a.click();
                callback({}, httpResponse);
            } else {
                callback(result, httpResponse);
            }
        }
    );
}

function closeDialogs(){
    var dialogs = document.getElementsByTagName('dialog');
    for(var i=0; i<dialogs.length; i++){
        var dialog = dialogs[i];
        dialog.close();
        dialog.classList.remove('opened');
        dialog.remove();
        $('.layer').hide();
        if(window.reloader) window.reloader();
    }
}

function initialize(element){
    if(!element) element = document;
    var message = getCookie('message');
    if(message){
        showMessage(message);
        setCookie('message', null);
    }
    $(element).find("input[type=file]").each(function(i, input) {
        input.addEventListener('change', function (e) {
            if (e.target.files) {
                let file = e.target.files[0];
                if(['png', 'jpeg', 'jpg', 'gif'].indexOf(file.name.toLowerCase().split('.').slice(-1)[0])<0) return;
                var reader = new FileReader();
                reader.onload = function (e) {
                    const MAX_WIDTH = 400;
                    var img = document.createElement("img");
                    img.id = input.id+'img';
                    img.style.width = 200;
                    img.style.display = 'block';
                    img.style.marginLeft = 300;
                    img.onload = function (event) {
                        const ratio = MAX_WIDTH/img.width;
                        var canvas = document.createElement("canvas");
                        const ctx = canvas.getContext("2d");
                        canvas.height = canvas.width * (img.height / img.width);
                        const oc = document.createElement('canvas');
                        const octx = oc.getContext('2d');
                        oc.width = img.width * ratio;
                        oc.height = img.height * ratio;
                        octx.drawImage(img, 0, 0, oc.width, oc.height);
                        ctx.drawImage(oc, 0, 0, oc.width * ratio, oc.height * ratio, 0, 0, canvas.width, canvas.height);
                        oc.toBlob(function(blob){
                            input.blob = blob;
                        });
                        input.parentNode.appendChild(img);

                    }
                    img.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    });
    $(element).find(".async").each(function(i, div) {
        fetch(div.dataset.url).then(
            function(response){
                response.text().then(
                    function(html){
                        var parser = new DOMParser();
                        var doc = parser.parseFromString(html, 'text/html');
                        var div2 = doc.getElementById(div.id)
                        div.innerHTML = div2.innerHTML;
                    }
                )
            }
        );
    });
}

function copyToClipboard(value){
    navigator.clipboard.writeText(value);
    showMessage('"'+value+'" copiado para a área de transferência!');
}

function setInnerHTML(elm, html) {
  elm.innerHTML = html;

  Array.from(elm.querySelectorAll("script"))
    .forEach( oldScriptEl => {
      const newScriptEl = document.createElement("script");

      Array.from(oldScriptEl.attributes).forEach( attr => {
        newScriptEl.setAttribute(attr.name, attr.value)
      });

      const scriptText = document.createTextNode(oldScriptEl.innerHTML);
      newScriptEl.appendChild(scriptText);

      oldScriptEl.parentNode.replaceChild(newScriptEl, oldScriptEl);
  });
}

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  if(cvalue==null) exdays = 0;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function hideMessage(){
    if(messageTimeout){
        clearTimeout(messageTimeout);
        messageTimeout = null;
    }
    var feedback = document.querySelector(".notification");
    if(feedback) feedback.style.display='none';
}
function showMessage(text, style){
    hideMessage();
    var feedback = document.querySelector(".notification");
    feedback.innerHTML = text;
    feedback.classList.remove('danger');
    feedback.classList.remove('success');
    feedback.classList.remove('warning');
    feedback.classList.remove('info');
    feedback.classList.add(style||'success');
    feedback.style.display='block';
    messageTimeout = setTimeout(function(){feedback.style.display='none';}, 5000);
}
