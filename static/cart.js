// Function to update the cart counter dynamically
function updateCartCount(count) {
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = count; // Update the cart count with the total items
}

// Add to Cart Logic
const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');

addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.dataset.id;
        const productName = button.dataset.name;
        const productPrice = button.dataset.price;

        // Send the product data to the server
        fetch('/add-to-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: productId,
                name: productName,
                price: parseFloat(productPrice),
            }),
        })
        .then(response => response.json())
        .then(cart => {
            // Calculate total items in the cart
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

            // Update cart counter dynamically
            updateCartCount(totalItems);
        })
        .catch(error => console.error('Error adding to cart:', error));
    });
});
// Remove Item
document.querySelectorAll('.btn-remove').forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.dataset.id; // Get the product ID from the button

        // Send a POST request to remove the item
        fetch('/remove-from-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: productId }),
        })
        .then(response => response.json())
        .then(cart => {
            console.log('Item removed, updated cart:', cart); // Debugging
            location.reload(); // Refresh the page to reflect changes
        })
        .catch(error => console.error('Error removing item:', error));
    });
});

