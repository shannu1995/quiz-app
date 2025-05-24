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
    fetch('/check_matches', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(matches)
    })
    .then(response => response.json())
    .then(data => {
        alert(`Score: ${data.correct} out of ${data.total}`);

        document.querySelectorAll('.droppable').forEach(droppable => {
            const actualMatch = droppable.dataset.match;
            const userChoice = matches[actualMatch];
            
            if (userChoice === actualMatch) {
                droppable.style.backgroundColor = '#4CAF50';
            } else {
                droppable.style.backgroundColor = '#F44336';
            }
        });
    });
}