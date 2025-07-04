const matches = {};
let selectedDraggable = null; // To store the currently selected draggable for click-and-drop

document.querySelectorAll(".draggable").forEach(draggable => {
    // Desktop drag-and-drop events
    draggable.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', draggable.id);
        // For mobile, prevent default touch behavior that might interfere
        e.stopPropagation();
    });

    // Click-and-drop functionality
    draggable.addEventListener('click', () => {
        if (selectedDraggable) {
            selectedDraggable.classList.remove('selected');
        }
        selectedDraggable = draggable;
        draggable.classList.add('selected');
    });

    // Mobile touch events to prevent default browser behavior
    draggable.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevent default touch behavior (like scrolling or opening new tab)
        e.stopPropagation();
        if (selectedDraggable) {
            selectedDraggable.classList.remove('selected');
        }
        selectedDraggable = draggable;
        draggable.classList.add('selected');
    }, { passive: false }); // Use passive: false to allow preventDefault
});

document.querySelectorAll('.droppable').forEach(droppable => {
    // Desktop drag-and-drop events
    droppable.addEventListener('dragover', event => event.preventDefault());

    droppable.addEventListener('drop', event => {
        event.preventDefault(); // Ensure default is prevented for drop
        const draggedId = event.dataTransfer.getData('text/plain');
        handleDrop(droppable, draggedId);
    });

    // Click-and-drop functionality
    droppable.addEventListener('click', () => {
        if (selectedDraggable) {
            handleDrop(droppable, selectedDraggable.id);
            selectedDraggable.classList.remove('selected');
            selectedDraggable = null; // Reset selected draggable after drop
        }
    });

    // Mobile touch events for droppable
    droppable.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevent default touch behavior
        e.stopPropagation();
        if (selectedDraggable) {
            handleDrop(droppable, selectedDraggable.id);
            selectedDraggable.classList.remove('selected');
            selectedDraggable = null; // Reset selected draggable after drop
        }
    }, { passive: false });
});

function handleDrop(droppableElement, draggedId) {
    matches[droppableElement.dataset.match] = draggedId;
    droppableElement.textContent = ` (Selected: ${draggedId})`; // Overwrite previous text
    const draggedElement = document.getElementById(draggedId);
    if (draggedElement) {
        draggedElement.classList.add('dropped');
        // Optionally, move the dragged element visually to the droppable area
        // This might require more complex DOM manipulation depending on layout
        // For now, just mark it as dropped.
    }
}

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

function resetQuiz() {
    location.reload();
}

// Auto-scrolling for drag-and-drop (desktop)
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

// Prevent default touch behaviors globally if not handled by specific elements
document.addEventListener('touchmove', (e) => {
    // Only prevent default if not scrolling naturally
    if (e.touches.length === 1) {
        e.preventDefault();
    }
}, { passive: false });

document.addEventListener('touchend', (e) => {
    e.preventDefault(); // Prevent default tap behavior
}, { passive: false });