    tinymce.init({
        menubar: false,
        plugins: ["code media lists table"],
        selector:"textarea",
        theme: 'modern',
        skin: "lightgray",
        toolbar: ["formatselect fontsizeselect undo redo bold italic underline strikethrough alignleft aligncenter alignright alignjustify", "table bullist numlist outdent indent media code"],
        // valid_elements : "p,a[href|target=_blank],strong/b,div[align],br,span",
        extended_valid_elements : "*[*]",//"math,msqrt,mroot,mfrac[bevelled],mn,mi,span[class],sup,sub,u",
    });