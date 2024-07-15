function clearPreviewContainer() {
    const previewContainer = document.getElementById("image-preview");
    const fileMedia = document.getElementById("id_media");
    previewContainer.innerHTML = "";
    fileMedia.value = "";
}

function clearForm() {
    clearPreviewContainer();
    if (document.getElementById("post_content")) {
        const postContent = document.getElementById("post_content");
        postContent.value = "";
    }
}
