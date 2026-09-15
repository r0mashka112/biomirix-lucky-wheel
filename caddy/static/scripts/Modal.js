const modal = document.querySelector('[data-js-modal]');
const modalText = document.querySelector('[data-js-modal-text]');
const modalCloseButtons = document.querySelectorAll(
    '[data-js-modal-close]'
);

let onCloseCallback = null;

function openModal(text, onClose = null) {
    modalText.textContent = text;

    onCloseCallback = onClose;

    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');

    if (onCloseCallback) {
        onCloseCallback();

        onCloseCallback = null;
    }
}

modalCloseButtons.forEach(button => {
    button.addEventListener('click', closeModal);
});

export {
    openModal,
    closeModal
};