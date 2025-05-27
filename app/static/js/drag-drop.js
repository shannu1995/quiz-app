const matches = {}
document.querySelectorAll(".draggable").forEach(draggable => {
    draggable.addEventListener('dragstart', (e) =>{
        e.dataTransfer.setData('text', draggable.id)
    })
});
document.querySelectorAll('.droppable').forEach(droppable => {
    droppable.addEventListener('dragover', event => event.preventDefault());

    droppable.addEventListener('drop', event => {
        const draggedId = event.dataTransfer.getData('text');
        matches[droppable.dataset.match] = draggedId;
        droppable.textContent += ` (Selected: ${draggedId})`;
    });
});

function submitResults() {
    fetch('/submit_results', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(matches)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    });
}