export const cartHandler = (targetButton) => {
    let action = targetButton.getAttribute("data-action");
    let productId = targetButton.getAttribute("data-product");

    if (action === "add") {
        if (cart[productId] === undefined) {
            cart[productId] = {"quantity": 1}
        } else {
            cart[productId] = {"quantity": cart[productId]['quantity'] += 1}
        }
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    }
    location.reload();
};




