var preview = CKEDITOR.document.getById( 'preview' );

function syncPreview() {
    preview.setHtml( editor.getData() );
}

var editor = CKEDITOR.replace( 'id_text', {
    on: {
        // Synchronize the preview on user action that changes the content.
        change: syncPreview,

        // Synchronize the preview when the new data is set.
        contentDom: syncPreview
    }
} );