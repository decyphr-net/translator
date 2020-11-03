const inputEditor = ace.edit("source-language-editor");
    inputEditor.setTheme("ace/theme/monokai");
    inputEditor.session.setMode("ace/mode/html");

    document.getElementById("source-language-editor").style.fontSize = "22px";
    document.getElementById("source-language-editor").querySelector(".ace_text-input").name = "input";
    inputEditor.setShowPrintMargin(false);
    inputEditor.getSession().setUseWrapMode(true);
    inputEditor.setOption("indentedSoftWrap", false);

    const outputEditor = ace.edit("target-language-editor");
    outputEditor.setTheme("ace/theme/monokai");
    outputEditor.session.setMode("ace/mode/html");

    document.getElementById("target-language-editor").style.fontSize = "22px";
    outputEditor.setShowPrintMargin(false);
    outputEditor.getSession().setUseWrapMode(true);
    outputEditor.setOption("indentedSoftWrap", false);

    function submit() {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      let data = {
        "text": inputEditor.getValue(),
        "source": document.querySelector("select[name='source']").value,
        "target": document.querySelector("select[name='target']").value
      }
      
      fetch("/translate", {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
      }).then(function(response) {
        return response.json();
      }).then(function(data) {
        outputEditor.setValue(data.translated_text, -1)
      });

      
    }