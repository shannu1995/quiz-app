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

function resetQuiz(){
    location.reload();
};

let scrollSpeed = 10;
let autoScrollInterval = null;

document.addEventListener('dragover', (e) => {
    const threshold = 100;
    const viewportHeight = window.innerHeight;

    if (autoScrollInterval) {
        clearInterval(autoScrollInterval);
        autoScrollInterval = null;
    }

    if (e.clientY < threshold) {
        autoScrollInterval = setInterval(() => {
            window.scrollBy(0, -scrollSpeed);
        }, 16);
    } else if (e.clientY > viewportHeight - threshold) {
        autoScrollInterval = setInterval(() => {
            window.scrollBy(0, scrollSpeed);
        }, 16);
    }
});

document.addEventListener('dragend', () => {
    if (autoScrollInterval) {
        clearInterval(autoScrollInterval);
        autoScrollInterval = null;
    }
});